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

# TODO: Rename below binary with main suffix.
py_binary(
    name = "daily_import_filings",
    srcs = ["daily_import_filings.py"],
    data = [
        ":sql_scripts",
        "insert_form_13f_row_wfl.pbtxt",
        "insert_cik_metadata_wfl.pbtxt",
        "insert_cusip_row_wfl.pbtxt",
    ],
    deps = [
        ":scrap_lib",
        "//src/tools/protobuf_sql_workflow:workflow",
    ],
)

py_binary(
    name = "compute_ownership_by_instrument_main",
    srcs = ["compute_ownership_by_instrument_main.py"],
    data = [
        ":sql_scripts",
        "compute_ownership_by_instrument_wfl.pbtxt",
    ],
    deps = [
        "//src/tools/protobuf_sql_workflow:workflow",
    ],
)
