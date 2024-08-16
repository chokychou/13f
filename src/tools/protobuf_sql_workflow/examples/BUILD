load("@pip//:requirements.bzl", "requirement")

filegroup(
    name = "sql_scripts",
    srcs = glob(["*.sql"]),
)

py_binary(
    name = "example",
    srcs = ["example.py"],
    data = [
        "workflow.pbtxt",
        ":sql_scripts",
    ],
    deps = [
        "//src/tools/protobuf_sql_workflow:workflow",
        requirement("protobuf"),
    ],
)
