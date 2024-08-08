# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'stt','app')))

from protos import stt_service_pb2

GRPC_GENERATED_VERSION = '1.65.2'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.66.0'
SCHEDULED_RELEASE_DATE = 'August 6, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in stt_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class STTServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ConvertSpeechToText = channel.unary_unary(
                '/stt.STTService/ConvertSpeechToText',
                request_serializer=stt_service_pb2.SpeechRequest.SerializeToString,
                response_deserializer=stt_service_pb2.SpeechResponse.FromString,
                _registered_method=True)


class STTServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ConvertSpeechToText(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_STTServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ConvertSpeechToText': grpc.unary_unary_rpc_method_handler(
                    servicer.ConvertSpeechToText,
                    request_deserializer=stt_service_pb2.SpeechRequest.FromString,
                    response_serializer=stt_service_pb2.SpeechResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'stt.STTService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('stt.STTService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class STTService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ConvertSpeechToText(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/stt.STTService/ConvertSpeechToText',
            stt_service_pb2.SpeechRequest.SerializeToString,
            stt_service_pb2.SpeechResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
