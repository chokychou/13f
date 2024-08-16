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

session = requests.Session()
headers = {
    "User-Agent": "13F Data Scraper (Contact: shenmeguislb@gmail.com)"
}


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

