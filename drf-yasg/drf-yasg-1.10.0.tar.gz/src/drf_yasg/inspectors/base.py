import inspect
import logging

from rest_framework import serializers

from .. import openapi
from ..utils import force_real_str, get_field_default, is_list_view

#: Sentinel value that inspectors must return to signal that they do not know how to handle an object
NotHandled = object()

logger = logging.getLogger(__name__)


class BaseInspector(object):
    def __init__(self, view, path, method, components, request):
        """
        :param view: the view associated with this endpoint
        :param str path: the path component of the operation URL
        :param str method: the http method of the operation
        :param openapi.ReferenceResolver components: referenceable components
        :param Request request: the request made against the schema view; can be None
        """
        self.view = view
        self.path = path
        self.method = method
        self.components = components
        self.request = request

    def process_result(self, result, method_name, obj, **kwargs):
        """After an inspector handles an object (i.e. returns a value other than :data:`.NotHandled`), all inspectors
        that were probed get the chance to alter the result, in reverse order. The inspector that handled the object
        is the first to receive a ``process_result`` call with the object it just returned.

        This behaviour is similar to the Django request/response middleware processing.

        If this inspector has no post-processing to do, it should just ``return result`` (the default implementation).

        :param result: the return value of the winning inspector, or ``None`` if no inspector handled the object
        :param str method_name: name of the method that was called on the inspector
        :param obj: first argument passed to inspector method
        :param kwargs: additional arguments passed to inspector method
        :return:
        """
        return result

    def probe_inspectors(self, inspectors, method_name, obj, initkwargs=None, **kwargs):
        """Probe a list of inspectors with a given object. The first inspector in the list to return a value that
        is not :data:`.NotHandled` wins.

        :param list[type[BaseInspector]] inspectors: list of inspectors to probe
        :param str method_name: name of the target method on the inspector
        :param obj: first argument to inspector method
        :param dict initkwargs: extra kwargs for instantiating inspector class
        :param kwargs: additional arguments to inspector method
        :return: the return value of the winning inspector, or ``None`` if no inspector handled the object
        """
        initkwargs = initkwargs or {}
        tried_inspectors = []

        for inspector in inspectors:
            assert inspect.isclass(inspector), "inspector must be a class, not an object"
            assert issubclass(inspector, BaseInspector), "inspectors must subclass BaseInspector"

            inspector = inspector(self.view, self.path, self.method, self.components, self.request, **initkwargs)
            tried_inspectors.append(inspector)
            method = getattr(inspector, method_name, None)
            if method is None:
                continue

            result = method(obj, **kwargs)
            if result is not NotHandled:
                break
        else:  # pragma: no cover
            logger.warning("%s ignored because no inspector in %s handled it (operation: %s)",
                           obj, inspectors, method_name)
            result = None

        for inspector in reversed(tried_inspectors):
            result = inspector.process_result(result, method_name, obj, **kwargs)

        return result


class PaginatorInspector(BaseInspector):
    """Base inspector for paginators.

    Responisble for determining extra query parameters and response structure added by given paginators.
    """

    def get_paginator_parameters(self, paginator):
        """Get the pagination parameters for a single paginator **instance**.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `paginator`.

        :param BasePagination paginator: the paginator
        :rtype: list[openapi.Parameter]
        """
        return NotHandled

    def get_paginated_response(self, paginator, response_schema):
        """Add appropriate paging fields to a response :class:`.Schema`.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `paginator`.

        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """
        return NotHandled


class FilterInspector(BaseInspector):
    """Base inspector for filter backends.

    Responsible for determining extra query parameters added by given filter backends.
    """

    def get_filter_parameters(self, filter_backend):
        """Get the filter parameters for a single filter backend **instance**.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `filter_backend`.

        :param BaseFilterBackend filter_backend: the filter backend
        :rtype: list[openapi.Parameter]
        """
        return NotHandled


