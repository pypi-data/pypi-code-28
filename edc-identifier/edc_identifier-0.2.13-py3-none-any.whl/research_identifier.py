from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from string import Formatter

from .checkdigit_mixins import LuhnMixin
from .exceptions import IdentifierError
from .models import IdentifierModel


class IdentifierMissingTemplateValue(Exception):
    pass


class ResearchIdentifier:

    label = None  # e.g. subject_identifier, plot_identifier, etc
    identifier_type = None  # e.g. 'subject', 'infant', 'plot', a.k.a subject_type
    template = None
    padding = 5
    checkdigit = LuhnMixin()
    identifier_model_cls = IdentifierModel

    def __init__(self, identifier_type=None, template=None,
                 device_id=None, protocol_number=None, site=None,
                 requesting_model=None, identifier=None):

        self._identifier = None
        self.requesting_model = requesting_model
        if not self.requesting_model:
            raise IdentifierError('Invalid requesting_model. Got None')
        self.identifier_type = identifier_type or self.identifier_type
        if not self.identifier_type:
            raise IdentifierError('Invalid identifier_type. Got None')
        self.template = template or self.template
        app_config = django_apps.get_app_config('edc_device')
        self.device_id = device_id or app_config.device_id
        app_config = django_apps.get_app_config('edc_protocol')
        self.protocol_number = protocol_number or app_config.protocol_number
        self.site = site or Site.objects.get_current()
        if identifier:
            # load an existing identifier
            self.identifier_model = self.identifier_model_cls.objects.get(
                identifier=identifier)
            self._identifier = self.identifier_model.identifier
            self.subject_type = self.identifier_model.subject_type
            self.site = self.identifier_model.site
        self.identifier

    def __repr__(self):
        return f'{self.__class__.__name__}({self.label})'

    def __str__(self):
        return self.identifier

    @property
    def identifier(self):
        """Returns a new and unique identifier and updates
        the IdentifierModel.
        """
        if not self._identifier:
            self.pre_identifier()
            self._identifier = self.template.format(**self.template_opts)
            check_digit = self.checkdigit.calculate_checkdigit(
                ''.join(self._identifier.split('-')))
            self._identifier = f'{self._identifier}-{check_digit}'
            self.identifier_model = self.identifier_model_cls.objects.create(
                name=self.label,
                sequence_number=self.sequence_number,
                identifier=self._identifier,
                protocol_number=self.protocol_number,
                device_id=self.device_id,
                model=self.requesting_model,
                site=self.site,
                identifier_type=self.identifier_type)
            self.post_identifier()
        return self._identifier

    def pre_identifier(self):
        pass

    def post_identifier(self):
        pass

    @property
    def template_opts(self):
        """Returns the template key/values, if a key from the template
        does not exist raises an exception.
        """
        template_opts = {}
        formatter = Formatter()
        keys = [opt[1] for opt in formatter.parse(
            self.template) if opt[1] not in ['sequence']]
        template_opts.update(
            sequence=str(self.sequence_number).rjust(self.padding, '0'))
        for key in keys:
            try:
                value = getattr(self, key)
            except AttributeError:
                raise IdentifierMissingTemplateValue(
                    f'Required option not provided. Got \'{key}\'.')
            else:
                if value:
                    template_opts.update({key: value})
                else:
                    raise IdentifierMissingTemplateValue(
                        f'Required option cannot be None. Got \'{key}\'.')
        return template_opts

    @property
    def site_id(self):
        return str(self.site.pk)

    @property
    def sequence_number(self):
        """Returns the next sequence number to use.
        """
        try:
            identifier_model = IdentifierModel.objects.filter(
                name=self.label,
                device_id=self.device_id,
                site=self.site).order_by('-sequence_number').first()
            sequence_number = identifier_model.sequence_number + 1
        except AttributeError:
            sequence_number = 1
        return sequence_number
