from __future__ import unicode_literals

from audit_tools.audit.forms.api import AccessFilterForm
from audit_tools.audit.models import Access, Process
from audit_tools.audit.models.serializers import AccessSerializer
from audit_tools.audit.views.api.base import APIViewSet

__all__ = ['AccessViewSet']


class AccessViewSet(APIViewSet):
    form_class = {
        'GET': AccessFilterForm,
        'POST': None,
        'PUT': None,
        'DELETE': None,
        'PATCH': None,
    }
    model = Access
    serializer_class = AccessSerializer
    paginate_by = 10
    order_by = '-time__request'

    def _filter_date(self, date_from=None, date_to=None):
        """
        Filter QuerySet using a range of dates.

        :param date_from: If given, a filter excluding previous data will be done.
        :type date_from: :class:`datetime.datetime`
        :param date_to: If given, a filter excluding next data will be done.
        :type date_to: :class:`datetime.datetime`
        :return: QuerySet filtered.
        :rtype: Mongoengine QuerySet.
        """
        if date_from:
            self.queryset = self.queryset.filter(
                time__request__gte=date_from,
            )

        if date_to:
            self.queryset = self.queryset.filter(
                time__request__lte=date_to,
            )

        return self.queryset

    def _filter_user(self, user_id=None):
        if user_id:
            self.queryset = self.queryset.filter(
                user__id=user_id,
            )

        return self.queryset

    def _filter_url(self, url=None):
        if url:
            self.queryset = self.queryset.filter(
                request__path__icontains=url,
            )

        return self.queryset

    def _filter_view(self, view_app=None, view_name=None):
        if view_app:
            self.queryset = self.queryset.filter(
                view__app=view_app,
            )

        if view_name:
            self.queryset = self.queryset.filter(
                view__name=view_name,
            )

        return self.queryset

    def _filter_interlink(self, interlink_id=None):
        if interlink_id:
            self.queryset = self.queryset.filter(
                interlink_id=interlink_id,
            )

        return self.queryset

    def _filter_by_processes(self, interlink_id=None):
        processes = Process.objects.all()
        if interlink_id:
            processes = processes.filter(interlink_id=interlink_id)

        self.queryset = self.queryset.filter(process__in=processes)

        return self.queryset

    def filter_query(self, filter_form):
        # Filter by date range
        date_from = filter_form.cleaned_data.get('date_from', None)
        date_to = filter_form.cleaned_data.get('date_to', None)
        self._filter_date(date_from, date_to)

        # Filter by user
        user_id = filter_form.cleaned_data.get('user_id', None)
        self._filter_user(user_id)

        # Filter by url
        url = filter_form.cleaned_data.get('url', None)
        self._filter_url(url)

        # Filter by view
        view_app = filter_form.cleaned_data.get('method_app', None)
        view_name = filter_form.cleaned_data.get('method_name', None)
        self._filter_view(view_app, view_name)

        # Filter by interlink access
        interlink_access = filter_form.cleaned_data.get('interlink_access', None)
        self._filter_interlink(interlink_access)

        # Filter by interlink process
        interlink_process = filter_form.cleaned_data.get('interlink_process', None)
        self._filter_by_processes(interlink_process)
