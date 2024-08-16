// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var service_pb = require('./service_pb.js');

function serialize_sample_IssuerStatsRequest(arg) {
  if (!(arg instanceof service_pb.IssuerStatsRequest)) {
    throw new Error('Expected argument of type sample.IssuerStatsRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_sample_IssuerStatsRequest(buffer_arg) {
  return service_pb.IssuerStatsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_sample_IssuerStatsResponse(arg) {
  if (!(arg instanceof service_pb.IssuerStatsResponse)) {
    throw new Error('Expected argument of type sample.IssuerStatsResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_sample_IssuerStatsResponse(buffer_arg) {
  return service_pb.IssuerStatsResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_sample_MatchIssuersRequest(arg) {
  if (!(arg instanceof service_pb.MatchIssuersRequest)) {
    throw new Error('Expected argument of type sample.MatchIssuersRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_sample_MatchIssuersRequest(buffer_arg) {
  return service_pb.MatchIssuersRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_sample_MatchIssuersResponse(arg) {
  if (!(arg instanceof service_pb.MatchIssuersResponse)) {
    throw new Error('Expected argument of type sample.MatchIssuersResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_sample_MatchIssuersResponse(buffer_arg) {
  return service_pb.MatchIssuersResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// The sample service definition.
var IssuerGraphServiceService = exports.IssuerGraphServiceService = {
  // Sends a transaction
getIssuerStats: {
    path: '/sample.IssuerGraphService/GetIssuerStats',
    requestStream: false,
    responseStream: false,
    requestType: service_pb.IssuerStatsRequest,
    responseType: service_pb.IssuerStatsResponse,
    requestSerialize: serialize_sample_IssuerStatsRequest,
    requestDeserialize: deserialize_sample_IssuerStatsRequest,
    responseSerialize: serialize_sample_IssuerStatsResponse,
    responseDeserialize: deserialize_sample_IssuerStatsResponse,
  },
  matchIssuers: {
    path: '/sample.IssuerGraphService/MatchIssuers',
    requestStream: false,
    responseStream: false,
    requestType: service_pb.MatchIssuersRequest,
    responseType: service_pb.MatchIssuersResponse,
    requestSerialize: serialize_sample_MatchIssuersRequest,
    requestDeserialize: deserialize_sample_MatchIssuersRequest,
    responseSerialize: serialize_sample_MatchIssuersResponse,
    responseDeserialize: deserialize_sample_MatchIssuersResponse,
  },
};

exports.IssuerGraphServiceClient = grpc.makeGenericClientConstructor(IssuerGraphServiceService);