class FieldInspector(BaseInspector):
    """Base inspector for serializers and serializer fields. """

    def __init__(self, view, path, method, components, request, field_inspectors):
        super(FieldInspector, self).__init__(view, path, method, components, request)
        self.field_inspectors = field_inspectors

    def add_manual_fields(self, serializer_or_field, schema):
        """Set fields from the ``swagger_schem_fields`` attribute on the Meta class. This method is called
        only for serializers or fields that are converted into ``openapi.Schema`` objects.

        :param serializer_or_field: serializer or field instance
        :param openapi.Schema schema: the schema object to be modified in-place
        """
        meta = getattr(serializer_or_field, 'Meta', None)
        swagger_schema_fields = getattr(meta, 'swagger_schema_fields', {})
        if swagger_schema_fields:
            for attr, val in swagger_schema_fields.items():
                setattr(schema, attr, val)

    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        """Convert a drf Serializer or Field instance into a Swagger object.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `field`.

        :param rest_framework.serializers.Field field: the source field
        :param type[openapi.SwaggerDict] swagger_object_type: should be one of Schema, Parameter, Items
        :param bool use_references: if False, forces all objects to be declared inline
           instead of by referencing other components
        :param kwargs: extra attributes for constructing the object;
           if swagger_object_type is Parameter, ``name`` and ``in_`` should be provided
        :return: the swagger object
        :rtype: openapi.Parameter,openapi.Items,openapi.Schema,openapi.SchemaRef
        """
        return NotHandled

    def probe_field_inspectors(self, field, swagger_object_type, use_references, **kwargs):
        """Helper method for recursively probing `field_inspectors` to handle a given field.

        All arguments are the same as :meth:`.field_to_swagger_object`.

        :rtype: openapi.Parameter,openapi.Items,openapi.Schema,openapi.SchemaRef
        """
        return self.probe_inspectors(
            self.field_inspectors, 'field_to_swagger_object', field, {'field_inspectors': self.field_inspectors},
            swagger_object_type=swagger_object_type, use_references=use_references, **kwargs
        )

    def _get_partial_types(self, field, swagger_object_type, use_references, **kwargs):
        """Helper method to extract generic information from a field and return a partial constructor for the
        appropriate openapi object.

        All arguments are the same as :meth:`.field_to_swagger_object`.

        The return value is a tuple consisting of:

        * a function for constructing objects of `swagger_object_type`; its prototype is: ::

            def SwaggerType(existing_object=None, **instance_kwargs):

          This function creates an instance of `swagger_object_type`, passing the following attributes to its init,
          in order of precedence:

            - arguments specified by the ``kwargs`` parameter of :meth:`._get_partial_types`
            - ``instance_kwargs`` passed to the constructor function
            - ``title``, ``description``, ``required`` and ``default`` inferred from the field,
              where appropriate

          If ``existing_object`` is not ``None``, it is updated instead of creating a new object.

        * a type that should be used for child objects if `field` is of an array type. This can currently have two
          values:

            - :class:`.Schema` if `swagger_object_type` is :class:`.Schema`
            - :class:`.Items` if `swagger_object_type` is  :class:`.Parameter` or :class:`.Items`

        :rtype: tuple[callable,(type[openapi.Schema],type[openapi.Items])]
        """
        assert swagger_object_type in (openapi.Schema, openapi.Parameter, openapi.Items)
        assert not isinstance(field, openapi.SwaggerDict), "passed field is already a SwaggerDict object"
        title = force_real_str(field.label) if field.label else None
        title = title if swagger_object_type == openapi.Schema else None  # only Schema has title
        description = force_real_str(field.help_text) if field.help_text else None
        description = description if swagger_object_type != openapi.Items else None  # Items has no description either

        def SwaggerType(existing_object=None, **instance_kwargs):
            if 'required' not in instance_kwargs and swagger_object_type == openapi.Parameter:
                instance_kwargs['required'] = field.required

            if 'default' not in instance_kwargs and swagger_object_type != openapi.Items:
                default = get_field_default(field)
                if default not in (None, serializers.empty):
                    instance_kwargs['default'] = default

            if instance_kwargs.get('type', None) != openapi.TYPE_ARRAY:
                instance_kwargs.setdefault('title', title)
            if description is not None:
                instance_kwargs.setdefault('description', description)
            instance_kwargs.update(kwargs)

            if existing_object is not None:
                assert isinstance(existing_object, swagger_object_type)
                for key, val in sorted(instance_kwargs.items()):
                    setattr(existing_object, key, val)
                result = existing_object
            else:
                result = swagger_object_type(**instance_kwargs)

            # Provide an option to add manual paremeters to a schema
            # for example, to add examples
            if swagger_object_type == openapi.Schema:
                self.add_manual_fields(field, result)
            return result

        # arrays in Schema have Schema elements, arrays in Parameter and Items have Items elements
        child_swagger_type = openapi.Schema if swagger_object_type == openapi.Schema else openapi.Items
        return SwaggerType, child_swagger_type


class SerializerInspector(FieldInspector):
    def get_schema(self, serializer):
        """Convert a DRF Serializer instance to an :class:`.openapi.Schema`.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `serializer`.

        :param serializers.BaseSerializer serializer: the ``Serializer`` instance
        :rtype: openapi.Schema
        """
        return NotHandled

    def get_request_parameters(self, serializer, in_):
        """Convert a DRF serializer into a list of :class:`.Parameter`\ s.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `serializer`.

        :param serializers.BaseSerializer serializer: the ``Serializer`` instance
        :param str in_: the location of the parameters, one of the `openapi.IN_*` constants
        :rtype: list[openapi.Parameter]
        """
        return NotHandled


