var PROTO_PATH = __dirname + '/../../../proto/service.proto';


var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
var services = grpc.loadPackageDefinition(packageDefinition).sample;


function main() {
    target = 'localhost:50051';
    var client = new services.IssuerGraphService(target,
        grpc.credentials.createInsecure());

    client.getIssuerStats({cusip : "002824100", prebuilt_graph: 1}, function (err, response) {
        console.log('Response:', response);
    });

}

main();