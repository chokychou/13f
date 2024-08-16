load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "test",
    srcs = ["test.py"],
    deps = [
        "//src/data_import_jobs:gcp_utils",
        "//src/data_import_jobs:utils",
        requirement("absl-py"),
    ],
)
