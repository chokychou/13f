#include "src/cache_server/producers/get_content_from_gcp_storage.h"

#include "absl/strings/str_cat.h"
#include "absl/strings/string_view.h"
#include "glog/logging.h"
#include "src/cache_server/utils/g_storage_utils.h"

using ccproducers::Error;
using ccproducers::Input;
using ccproducers::Output;

namespace CacheServer {

Output<std::string>
GetContentFromGcpStorage(Input<absl::string_view> bucket_path,
                         Input<const std::string> object_path) {

  auto client = std::make_unique<CacheServer::CloudStorageOperator>();
  auto &object_path_value = object_path.get();
  auto status = client->ReadContentFromBucket(std::string(bucket_path.get()),
                                              object_path_value);
  if (!status.ok()) {
    LOG(ERROR) << absl::StrCat(
        "GetContentFromGcpStorage: Failed to read content: ", status.status());
    return static_cast<std::string>("");
  }
  return static_cast<std::string>(status.value());
}
} // namespace CacheServer
