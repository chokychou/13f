import src.tools.protobuf_sql_workflow.workflow as sql_workflow
from src.tools.protobuf_sql_workflow.sql_engine import DbConfig

if __name__ == "__main__":
    db_configs = DbConfig(
        host="127.0.0.1",  # Filled in from --db_host
        database="postgres",  # Filled in from --db_name
        user="test_user",  # Filled in from --db_user
        password="test_pw",  # Filled in from --db_password
        port="5432"  # Filled in from --db_port
    )
    sql_workflow.run(db_configs, "src/tools/protobuf_sql_workflow/examples/workflow.pbtxt")