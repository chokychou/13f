#ifndef CACHE_SERVER_PRODUCERS_GET_CONTENT_FROM_GCP_STORAGE_H
#define CACHE_SERVER_PRODUCERS_GET_CONTENT_FROM_GCP_STORAGE_H

#include "absl/strings/string_view.h"
#include "producer_graph.h"

namespace CacheServer {
ccproducers::Output<std::string>
GetContentFromGcpStorage(ccproducers::Input<absl::string_view> bucket_path,
                         ccproducers::Input<const std::string> object_path);
}

#endif // CACHE_SERVER_PRODUCERS_GET_CONTENT_FROM_GCP_STORAGE_H