# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid
from django.forms.models import model_to_dict

def GetRoom(request):#不需要传入信息，直接读取所有房间信息并返回
    status = 200
    text = '获取' 

    rooms = list(room.objects.all())
    for i in range(len(rooms)): 
        ID = rooms[i].ID
        rooms[i] = model_to_dict(rooms[i])
        rooms[i]['ID'] = ID
    rooms = sorted(rooms,key=lambda e: e.__getitem__('condition'))

    return JsonResponse({
                "status" : status,
                "rooms" : rooms
            })

def AddRoom(request): #添加会议室，传入place,maxPeople,introduction
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
    text = '' 

    data = request.POST
    changeRoom = room.objects.get(ID=data['ID'])
    changeRoom.place = data['place']
    changeRoom.maxPeople = data['maxPeople']
    changeRoom.introduction = data['introduction']
    save = changeRoom.save()
    if save != None:
        status = 400
        text = '修改失败'
    else:
        text = '修改成功'
    return JsonResponse({
                "status" : status,
                "text" : text
            })

def RemoveRoom(request):#传入会议室的ID，返回处理结果
    status = 200
    text = '删除成功' 

    data = request.POST
    changeRoom = room.objects.get(ID=data['ID'])
    changeRoom.delete()
    return JsonResponse({
                "status" : status,
                "text" : text
            })

def DealReserve(request):
    #传入会议室的ID、修改后的condition，reserveInfo，修改数据库中会议室的condition，并根据reserver中分reserveID寻找对应的reserve，修改对应reserve的contion
    status = 200
    text = '处理预定' 
    data = request.POST

    changeRoom = room.objects.get(ID=data['roomID'])
    changeRoom.condition = data['condition']

    reserveRecord = reserve.objects.get(ID=data['reserveID'])
    print(data['condition'])
    if data['condition'] == '0':
        reserveRecord.condition = -1
        changeRoom.reserveInfo = ''
        text = '拒绝预订'
    else:
        reserveRecord.condition = 1
        text = '同意预定'

    result = changeRoom.save()
    if result != None:
        status = 400
        text = '网络错误'

    result = reserveRecord.save()
    if result != None:
        status = 400
        text = '网络错误'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def WithdrawRoom(request):
    #传入会议室的ID、修改后的condition，reserveInfo，修改数据库中会议室的condition，并根据reserver中分reserveID寻找对应的reserve，修改对应reserve的contion
    status = 200
    text = '撤回预定成功' 
    data = request.POST

    changeRoom = room.objects.get(ID=data['roomID'])
    changeRoom.condition = 0
    changeRoom.reserveInfo = ''
    result = changeRoom.save()
    if result != None:
        status = 400
        text = '网络错误'

    reserveRecord = reserve.objects.get(ID=data['reserveID'])
    reserveRecord.delete()

    return JsonResponse({
                "status" : status,
                "text" : text
            })