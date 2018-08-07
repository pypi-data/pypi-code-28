from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from inflection import camelize
from rest_framework import generics, status
from rest_framework.parsers import FormParser

from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class CamelCaseOperationIDAutoSchema(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys):
        operation_id = super(CamelCaseOperationIDAutoSchema, self).get_operation_id(operation_keys)
        return camelize(operation_id, uppercase_first_letter=False)


class SnippetList(generics.ListCreateAPIView):
    """SnippetList classdoc"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    parser_classes = (FormParser, CamelCaseJSONParser,)
    renderer_classes = (CamelCaseJSONRenderer,)
    swagger_schema = CamelCaseOperationIDAutoSchema

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        """post method docstring"""
        return super(SnippetList, self).post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id='snippets_delete_bulk',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'body': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='this should not crash (request body on DELETE method)'
                )
            }
        ),
    )
    def delete(self, *args, **kwargs):
        pass


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    SnippetDetail classdoc

    put:
    put class docstring

    patch:
    patch class docstring
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    pagination_class = None

    parser_classes = (CamelCaseJSONParser,)
    renderer_classes = (CamelCaseJSONRenderer,)
    swagger_schema = CamelCaseOperationIDAutoSchema

    def patch(self, request, *args, **kwargs):
        """patch method docstring"""
        return super(SnippetDetail, self).patch(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="path parameter override",
                required=True
            ),
            openapi.Parameter(
                name='delete_form_param', in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="this should not crash (form parameter on DELETE method)"
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="this should not crash (response object with no schema)"
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        """delete method docstring"""
        return super(SnippetDetail, self).patch(request, *args, **kwargs)
