load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//src:__subpackages__"])

py_binary(
    name = "daily_importer",
    srcs = ["daily_importer.py"],
    deps = [
        ":gcp_utils",
        ":utils",
        ":daily_import_filings",
        ":daily_import_process",
        requirement("absl-py"),
    ],
)

py_binary(
    name = "daily_import_filings",
    srcs = ["daily_import_filings.py"],
    deps = [
        ":gcp_utils",
        ":utils",
        requirement("absl-py"),
    ],
)

py_binary(
    name = "daily_import_process",
    srcs = ["daily_import_process.py"],
    deps = [
        ":gcp_utils",
        ":utils",
        requirement("absl-py"),
    ],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        "//src/proto:sample_py_proto",
        requirement("xmltodict"),
        requirement("requests"),
        requirement("beautifulsoup4"),
        requirement("lxml"),
    ],
)

py_library(
    name = "gcp_utils",
    srcs = ["gcp_utils.py"],
    deps = [
        requirement("grpcio"),
        requirement("google-api-core"),
        requirement("google-cloud-core"),
        requirement("google-cloud-storage"),
    ],
)
