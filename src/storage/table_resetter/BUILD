load("@pip//:requirements.bzl", "requirement")

filegroup(
    name = "sql_scripts",
    srcs = glob(["*.sql"]),
)

py_binary(
    name = "table_resetter",
    srcs = ["table_resetter.py"],
    data = [
        "workflow.pbtxt",
        ":sql_scripts",
        "//src/storage:sql_scripts",
    ],
    deps = [
        "//src/tools/protobuf_sql_workflow:workflow",
        requirement("protobuf"),
    ],
)
