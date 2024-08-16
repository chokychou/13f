var messages = require('./proto/service_pb');
var services = require('./proto/service_grpc_pb');

var grpc = require('@grpc/grpc-js');

export default async function MatchIssuers(text_to_match, target = 'localhost:50051') {
    if (!text_to_match) {
        throw new Error('Cusip is required');
    }

    const client = new services.IssuerGraphServiceClient(target,
        grpc.credentials.createInsecure());

    const request = new messages.MatchIssuersRequest();
    request.setTextToMatch(text_to_match);

    try {
        const response = await new Promise((resolve, reject) => {
            client.matchIssuers(request, (err, res) => {
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
