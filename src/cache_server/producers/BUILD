package(default_visibility = ["//src:__subpackages__"])

cc_library(
    name = "get_content_from_gcp_storage",
    srcs = ["get_content_from_gcp_storage.cc"],
    hdrs = ["get_content_from_gcp_storage.h"],
    deps = [
        "//src/cache_server/utils:g_storage_utils",
        "@ccproducers//:producer_graph",
        "@com_github_google_glog//:glog",
        "@com_google_absl//absl/strings",
    ],
)

cc_library(
    name = "merge_cache_key_name_producer",
    srcs = ["merge_cache_key_name_producer.cc"],
    hdrs = ["merge_cache_key_name_producer.h"],
    deps = [
        "//src/proto:sample_cc_proto",
        "@ccproducers//:producer_graph",
        "@com_github_google_glog//:glog",
    ],
)
