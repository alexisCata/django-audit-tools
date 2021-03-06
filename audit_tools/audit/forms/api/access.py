from __future__ import unicode_literals

from django import forms

__all__ = ['AccessFilterForm']


class AccessFilterForm(forms.Form):
    date_from = forms.SplitDateTimeField(required=False, input_date_formats=['%d/%m/%Y'])
    date_to = forms.SplitDateTimeField(required=False, input_date_formats=['%d/%m/%Y'])
    user_id = forms.IntegerField(required=False)
    url = forms.CharField(required=False)
    method_name = forms.CharField(required=False)
    method_app = forms.CharField(required=False)
    instance_id = forms.CharField(required=False)
    interlink_access = forms.CharField(required=False)
    interlink_process = forms.CharField(required=False)
