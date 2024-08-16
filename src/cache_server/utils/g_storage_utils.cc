#include "src/cache_server/utils/g_storage_utils.h"

#include "google/cloud/storage/client.h"
#include "google/cloud/storage/client_options.h"
#include <string>
#include "absl/strings/str_cat.h"

namespace CacheServer {

absl::StatusOr<std::string>
CloudStorageOperator::ReadContentFromBucket(const std::string &bucket_path,
                                            const std::string &filename) {

  auto client_options =
      google::cloud::storage::ClientOptions::CreateDefaultClientOptions();
  client_options->set_project_id(project_id_);

  google::cloud::storage::Client client(*client_options);

  auto reader = client.ReadObject(bucket_path, filename);
  if (!reader) {
    return absl::NotFoundError(absl::StrCat(
        "ReadContentFromBucket: Error reading object at ", bucket_path, "/",
        filename, ": ", reader.status().message()));
  }

  std::string contents{std::istreambuf_iterator<char>{reader}, {}};
  return contents;
}

} // namespace CacheServer
