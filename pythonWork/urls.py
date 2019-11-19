from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import user 

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'^MeetingRoom/user/managerLogin$', user.managerLogin),
    url(r'^MeetingRoom/user/managerRegister$', user.managerRegister),

    url(r'^MeetingRoom/user/login$', user.login),
    url(r'^MeetingRoom/user/findpsw$', user.findpsw),
    url(r'^MeetingRoom/user/register$', user.register),
    url(r'^MeetingRoom/user/sendEmail$', user.sendEmail),

    url(r'^MeetingRoom/user/verifyUser$', user.verifyUser),#检测登录是否过期

]
