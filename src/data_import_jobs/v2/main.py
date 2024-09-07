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
                filing["company_name"], 
                filing["form_type"], 
                filing["cik"], 
                filing["date_filed"], 
                filing["directory_url"], 
            ),
            (
                filing["external_id"],
                # TODO: Fix this info_table below
                # filing["info_table"],
                filing["full_submission_url"], 
            )
        ]
    )

def run():
    print("Getting latest 13F filings...")
    # Query latest 13F list and write to db
    for filing in latest_thirteen_f_filings():
        import_filing_fn(filing)


if __name__ == "__main__":
    run()