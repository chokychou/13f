import os
import re
import xmltodict
import requests
from collections import defaultdict
from typing import List, Dict
from urllib.parse import urljoin
import datetime
from bs4 import BeautifulSoup
import warnings
import functools
from concurrent.futures import ThreadPoolExecutor
import src.proto.sample_pb2 as sample_pb2
from dataclasses import dataclass

BASE_URL = "https://www.sec.gov"
EXPECTED_COL_NAMES = ["cik", "company_name", "form_type", "date_filed", "filename"]
THIRTEEN_F_FORM_TYPES = ["13F-HR", "13F-HR/A"]


fileCacheDailyFn = lambda date: os.path.join(
    "form_13f",
    "raw",
    parse_path_doc_ref(date),
    date,
    "data",
)


issuerCacheFn = lambda cusip, form: os.path.join("issuer", cusip, form)

cikPathGen = lambda: os.path.join("form_13f", "cik_mapping", "data")

cusipPathGen = lambda: os.path.join("form_13f", "cusip_mapping", "data")

@dataclass
class Struct:
    gcp_project_id: str
    database_id: str

def check_env(func):
    def helper():
        if FLAGS.job_stage not in ["dev", "staging", "prod"]:
            raise ValueError("Invalid job stage.")

    return func


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


session = requests.Session()
headers = {
    "User-Agent": "13F Data Scraper (Contact: shenmeguislb@gmail.com)"
}

filenameFn = lambda filing_year, filing_quarter: os.path.join(
    "tmp",
    "sec_daily_index_files",
    str(filing_year),
    f"QTR{filing_quarter}",
    "master.idx",
)


def download_and_save_sec_filings(
    filing_year: int, filing_quarter: str, delete_tmpfile: bool = True
) -> None:
    url = f"{BASE_URL}/Archives/edgar/full-index/{filing_year}/QTR{filing_quarter}/master.idx"

    filename = filenameFn(filing_year, filing_quarter)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    response = session.get(url, headers=headers)
    with open(filename, "w") as f:
        f.write(response.text)


def padded_cik(str_or_int):
    """Converts a string or integer to a 10-character string padded with zeros.

    Args:
        str_or_int: The string or integer to convert.

    Returns:
        A 10-character string padded with zeros.
    """
    # Convert the input to a string.
    str_val = str(str_or_int)
    # Strip any whitespace from the string.
    str_val = str_val.strip()
    padded_val = str_val.rjust(10, "0")
    return padded_val


def organize_forms_by_types(
    filing_year: int, filing_quarter: str, form_types: List[str] = []
) -> List[Dict]:
    thirteen_fs = []
    col_names = None

    filename = filenameFn(filing_year, filing_quarter)

    with open(filename) as f:
        for raw_line in f:
            line = raw_line.strip().split("|")
            if len(line) == len(EXPECTED_COL_NAMES):
                if col_names is None:
                    col_names = [n.lower().replace(" ", "_") for n in line]
                    if col_names != EXPECTED_COL_NAMES:
                        raise ValueError("Unexpected column names")

                    continue

                row = dict(zip(col_names, line))

                if row["form_type"] in form_types:
                    full_submission_url = urljoin(
                        BASE_URL + "Archives/", row["filename"]
                    )
                    dir_url = full_submission_url[:-4].replace("-", "")

                    thirteen_fs.append(
                        {
                            "external_id": dir_url.split("/")[-1],
                            "company_name": row["company_name"],
                            "form_type": row["form_type"].upper(),
                            "cik": padded_cik(row["cik"]),
                            "date_filed": row["date_filed"].replace(".", "-"),
                            "full_submission_url": full_submission_url,
                            "directory_url": dir_url,
                        }
                    )

    return thirteen_fs

