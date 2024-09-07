import os
import sys
import src.tools.protobuf_sql_workflow.workflow_pb2 as workflow_pb2
from google.protobuf import text_format
from src.tools.protobuf_sql_workflow.sql_engine import SqlEngine


def parse_sql_workflow(file_path):
    if not file_path:
        print("No file is provided")
        return
    with open(file_path) as f:
        txt = f.read()
    return text_format.Parse(txt, workflow_pb2.SimpleWorkFlow())

def parse_sql_script(file_path) -> str:
    if not file_path:
        print("No file is provided")
        return
    with open(file_path) as f:
        return f.read()
    return ""

def sql_executor(db_configs, script, options):
    sql_engine = SqlEngine(db_configs)
    sql_engine.execute_query(script, options)


def run(db_configs, wfl_file_path, options):
    workflow = parse_sql_workflow(wfl_file_path)
    if workflow:
        print(f"Workflow ({workflow.name}) parsed successfully!")
        for script, option in zip(workflow.sql_script, options):
            print("Executing script:" + script.name)
            sql_executor(db_configs, parse_sql_script(script.path), option)
    else:
        print("Failed to parse workflow.")
