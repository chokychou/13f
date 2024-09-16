import src.tools.protobuf_sql_workflow.workflow as sql_workflow
from src.tools.protobuf_sql_workflow.sql_engine import DbConfig

db_configs = DbConfig(
    host="127.0.0.1",  # Filled in from --db_host
    database="postgres",  # Filled in from --db_name
    user="test_user",  # Filled in from --db_user
    password="test_pw",  # Filled in from --db_password
    port="5432"  # Filled in from --db_port
)

# TODO: temporary helper function. remove.
def print_callback(result):
    print(result)

def compute_ownership_by_instrument():
    sql_workflow.run(db_configs,
        "src/data_import_jobs/v2/compute_ownership_by_instrument_wfl.pbtxt",
        [()],
        print_callback
    )

def run():
    print("Computing ownership for companies...")
    compute_ownership_by_instrument()


if __name__ == "__main__":
    run()