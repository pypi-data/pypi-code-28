from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from urllib.parse import urlencode, unquote

from ..models import SubjectScheduleHistory

register = template.Library()


@register.inclusion_tag('edc_visit_schedule/subject_schedule_footer_row.html')
def subject_schedule_footer_row(subject_identifier, visit_schedule, schedule,
                                subject_dashboard_url):

    context = {}
    try:
        history_obj = SubjectScheduleHistory.objects.get(
            visit_schedule_name=visit_schedule.name,
            schedule_name=schedule.name,
            subject_identifier=subject_identifier,
            offschedule_datetime__isnull=False)
    except ObjectDoesNotExist:
        onschedule_model_obj = schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier)
        options = dict(subject_identifier=subject_identifier)
        query = unquote(urlencode(options))
        href = (f'{schedule.offschedule_model_cls().get_absolute_url()}?next='
                f'{subject_dashboard_url},subject_identifier')
        href = '&'.join([href, query])
        context = dict(
            offschedule_datetime=None,
            onschedule_datetime=onschedule_model_obj.onschedule_datetime,
            href=mark_safe(href))
    else:
        onschedule_model_obj = schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier)
        offschedule_model_obj = schedule.offschedule_model_cls.objects.get(
            subject_identifier=subject_identifier)
        options = dict(subject_identifier=subject_identifier)
        query = unquote(urlencode(options))
        href = (f'{offschedule_model_obj.get_absolute_url()}?next='
                f'{subject_dashboard_url},subject_identifier')
        href = '&'.join([href, query])
        context = dict(
            offschedule_datetime=history_obj.offschedule_datetime,
            onschedule_datetime=onschedule_model_obj.onschedule_datetime,
            href=mark_safe(href))
    context.update(
        visit_schedule=visit_schedule,
        schedule=schedule,
        verbose_name=schedule.offschedule_model_cls._meta.verbose_name)
    return context
