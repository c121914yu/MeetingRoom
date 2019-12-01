# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import user,manager,reserve

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'^MeetingRoom/user/managerLogin$', user.managerLogin),
    url(r'^MeetingRoom/user/managerRegister$', user.managerRegister),

    url(r'^MeetingRoom/user/login$', user.login),
    url(r'^MeetingRoom/user/findpsw$', user.findpsw),
    url(r'^MeetingRoom/user/register$', user.register),
    url(r'^MeetingRoom/user/sendEmail$', user.sendEmail),
    url(r'^MeetingRoom/user/verifyUser$', user.verifyUser),#检测登录是否过期

    #管理会议室
    url(r'^MeetingRoom/manage/GetRoom$', manager.GetRoom),
    url(r'^MeetingRoom/manage/AddRoom$', manager.AddRoom),
    url(r'^MeetingRoom/manage/ChangeRoom$', manager.ChangeRoom),
    url(r'^MeetingRoom/manage/RemoveRoom$', manager.RemoveRoom),
    url(r'^MeetingRoom/manage/DealReserve$', manager.DealReserve),
    url(r'^MeetingRoom/manage/WithdrawRoom$', manager.WithdrawRoom),

    url(r'^MeetingRoom/reserve/GetInfo$', reserve.GetInfo),
    url(r'^MeetingRoom/reserve/ReserveRoom$', reserve.ReserveRoom),
    url(r'^MeetingRoom/reserve/WithdrawReserve$', reserve.WithdrawReserve),
    url(r'^MeetingRoom/reserve/BackRoom$', reserve.BackRoom),
]
