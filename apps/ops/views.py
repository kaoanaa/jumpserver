# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
import time
from datetime import datetime

from django.utils.translation import ugettext as _
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.shortcuts import redirect, reverse

from common.mixins import DatetimeSearchMixin
from .models import Task, AdHoc, AdHocRunHistory
from ops.tasks import rerun_task


class TaskListView(DatetimeSearchMixin, ListView):
    paginate_by = settings.CONFIG.DISPLAY_PER_PAGE
    model = Task
    ordering = ('-date_created',)
    context_object_name = 'task_list'
    template_name = 'ops/task_list.html'
    date_format = '%m/%d/%Y'
    keyword = ''

    def get_queryset(self):
        self.queryset = super().get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        self.queryset = self.queryset.filter(
            date_created__gt=self.date_from,
            date_created__lt=self.date_to
        )

        if self.keyword:
            self.queryset = self.queryset.filter(
                name__icontains=self.keyword,
            )
        return self.queryset

    def get_context_data(self, **kwargs):
        print(self.date_from)
        context = {
            'app': 'Ops',
            'action': _('Task list'),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'keyword': self.keyword,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'ops/task_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Ops',
            'action': 'Task detail',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskAdhocView(DetailView):
    model = Task
    template_name = 'ops/task_adhoc.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Ops',
            'action': 'Task versions',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskHistoryView(DetailView):
    model = Task
    template_name = 'ops/task_history.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Ops',
            'action': 'Task run history',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskRunView(View):
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        rerun_task.delay(pk)
        time.sleep(0.5)
        return redirect(reverse('ops:task-detail', kwargs={'pk': pk}))


class AdHocDetailView(DetailView):
    model = AdHoc
    template_name = 'ops/adhoc_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Ops',
            'action': 'Task version detail',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdHocHistoryView(DetailView):
    model = AdHoc
    template_name = 'ops/adhoc_history.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Ops',
            'action': 'Version run history',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdHocHistoryDetailView(DetailView):
    model = AdHocRunHistory
    template_name = 'ops/adhoc_history_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Ops',
            'action': 'Run history detail',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)