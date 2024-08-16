var messages = require('./proto/service_pb');
var services = require('./proto/service_grpc_pb');

var grpc = require('@grpc/grpc-js');

export default async function RequestIssuerStats(cusip, graph = 1, target = 'localhost:50051') {
    if (!cusip) {
        throw new Error('Cusip is required');
    }

    const client = new services.IssuerGraphServiceClient(target,
        grpc.credentials.createInsecure());

    const request = new messages.IssuerStatsRequest();
    request.setCusip(cusip);
    request.setPrebuiltGraph(graph);

    try {
        const response = await new Promise((resolve, reject) => {
            client.getIssuerStats(request, (err, res) => {
                if (err) {
                    console.error("Probably the reqested graph isn't implemented.");
                    reject(err);
                } else {
                    resolve(res);
                }
            });
        });

        return response.toObject();
    } catch (err) {
        console.error(err);
        throw err;
    }
}

