package(default_visibility = [
    "//docker:__subpackages__",
    "//src/bin:__subpackages__",
])

cc_binary(
    name = "server",
    srcs = ["server.cc"],
    deps = [
        ":graph_runner",
        "@com_github_grpc_grpc//:grpc++",
        "@com_google_absl//absl/flags:flag",
        "@com_google_absl//absl/flags:parse",
        "@com_google_absl//absl/strings:str_format",
    ],
)

cc_library(
    name = "graph_runner",
    srcs = ["graph_runner.cc"],
    hdrs = ["graph_runner.h"],
    deps = [
        "//src/cache_server/producers:get_content_from_gcp_storage",
        "//src/cache_server/utils:g_storage_utils",
        "//src/proto:sample_cc_proto",
        "//src/proto:service_cc_grpc",
        "@ccproducers//:producer_graph",
        "@com_github_google_glog//:glog",
        "@com_google_absl//absl/time",
        "//src/cache_server/producers:merge_cache_key_name_producer",
    ],
)
