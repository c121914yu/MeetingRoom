# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid

def GetRoom(request):#不需要传入信息，直接读取所有房间信息并返回
    status = 200
    text = '获取' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def AddRoom(request): #添加会议室
    status = 200
    text = '' 
    data = request.POST

    ID = uuid.uuid4()
    db = room(
        ID = ID,
        place = data['place'],
        maxPeople = data['maxPeople'],
        introduction = data['introduction'],
    )
    result = db.save()
    if result == None:
        text = '添加成功'
    else:
        status = 400
        text = '请求失败'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def ChangeRoom(request):#传入会议室的ID、修改后的信息（place,maxPeople,introduction），返回修改结果
    status = 200
    text = '修改' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def RemoveRoom(request):#传入会议室的ID，返回处理结果
    status = 200
    text = '删除' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def DealReserve(request):
    #传入会议室的ID、修改后的condition，reserveInfo，修改数据库中会议室的condition，并根据reserver中分reserveID寻找对应的reserve，修改对应reserve的contion
    status = 200
    text = '处理预定' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def WithdrawRoom(request):
    #传入会议室的ID、修改后的condition，reserveInfo，修改数据库中会议室的condition，并根据reserver中分reserveID寻找对应的reserve，修改对应reserve的contion
    status = 200
    text = '撤回预定' 

    return JsonResponse({
                "status" : status,
                "text" : text
            })