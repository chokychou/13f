#include "src/cache_server/producers/merge_cache_key_name_producer.h"

#include "glog/logging.h"
#include "src/proto/sample.pb.h"

using ccproducers::Error;
using ccproducers::Input;
using ccproducers::Output;

namespace CacheServer {

using sample::Issuer;

ccproducers::Output<sample::Issuer>
MergeCacheKeyName(ccproducers::Input<std::string> issuer_string) {
  Issuer issuer;
  if (!issuer.ParseFromString(issuer_string.get())) {
    LOG(ERROR) << "IssuerStatsRequest: Failed to parse the issuer result.";
  }

  return issuer;
}
} // namespace CacheServer
