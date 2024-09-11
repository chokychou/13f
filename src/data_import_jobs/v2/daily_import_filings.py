from src.data_import_jobs.v2.scrap_lib import *
import src.tools.protobuf_sql_workflow.workflow as sql_workflow
from src.tools.protobuf_sql_workflow.sql_engine import DbConfig

db_configs = DbConfig(
    host="127.0.0.1",  # Filled in from --db_host
    database="postgres",  # Filled in from --db_name
    user="test_user",  # Filled in from --db_user
    password="test_pw",  # Filled in from --db_password
    port="5432"  # Filled in from --db_port
)

def import_filing_fn(filing):
    sql_workflow.run(db_configs,
        "src/data_import_jobs/v2/insert_form_13f_row_wfl.pbtxt",
        [
            (
                filing["external_id"],
                filing["form_type"], 
                filing["cik"], 
                filing["date_filed"], 
                filing["directory_url"], 
            ),
            (
                filing["external_id"],
                parse_info_table_as_text(filing["info_table"]),
                filing["full_submission_url"], 
            )
        ]
    )

def process_cik_metadata_fn(filing):
    sql_workflow.run(db_configs,
        "src/data_import_jobs/v2/insert_cik_metadata_wfl.pbtxt",
        [
            (
                filing["cik"],
                filing["company_name"], 
                filing["date_filed"], 
            )
        ]
    )

# TODO: This part is going to be ungly because the sql engine does not support return function.
def temp_process_cusip_ownership_per_filing(filing):
    sample = sample_pb2.Sample()
    sample.ParseFromString(parse_info_table_as_text(filing["info_table"]))
    for it in sample.info_table:
        sql_workflow.run(db_configs,
            "src/data_import_jobs/v2/insert_cusip_row_wfl.pbtxt",
            [
                (
                    it.cusip,
                    it.name_of_issuer, 
                ),
                (
                    it.cusip,
                    filing["cik"],
                    # TODO: replace with name. Maybe sample_pb2.ShrsPrnAmt.Name(it.shrs_prn_amt.type),
                    it.shrs_prn_amt.type,
                    it.shrs_prn_amt.number,
                    it.value,
                    filing["date_filed"], 
                )
            ]
        )

def run():
    print("Getting latest 13F filings...")
    for filing in latest_thirteen_f_filings(2):
        # Query latest 13F list, and write metadata to db
        import_filing_fn(filing)
        # Process cik metadata from filings
        process_cik_metadata_fn(filing)
        temp_process_cusip_ownership_per_filing(filing)


if __name__ == "__main__":
    run()