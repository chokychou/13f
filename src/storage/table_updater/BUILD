load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "table_updater",
    srcs = ["table_updater.py"],
    data = [
        "workflow.pbtxt",
        "//src/storage:sql_scripts",
    ],
    deps = [
        "//src/tools/protobuf_sql_workflow:workflow",
        requirement("protobuf"),
    ],
)
