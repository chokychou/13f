#ifndef CACHE_SERVER_PRODUCERS_MERGE_CACHE_KEY_NAME_PRODUCER_H
#define CACHE_SERVER_PRODUCERS_MERGE_CACHE_KEY_NAME_PRODUCER_H

#include "producer_graph.h"
#include "src/proto/sample.pb.h"

namespace CacheServer {
// TODO: Rename. This function cast issuer. it does not have the merge logic.
ccproducers::Output<sample::Issuer>
MergeCacheKeyName(ccproducers::Input<std::string> issuer_string);
}

#endif // CACHE_SERVER_PRODUCERS_MERGE_CACHE_KEY_NAME_PRODUCER_H