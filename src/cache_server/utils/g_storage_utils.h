#ifndef CACHE_SERVER_UTILS_G_STORAGE_UTILS
#define CACHE_SERVER_UTILS_G_STORAGE_UTILS

#include "absl/status/statusor.h"

namespace CacheServer {

// Defines methods that operate on Cloud Storage.
class CloudStorageOperator {
public:
  // Reads serialized data from the Cloud Storage.
  absl::StatusOr<std::string>
  ReadContentFromBucket(const std::string &bucket_path,
                        const std::string &filename);

private:
  const std::string project_id_;
};
} // namespace CacheServer

#endif // CACHE_SERVER_UTILS_G_STORAGE_UTILS
