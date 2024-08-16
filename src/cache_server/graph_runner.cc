#include "src/cache_server/graph_runner.h"

#include "absl/time/time.h"
#include "glog/logging.h"
#include "producer_graph.h"
#include "src/cache_server/producers/get_content_from_gcp_storage.h"
#include "src/cache_server/producers/merge_cache_key_name_producer.h"
#include "src/google/protobuf/stubs/status_macros.h"
#include "src/proto/sample.pb.h"
#include <string>

namespace CacheServer {

using ccproducers::Output;
using google::protobuf::util::DoAssignOrReturn;
using sample::CacheMappings;
using sample::Issuer;
using sample::IssuerStats;
using sample::IssuerStatsRequest;
using sample::IssuerStatsResponse;
using sample::OwnershipByInstruments;
using sample::PerInstrumentOwnershipHistory;

constexpr absl::string_view cik_mapping_path = "form_13f/cik_mapping/data";
constexpr absl::string_view cusip_mapping_path = "form_13f/cusip_mapping/data";

bool IsSubstring(const std::string &text, const std::string &key) {
  // Convert both strings to lowercase for case-insensitive comparison.
  std::string textLower = text;
  std::transform(textLower.begin(), textLower.end(), textLower.begin(),
                 ::tolower);
  std::string keyLower = key;
  std::transform(keyLower.begin(), keyLower.end(), keyLower.begin(), ::tolower);

  return std::search(keyLower.begin(), keyLower.end(), textLower.begin(),
                     textLower.end()) != keyLower.end();
}

std::vector<CUSIP> FindMatchingKeys(
    const absl::flat_hash_map<CUSIP, CORP_NAME> &cusip_to_corp_name_map,
    const std::string &text) {
  std::vector<CUSIP> matchingKeys;
  for (const auto &[cusip, corpName] : cusip_to_corp_name_map) {
    if (IsSubstring(text, cusip)) {
      matchingKeys.push_back(cusip);
    } else if (IsSubstring(text, corpName)) {
      matchingKeys.push_back(cusip);
    }
  }
  return matchingKeys;
}

bool NeedUpdate(int timestamp) {
  return absl::FromUnixSeconds(timestamp) - absl::Now() > absl::Hours(24);
}

// TODO
absl::Status
BuildCacheKeyMap(absl::string_view bucket_path, absl::string_view cache_path,
                 absl::flat_hash_map<std::string, CORP_NAME> &cache_map) {
  ccproducers::ProducerGraph graph;
  std::function<Output<absl::string_view>()> bucket_path_fn = [bucket_path]() {
    return bucket_path;
  };
  auto bucket_path_producer = graph.AddProducer(bucket_path_fn);
  std::function<Output<const std::string>()> cache_map_fn = [cache_path]() {
    return static_cast<std::string>(cache_path);
  };
  auto get_cache_map_producer = graph.AddProducer(cache_map_fn);
  auto cache_map_producer = graph.AddProducer(
      &GetContentFromGcpStorage, bucket_path_producer, get_cache_map_producer);
  auto result_future = graph.Execute(cache_map_producer);
  result_future.wait();

  // TODO: Put below in producer. And assign to cik_to_corp_name_map_ or what
  // ever
  CacheMappings cache_mappings;
  if (!cache_mappings.ParseFromString(result_future.get())) {
    LOG(ERROR) << "BuildCacheKeyMap: Failed to parse the cache_mappings.";
  }

  for (const auto &[_, cache_mapping] : cache_mappings.cache_mapping()) {
    cache_map[cache_mapping.key()] = cache_mapping.name();
  }
  LOG(INFO) << "BuildCacheKeyMap: Cache key map built with size of "
            << cache_map.size();
  return absl::OkStatus();
}

absl::StatusOr<IssuerStats>
ComputeOwnershipByInstruments(const Issuer &issuer) {
  IssuerStats out_issuer_stats;

  for (const auto &[cik, history] : issuer.issue_history()) {
    OwnershipByInstruments owner_list;
    owner_list.set_cik(cik);
    owner_list.set_shrs_prn_amt(history.shrs_prn_amt());
    owner_list.set_value(history.value());

    out_issuer_stats.add_owner_lists()->CopyFrom(owner_list);
  }
  return out_issuer_stats;
}

absl::StatusOr<IssuerStatsResponse>
BuildIssuerStatsResponse(absl::string_view bucket_path,
                         absl::string_view cusip) {

  auto response = IssuerStatsResponse();

  ccproducers::ProducerGraph graph;

  std::function<Output<absl::string_view>()> bucket_path_fn = [bucket_path]() {
    return bucket_path;
  };
  auto bucket_path_producer = graph.AddProducer(bucket_path_fn);

  std::function<Output<const std::string>()> cusip_path_fn = [cusip]() {
    return absl::StrCat("issuer/", cusip, "/data");
  };
  auto cusip_producer = graph.AddProducer(cusip_path_fn);
  auto issuer_producer = graph.AddProducer(
      &GetContentFromGcpStorage, bucket_path_producer, cusip_producer);

  auto merged_key_name_response =
      graph.AddProducer(&MergeCacheKeyName, issuer_producer);

  auto issuer_result_future = graph.Execute(merged_key_name_response);
  issuer_result_future.wait();

  response.set_cusip(cusip);

  // Compute for OwnershipByInstruments.
  response.mutable_issuer_stats()->MergeFrom(
      ComputeOwnershipByInstruments(issuer_result_future.get()).value());

  // TODO: Compute for PerInstrumentOwnershipHistory

  response.set_last_update_timestamp(absl::ToUnixSeconds(absl::Now()));
  LOG(INFO) << absl::StrCat("IssuerStatsRequest: Update response ", cusip);

  // This means we find the response in cache and is OK to return.
  return response;
}

IssuerStatsResponse
GraphRunner::PullAllIssuerStatsFromCache(absl::string_view bucket_path,
                                         absl::string_view cusip) {

  auto response = IssuerStatsResponse();

  auto result = issuers_cache_map_.find(cusip);

  // Refresh the cache if the issuer is not in the cache or due to a timeout.
  // Else means we find the response in cache and is OK to return.
  if (result == issuers_cache_map_.end() ||
      NeedUpdate(result->second.last_update_timestamp())) {
    CHECK(
        DoAssignOrReturn(response, BuildIssuerStatsResponse(bucket_path, cusip))
            .ok())
        << "Failed to build response for " << cusip;
    // Append CUSIP name.
    CHECK(BuildCacheKeyMap(bucket_path, cusip_mapping_path,
                           cusip_to_corp_name_map_)
              .ok())
        << "Failed to build cik_to_corp_name_map_";
    response.set_name(cusip_to_corp_name_map_[cusip]);
    // Append CIK name.
    CHECK(BuildCacheKeyMap(bucket_path, cik_mapping_path, cik_to_corp_name_map_)
              .ok())
        << "Failed to build cik_to_corp_name_map_";
    for (auto &owner_list :
         *response.mutable_issuer_stats()->mutable_owner_lists()) {
      owner_list.set_name(cik_to_corp_name_map_[owner_list.cik()]);
    }
  } else {
    response.CopyFrom(result->second);
  }

  issuers_cache_map_[cusip].CopyFrom(response);
  return response;
}

absl::StatusOr<IssuerStatsResponse>
GraphRunner::IssuerStatsGraphRunner(IssuerStatsRequest request,
                                    absl::string_view bucket_path) {
  switch (request.prebuilt_graph()) {

  case IssuerStatsRequest::PULL_ALL_STATS: {
    return PullAllIssuerStatsFromCache(bucket_path, request.cusip());
  }

  // This should be a client error.
  default:
    LOG(ERROR) << "IssuerStatsRequest: Requested graph is not found.";
    return absl::InvalidArgumentError(
        absl::StrCat("IssuerStatsRequest: Unsupported graph type."));
  }
}
}; // namespace CacheServer
