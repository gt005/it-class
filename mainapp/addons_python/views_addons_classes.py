from django.views.generic.base import View
from ..models import Events, Puples


class HeaderNotificationsCounter(View):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_new'] = Events.objects.filter(check=False).count()
        context['applicants_count'] = Puples.objects.filter(
            status="APP").count()
        return context