


#include <iostream>
#include <memory>
#include <string>
#include <thread>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"

#include <grpc/support/log.h>
#include <grpcpp/grpcpp.h>

#ifdef BAZEL_BUILD
#include "src/proto/service.grpc.pb.h"
#else
#include "src/proto/service.grpc.pb.h"
#endif

ABSL_FLAG(std::string, target, "localhost:50051", "Server address");

using grpc::Channel;
using grpc::Status;
using grpc::ClientContext;
using grpc::CompletionQueue;

using sample::IssuerStatsRequest;
using sample::IssuerStatsResponse;
using sample::IssuerGraphService;

class Client {
public:
    explicit Client(std::shared_ptr<Channel> channel)
        : stub_(IssuerGraphService::NewStub(channel)) {}

    void GetIssuerStats(const std::string& user){
        IssuerStatsRequest request;
        request.set_cusip(user);
        IssuerStatsResponse response;
        ClientContext context;
        Status status = stub_->GetIssuerStats(&context, request, &response);

        if (status.ok()) {
            std::cout << "Issuer stats for user: " << user << std::endl;
        } else {
            std::cerr << "RPC failed: " << status.error_message() << std::endl;
        }

    }

private:
    std::unique_ptr<IssuerGraphService::Stub> stub_;


};


int main(int argc, char** argv){
    absl::ParseCommandLine(argc, argv);
    std::string target_str = absl::GetFlag(FLAGS_target);
    std::shared_ptr<grpc::Channel> channel = grpc::CreateChannel(
        target_str, grpc::InsecureChannelCredentials());
    Client client(channel);
    std::string user("00287Y109");
    client.GetIssuerStats("user");
    return 0;
}
