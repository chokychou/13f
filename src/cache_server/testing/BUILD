package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "client",
    srcs = ["client.cc"],
    defines = ["BAZEL_BUILD"],
    deps = [
        "//src/proto:service_cc_grpc",
        "@com_google_absl//absl/flags:flag",
        "@com_google_absl//absl/flags:parse",
        '@com_github_grpc_grpc//:grpc++',
    ],
)

cc_binary(
    name = "mock_server",
    srcs = ["mock_server.cc"],
    deps = [
        "@com_github_grpc_grpc//:grpc++",
        "@com_google_absl//absl/flags:flag",
        "@com_google_absl//absl/flags:parse",
        "@com_google_absl//absl/strings:str_format",
        "//src/proto:service_cc_grpc",
    ],
)
