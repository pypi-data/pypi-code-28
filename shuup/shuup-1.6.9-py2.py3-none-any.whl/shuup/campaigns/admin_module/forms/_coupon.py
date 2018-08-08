# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from shuup.campaigns.models.campaigns import Coupon


class CouponForm(forms.ModelForm):
    autogenerate = forms.BooleanField(label=_("Autogenerate code"), required=False)

    class Meta:
        model = Coupon
        fields = [
            'code',
            'usage_limit_customer',
            'usage_limit',
            'active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super(CouponForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.has_been_used():
            self.fields["code"].readonly = True

        if self.request.GET.get("mode") == "iframe":
            self.fields["active"].disabled = True
            self.fields["active"].widget.disabled = True

    def clean_code(self):
        code = self.cleaned_data["code"]
        qs = Coupon.objects.filter(code=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(_("Discount Code already in use."))
        return code
