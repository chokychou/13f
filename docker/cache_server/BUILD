load("@rules_oci//oci:defs.bzl", "oci_image", "oci_tarball")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")


######################################
# Server image                       #
######################################

pkg_tar(
    name = "server_tar",
    srcs = ["//src/cache_server:server"],
)

# Making image
oci_image(
    name = "server_image",
    base = "@docker_lib_cc_ubuntu",
    tars = [":server_tar"],
    workdir = "/",
    entrypoint = ["/server", "--bucket_path='stocker-datahub-prod'"],
)

# $ docker run -p 50051:50051 --rm server:local
oci_tarball(
    name = "server_image_tarball",
    image = ":server_image",
    repo_tags = ["server:local"],
)