class ViewInspector(BaseInspector):
    body_methods = ('PUT', 'PATCH', 'POST', 'DELETE')  #: methods that are allowed to have a request body

    #: methods that are assumed to require a request body determined by the view's ``serializer_class``
    implicit_body_methods = ('PUT', 'PATCH', 'POST')

    # real values set in __init__ to prevent import errors
    field_inspectors = []  #:
    filter_inspectors = []  #:
    paginator_inspectors = []  #:

    def __init__(self, view, path, method, components, request, overrides):
        """
        Inspector class responsible for providing :class:`.Operation` definitions given a view, path and method.

        :param dict overrides: manual overrides as passed to :func:`@swagger_auto_schema <.swagger_auto_schema>`
        """
        super(ViewInspector, self).__init__(view, path, method, components, request)
        self.overrides = overrides
        self._prepend_inspector_overrides('field_inspectors')
        self._prepend_inspector_overrides('filter_inspectors')
        self._prepend_inspector_overrides('paginator_inspectors')

    def _prepend_inspector_overrides(self, inspectors):
        extra_inspectors = self.overrides.get(inspectors, None)
        if extra_inspectors:
            default_inspectors = [insp for insp in getattr(self, inspectors) if insp not in extra_inspectors]
            setattr(self, inspectors, extra_inspectors + default_inspectors)

    def get_operation(self, operation_keys):
        """Get an :class:`.Operation` for the given API endpoint (path, method).
        This includes query, body parameters and response schemas.

        :param tuple[str] operation_keys: an array of keys describing the hierarchical layout of this view in the API;
          e.g. ``('snippets', 'list')``, ``('snippets', 'retrieve')``, etc.
        :rtype: openapi.Operation
        """
        raise NotImplementedError("ViewInspector must implement get_operation()!")

    # methods below provided as default implementations for probing inspectors

    def should_filter(self):
        """Determine whether filter backend parameters should be included for this request.

        :rtype: bool
        """
        if not getattr(self.view, 'filter_backends', None):
            return False

        if self.method.lower() not in ["get", "delete"]:
            return False

        return is_list_view(self.path, self.method, self.view)

    def get_filter_parameters(self):
        """Return the parameters added to the view by its filter backends.

        :rtype: list[openapi.Parameter]
        """
        if not self.should_filter():
            return []

        fields = []
        for filter_backend in self.view.filter_backends:
            fields += self.probe_inspectors(self.filter_inspectors, 'get_filter_parameters', filter_backend()) or []

        return fields

    def should_page(self):
        """Determine whether paging parameters and structure should be added to this operation's request and response.

        :rtype: bool
        """
        if not getattr(self.view, 'paginator', None):
            return False

        if self.method.lower() != 'get':
            return False

        return is_list_view(self.path, self.method, self.view)

    def get_pagination_parameters(self):
        """Return the parameters added to the view by its paginator.

        :rtype: list[openapi.Parameter]
        """
        if not self.should_page():
            return []

        return self.probe_inspectors(self.paginator_inspectors, 'get_paginator_parameters', self.view.paginator) or []

    def serializer_to_schema(self, serializer):
        """Convert a serializer to an OpenAPI :class:`.Schema`.

        :param serializers.BaseSerializer serializer: the ``Serializer`` instance
        :returns: the converted :class:`.Schema`, or ``None`` in case of an unknown serializer
        :rtype: openapi.Schema,openapi.SchemaRef
        """
        return self.probe_inspectors(
            self.field_inspectors, 'get_schema', serializer, {'field_inspectors': self.field_inspectors}
        )

    def serializer_to_parameters(self, serializer, in_):
        """Convert a serializer to a possibly empty list of :class:`.Parameter`\ s.

        :param serializers.BaseSerializer serializer: the ``Serializer`` instance
        :param str in_: the location of the parameters, one of the `openapi.IN_*` constants
        :rtype: list[openapi.Parameter]
        """
        return self.probe_inspectors(
            self.field_inspectors, 'get_request_parameters', serializer, {'field_inspectors': self.field_inspectors},
            in_=in_
        ) or []

    def get_paginated_response(self, response_schema):
        """Add appropriate paging fields to a response :class:`.Schema`.

        :param openapi.Schema response_schema: the response schema that must be paged.
        :returns: the paginated response class:`.Schema`, or ``None`` in case of an unknown pagination scheme
        :rtype: openapi.Schema
        """
        return self.probe_inspectors(self.paginator_inspectors, 'get_paginated_response',
                                     self.view.paginator, response_schema=response_schema)
