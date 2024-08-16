#ifndef CACHE_SERVER_GRAPH_RUNNER_H
#define CACHE_SERVER_GRAPH_RUNNER_H

#include "absl/container/flat_hash_map.h"
#include "absl/status/statusor.h"
#include "src/proto/service.pb.h"
#include <string>

// TODO: check arg2 status is ok.
#ifndef ASSIGN_ELSE_ERROR
#define ASSIGN_ELSE_ERROR(arg1, arg2) arg1 = std::move(arg2.value())
#endif

#define CORP_NAME std::string
#define CUSIP std::string
#define CIK std::string

namespace CacheServer {

bool IsSubstring(const std::string &text, const std::string &key);

std::vector<CUSIP> FindMatchingKeys(
    const absl::flat_hash_map<CUSIP, CORP_NAME> &cusip_to_corp_name_map,
    const std::string &text);

class GraphRunner {
public:
  GraphRunner() = default;
  virtual ~GraphRunner() = default;

  absl::StatusOr<sample::IssuerStatsResponse>
  IssuerStatsGraphRunner(sample::IssuerStatsRequest,
                         absl::string_view bucket_path);

  // Implement sample::PULL_ISSSUER_FROM_CACHE method. Pulls issuers from the
  // cache and assign to the response.
  sample::IssuerStatsResponse
  PullAllIssuerStatsFromCache(absl::string_view bucket_path,
                              absl::string_view cusip);

  const absl::flat_hash_map<CUSIP, CORP_NAME> &GetCusipToCorpNameMap() {
    return cusip_to_corp_name_map_;
  }

private:
  absl::flat_hash_map<CUSIP, sample::IssuerStatsResponse> issuers_cache_map_;

  absl::flat_hash_map<CUSIP, CORP_NAME> cusip_to_corp_name_map_;
  absl::flat_hash_map<CIK, CORP_NAME> cik_to_corp_name_map_;
};

} // namespace CacheServer

#endif // CACHE_SERVER_GRAPH_RUNNER_H
