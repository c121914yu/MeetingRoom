# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid,json
from django.forms.models import model_to_dict

def GetInfo(request):#不传入信息，直接读取condition=0的所以会议室
    status = 200
    data = request.POST
    email = data['email']

    rooms = list(room.objects.filter(condition=0))
    for i in range(len(rooms)): 
        ID = rooms[i].ID
        rooms[i] = model_to_dict(rooms[i])
        rooms[i]['ID'] = ID

    reserveRecord = list(reserve.objects.filter(email=email))
    for i in range(len(reserveRecord)):
        ID = reserveRecord[i].ID
        reserveRecord[i] = model_to_dict(reserveRecord[i])
        reserveRecord[i]['ID'] = ID
    reserveRecord = sorted(reserveRecord,key=lambda e: e.__getitem__('condition'))
    
    return JsonResponse({
                "status" : status,
                "rooms" : rooms,
                "reserveRecord" : reserveRecord
            })

def ReserveRoom(request):
    #传入roomInfo,reserveInfo,生成随机ID，并向reserveInfo添加reserveID属性，之后将两个数据存储，最后将reserveID返回
    status = 200
    text = '' 

    data = request.POST
    ID = uuid.uuid4()
    reserveInfo = json.loads(data['reserveInfo'])
    reserveInfo['reserveID'] = str(ID)
    reserveInfo = json.dumps(reserveInfo)

    roomInfo = json.loads(data['roomInfo'])
    roomID = roomInfo['ID']
    changeRoom = room.objects.get(ID=roomID)
    changeRoom.condition = 1
    changeRoom.reserveInfo = reserveInfo
    changeRoom.save()
 
    db = reserve(
        ID = ID,
        roomInfo = data['roomInfo'],
        email = data['email'],
        reserveInfo = reserveInfo
    )
    result = db.save()
    if result != None:
        status = 400
        text = '预订失败'
    else:
        text = '预订成功'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def WithdrawReserve(request):
    #传入会议室ID，和resereveID,修改会议室的condition=0,并根据reserveID删除reserve中对应ID的元素
    status = 200
    text = '取消预定成功' 
    data = request.POST

    changeRoom = room.objects.get(ID=data['roomID'])
    changeRoom.condition = 0
    changeRoom.reserveInfo = ''
    result = changeRoom.save()
    if result != None:
        status = 400
        text = '取消失败'

    reserveRecord = reserve.objects.get(ID=data['reserveID'])
    reserveRecord.delete()

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def BackRoom(request):
    #传入roomID，和resereveInfo,修改会议室的condition,并根据reserveInfo里的reserveID修改reserve中condition
    status = 200
    text = '归还会议室成功' 
    data = request.POST

    changeRoom = room.objects.get(ID=data['roomID'])
    changeRoom.condition = 0
    changeRoom.reserveInfo = ''
    reserveRecord = reserve.objects.get(ID=data['reserveID'])
    reserveRecord.condition = 2

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