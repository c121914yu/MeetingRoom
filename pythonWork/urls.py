from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import server

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^test/$', server.test),
]
