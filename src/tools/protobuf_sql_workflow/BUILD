load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")
load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//src:__subpackages__"])

proto_library(
    name = "workflow_proto",
    srcs = ["workflow.proto"],
)

py_proto_library(
    name = "workflow_py_proto",
    deps = [":workflow_proto"],
)

# Make to py_library
py_library(
    name = "workflow",
    srcs = ["workflow.py"],
    deps = [
        requirement("absl-py"),
        requirement("psycopg2-binary"),
        ":sql_engine",
        ":workflow_py_proto",
    ],
)

py_library(
    name = "sql_engine",
    srcs = ["sql_engine.py"],
    deps = [
        requirement("absl-py"),
        requirement("psycopg2-binary"),
    ],
)

# TODO: use py_test
py_binary(
    name = "sql_engine_test",
    srcs = ["sql_engine_test.py"],
    deps = [
        ":sql_engine",
        requirement("absl-py"),
        requirement("psycopg2-binary"),
    ],
)
