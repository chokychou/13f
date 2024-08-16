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
    # {'external_id': '000109544924000066', 'company_name': '13F-HR - Unconventional Investor, LLC (0001910387)', 'form_type': '13F-HR', 'cik': '0001910387', 'date_filed': '2024-08-14', 'directory_url': 'https://www.sec.gov/Archives/edgar/data/1910387/000109544924000066'}
    sql_workflow.run(db_configs,
        "src/data_import_jobs/v2/insert_form_13f_row_wfl.pbtxt",
        tuple(filing.values())
    )

def run():
    print("Getting latest 13F filings...")
    # Query latest 13F list and write to db
    for filing in latest_thirteen_f_filings():
        import_filing_fn(filing)


if __name__ == "__main__":
    run()