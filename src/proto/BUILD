load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")
load(
    "@com_github_grpc_grpc//bazel:cc_grpc_library.bzl",
    "cc_grpc_library",
)

package(default_visibility = ["//src:__subpackages__"])

proto_library(
    name = "sample_proto",
    srcs = ["sample.proto"],
)

cc_proto_library(
    name = "sample_cc_proto",
    deps = [":sample_proto"],
)

proto_library(
    name = "service_proto",
    srcs = ["service.proto"],
)

cc_proto_library(
    name = "service_cc_proto",
    deps = [":service_proto"],
)

cc_grpc_library(
    name = "service_cc_grpc",
    srcs = [":service_proto"],
    grpc_only = True,
    deps = [
        ":service_cc_proto",
    ],
)

py_proto_library(
    name = "sample_py_proto",
    deps = [":sample_proto"],
)
