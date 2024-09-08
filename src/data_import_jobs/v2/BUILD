load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//src:__subpackages__"])

filegroup(
    name = "sql_scripts",
    srcs = glob(["*.sql"]),
)

py_library(
    name = "scrap_lib",
    srcs = ["scrap_lib.py"],
    deps = [
        "//src/proto:sample_py_proto",
        requirement("xmltodict"),
        requirement("requests"),
        requirement("beautifulsoup4"),
        requirement("lxml"),
    ],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        ":sql_scripts",
        "insert_form_13f_row_wfl.pbtxt",
        "insert_cik_metadata.pbtxt",
    ],
    deps = [
        ":scrap_lib",
        "//src/tools/protobuf_sql_workflow:workflow",
    ],
)
