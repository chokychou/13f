/*
 *
 * Copyright 2021 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <cmath>
#include <iostream>
#include <memory>
#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/strings/str_format.h"

#include <grpc/grpc.h>
#include <grpcpp/security/server_credentials.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>

#include "src/cache_server/graph_runner.h"

#ifdef BAZEL_BUILD
#include "src/proto/service.grpc.pb.h"
#else
#include "src/proto/service.grpc.pb.h"
#endif

ABSL_FLAG(uint16_t, port, 50051, "Server port for the service");
ABSL_FLAG(std::string, bucket_path, "stocker-datahub-dev",
          "Issuer database path");

using grpc::CallbackServerContext;
using grpc::Server;
using grpc::ServerBuilder;
using grpc::Status;
using sample::IssuerGraphService;
using sample::IssuerStatsRequest;
using sample::IssuerStatsResponse;
using sample::MatchIssuersRequest;
using sample::MatchIssuersResponse;

class ServerImpl final : public IssuerGraphService::CallbackService {
public:
  explicit ServerImpl() {
    graph_runner_ = CacheServer::GraphRunner();
    // Quick load cache data.
    graph_runner_.PullAllIssuerStatsFromCache(absl::GetFlag(FLAGS_bucket_path),
                                              "");
  }

  grpc::ServerUnaryReactor *
  GetIssuerStats(CallbackServerContext *context,
                 const IssuerStatsRequest *request,
                 IssuerStatsResponse *response) override {
    // The actual processing.
    mu_.Lock();
    auto out_response = graph_runner_.IssuerStatsGraphRunner(
        *request, absl::GetFlag(FLAGS_bucket_path));
    mu_.Unlock();

    response->CopyFrom(out_response.value());
    auto *reactor = context->DefaultReactor();
    reactor->Finish(Status::OK);
    return reactor;
  }

  grpc::ServerUnaryReactor *
  MatchIssuers(CallbackServerContext *context,
               const MatchIssuersRequest *request,
               MatchIssuersResponse *response) override {
    // The actual processing.
    mu_.Lock();
    auto keys_vec = CacheServer::FindMatchingKeys(
        graph_runner_.GetCusipToCorpNameMap(), request->text_to_match());
    MatchIssuersResponse out_response;
    for (const auto &key : keys_vec) {
      MatchIssuersResponse::CusipCandidate candidate;
      candidate.set_cusip(key);
      candidate.set_name(absl::StrCat(
          graph_runner_.GetCusipToCorpNameMap().at(key), " ", "(", key, ")"));
      auto next_candidate = out_response.add_cusip_candidate();
      next_candidate->CopyFrom(std::move(candidate));
    }
    mu_.Unlock();

    response->CopyFrom(out_response);
    auto *reactor = context->DefaultReactor();
    reactor->Finish(Status::OK);
    return reactor;
  }

private:
  absl::Mutex mu_;
  CacheServer::GraphRunner graph_runner_ ABSL_GUARDED_BY(mu_);
};

void RunServer(uint16_t port) {
  std::string server_address(absl::StrFormat("0.0.0.0:%d", port));
  ServerImpl service;

  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;
  server->Wait();
}

int main(int argc, char **argv) {
  absl::ParseCommandLine(argc, argv);
  std::cout << "Bucket path: " << absl::GetFlag(FLAGS_bucket_path) << std::endl;
  RunServer(absl::GetFlag(FLAGS_port));
  return 0;
}