def latest_thirteen_f_filings(
    filed_since: str = (datetime.date.today() - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ),
    per_page: int = 100,
    max_pages: int = 100,
) -> List[Dict]:
    url = f"{BASE_URL}/cgi-bin/browse-edgar"

    query_params = {
        "action": "getcurrent",
        "count": per_page,
        "output": "atom",
        "type": "13F-HR",
        "start": 0,
    }

    title_regex = re.compile(r"\A13F\-HR(?:\/A)? - (.+?) \((\d{10})\)")

    results = []

    for _ in range(max_pages):
        response = session.get(url, headers=headers, params=query_params)
        print("Sec server response code: ", response.status_code, "\n", response.headers)
        soups = BeautifulSoup(response.text, "html.parser")
        for soup in soups.select("entry"):
            filing_date_raw = soup.select_one("updated", features="xml").text
            filing_date = datetime.datetime.strptime(
                filing_date_raw, "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            if filing_date < datetime.datetime.strptime(filed_since, "%Y-%m-%d").date():
                continue
            directory_url = "/".join(
                soup.select_one("link", features="xml")["href"].split("/")[0:-1]
            )
            external_id = directory_url.split("/")[-1]
            cik = padded_cik(directory_url.split("/")[-2])
            form_type = soup.select_one("category", features="xml")["term"]

            company_name = title_regex.search(
                soup.select_one("title", features="xml").text
            ).group()
            results.append(
                {
                    "external_id": external_id,
                    "company_name": company_name,
                    "form_type": form_type,
                    "cik": cik,
                    "date_filed": filing_date.strftime("%Y-%m-%d"),
                    "directory_url": directory_url,
                }
            )

        if len(soups.find_all("entry")) < per_page:
            break

        query_params["start"] += per_page
    return results


def construct_xml_urls(directory_url):
    """
    Extracts the URLs of all XML files from the given SEC Edgar directory URL.

    Args:
        directory_url: The URL of the SEC Edgar directory.

    Returns:
        A list of URLs for the XML files.

    Raises:
        XmlUrlsNotFound: If no XML files are found in the directory.
    """

    # Get the HTML content of the directory page.
    response = session.get(directory_url, headers=headers)
    html = response.content

    # Parse the HTML content using BeautifulSoup.
    soup = BeautifulSoup(html, "html.parser")

    # Find all <a> tags containing links to XML files.
    xml_links = soup.select("#main-content a[href$='.xml']")

    # Extract the full URLs from the relative links.
    xml_urls = [BASE_URL + link["href"] for link in xml_links]

    # Raise an exception if no XML files are found.
    if not xml_urls:
        raise Exception("No XML files found in directory.")

    return xml_urls


def extract_primary_doc_url(xml_urls):
    """
    Finds the URL of the primary document from a list of SEC Edgar XML file URLs.

    Args:
        xml_urls: A list of URLs for SEC Edgar XML files.

    Returns:
        The URL of the primary document, or None if not found.
    """

    # Check for a URL containing "primary.doc" in the filename.
    for url in xml_urls:
        if "primary.doc" in url.lower():
            return url

    # Otherwise, find the URL of the first XML file that contains an "edgarSubmission" element.
    for url in xml_urls:
        response = session.get(url, headers=headers)
        xml = BeautifulSoup(response.content, "xml")
        if xml.find("edgarSubmission"):
            return url

    # If no primary document is found, return None.
    return None


def extract_info_table_url(xml_urls):
    """
    Finds the URL of the information table from a list of SEC Edgar XML file URLs.

    Args:
        xml_urls: A list of URLs for SEC Edgar XML files.

    Returns:
        The URL of the information table, or None if not found.
    """

    # Check for a URL containing "info.table" in the filename.
    for url in xml_urls:
        if "info.table" in url.lower():
            return url

    # Otherwise, find the URL of the first XML file that contains an "informationTable" element.
    for url in xml_urls:
        response = session.get(url, headers=headers)
        xml = BeautifulSoup(response.content, "xml")
        if xml.find("informationTable"):
            return url

    # If no information table is found, return None.
    return None


def get_holdings_from_13f_xml_as_dict(xml_url):
    def remove_prefix_from_keys(d):
        """
        Recursively remove a common prefix from all keys in a dictionary.

        Args:
            d (dict): The dictionary to modify.
            prefix (str): The prefix to remove from the keys.

        Returns:
            dict: The modified dictionary.
        """
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = remove_prefix_from_keys(v)
            if isinstance(v, list):
                v = [remove_prefix_from_keys(item) for item in v]

            while k.find(":") > 0:
                colon_index = k.find(":")
                k = k[colon_index + 1 :]
            new_dict[k] = v
        return new_dict

    try:
        response = session.get(xml_url, headers=headers)
        xml_dict = xmltodict.parse(response.text)
        return remove_prefix_from_keys(xml_dict)
    except:
        return ""


def process_latest_filings(latest_filings):
    """
    This function processes each latest filing in a list by constructing XML URLs,
    extracting full submission URLs, and fetching meta data from XML.

    Args:
        latest_filings (List[Dict]): A list of dictionaries containing information about the latest filings.

    Returns:
        None (Modifies the 'latest_filings' list in-place): Adds two new keys to each dictionary:
            - 'full_submission_url': The extracted full submission URL.
            - 'meta_data': A dictionary containing the holdings data fetched from the 13F XML.

    """
    xml_urls = construct_xml_urls(latest_filings["directory_url"])
    full_submission_url = extract_info_table_url(xml_urls)
    latest_filings["full_submission_url"] = full_submission_url
    latest_filings["info_table"] = get_holdings_from_13f_xml_as_dict(
        full_submission_url
    )
    return latest_filings


def parse_to_proto_str(data):
    def shrs_prn_amt_builder(raw_shrs_prn_amt):
        out_shrs_prn_amt = sample_pb2.ShrsPrnAmt()
        out_shrs_prn_amt.number = int(raw_shrs_prn_amt["sshPrnamt"])

        if raw_shrs_prn_amt["sshPrnamtType"] in "SHRS":
            out_shrs_prn_amt.type = sample_pb2.ShrsPrnAmt().SHRS

        if raw_shrs_prn_amt["sshPrnamtType"] in "PRN":
            out_shrs_prn_amt.type = sample_pb2.ShrsPrnAmt().PRN

        return out_shrs_prn_amt

    def form_type_matcher(todo):
        return 1

    def info_table_builder(out_info_table, raw_info_table):

        try:
            data_sets = raw_info_table["informationTable"]["infoTable"]
        except:
            print(raw_info_table)
            print("we have an error")
            return 0

        if type(data_sets) is not list:
            data_sets = [data_sets]

        for data in data_sets:
            info_table = sample_pb2.InfoTable()
            info_table.name_of_issuer = data["nameOfIssuer"]
            info_table.cusip = data["cusip"]
            info_table.value = int(data["value"])
            info_table.shrs_prn_amt.MergeFrom(
                shrs_prn_amt_builder(data["shrsOrPrnAmt"])
            )
            out_info_table.append(info_table)

        return 1

    sample = sample_pb2.Sample()
    sample.external_id = data["external_id"]
    sample.cik = data["cik"]
    sample.date_filed = data["date_filed"]
    sample.directory_url = data["directory_url"]
    sample.form_type = form_type_matcher(data["form_type"])
    status = info_table_builder(sample.info_table, data["info_table"])

    print(
        f"Decoded filings {sample.cik} with id {sample.external_id}: OK"
        if status
        else f"Decoded filings id {sample.external_id}: ERROR"
    )
    return sample


def parse_path_doc_ref(date_string):
    """
    This function parses the path and doc_ref from a given filing.

    Args:
        date_string (str): String of date

    Returns:
        doc ref string (str): The doc ref string.
    """

    # Convert string to datetime object
    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")

    # Extract year
    year = date_obj.year

    # Calculate quarter (Q1 = January - March, Q2 = April - June, Q3 = July - September, Q4 = October - December)
    quarter = 1 + ((date_obj.month - 1) // 3)

    # Return year and quarter as a tuple or separate variables
    return str(year) + "-Q" + str(quarter)


def update_issuer_with_new_entry(p_issuer, n_entry, metadata):
    """_summary_

    Args:
        p_issuer (_type_): Read from the cache (storage + cache map)
        n_entry (_type_): Read from the lastest filing
        metadata (_type_): Some data for quick insertion

    Raises:
        Exception: When cusip dismatches

    Returns:
        _type_: p_issuer
    """
    if not p_issuer.cusip:
        p_issuer.cusip = n_entry.cusip

    if p_issuer.cusip != n_entry.cusip:
        raise Exception(
            f"update_issuer_with_new_entry: Issuer {p_issuer.cusip} does not match new issuer {n_entry.cusip}"
        )

    # build an issue history
    n_issue_history = sample_pb2.IssueHistory()
    n_issue_history.filing_id = metadata[0]
    n_issue_history.date_filed = metadata[1]
    n_issue_history.shrs_prn_amt = n_entry.shrs_prn_amt.number
    n_issue_history.value = n_entry.value
    # cik key ensures unique entry
    p_issuer.issue_history[metadata[2]].CopyFrom(n_issue_history)

    return p_issuer


def generate_cik_mapping(data):
    cik_mapping = sample_pb2.CacheMapping()
    cik_mapping.key = data["cik"]
    cik_mapping.name = data["company_name"]
    cik_mapping.date = data["date_filed"]
    return cik_mapping

def generate_cusip_mapping(data):
    cusip_mapping = sample_pb2.CacheMapping()
    cusip_mapping.key = data.cusip
    cusip_mapping.name = data.name_of_issuer
    # TODO: add date_filed
    cusip_mapping.date = ""

    return cusip_mapping
