# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import user,manager
import uuid

def GetRoom(request):#不传入信息，直接读取condition=0的所以会议室
    status = 200
    text = '获取' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def ReserveRoom(request):
    #传入roomInfo,reserveInfo,生成随机ID，并向reserveInfo添加reserveID属性，之后将两个数据存储，最后将reserveID返回
    status = 200
    text = '预定' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def WithdrawReserve(request):
    #传入会议室ID，和resereveInfo,修改会议室的condition,并根据reserveInfo里的reserveID删除reserve中对应ID的元素
    status = 200
    text = '取消预定' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def BackRoom(request):
    #传入会议室ID，和resereveInfo,修改会议室的condition,并根据reserveInfo里的reserveID修改reserve中condition
    status = 200
    text = '归还会议室' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })