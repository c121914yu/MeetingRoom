# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid,json
from django.forms.models import model_to_dict

def GetInfo(request):#不传入信息，直接读取condition=0的所有会议室
    status = 200
    data=request.POST
    reservecord=list(reserve.objects.filter(email=data['email']))
    for i in range(len(reservecord)):
        id=reserve.objects.all()[i].ID
        reservecord[i]=model_to_dict(reservecord[i])
        reservecord[i].update({"ID":id})

    rooms=list(room.objects.filter(condition=0))
    for i in range(len(rooms)):
        id=room.objects.all()[i].ID
        rooms[i]=model_to_dict(rooms[i])
        rooms[i].update({"ID":id})
   
    return JsonResponse({
                "status" : status,
                "rooms" : rooms,
                "reserveRecord":reservecord
            })

def ReserveRoom(request):
    #传入roomInfo,reserveInfo,生成随机ID，并向reserveInfo添加reserveID属性，之后将两个数据存储，最后将reserveID返回
    status = 200
    text = ''
    data=request.POST

    reserveID=uuid.uuid4()

    reserveinfo1= json.loads(data['reserveInfo'])
    reserveinfo1.update({"reserveID":str(reserveID)})
    reserveinfo1 = json.dumps(reserveinfo1)

    roomInfo = json.loads(data['roomInfo'])
    ID = roomInfo["ID"]

    #修改不成功，，再想room添加reserveInfo
    room.objects.filter(ID=ID).update(condition=1)

    db=reserve(
        ID=reserveID,
        roomInfo=data['roomInfo'],
        reserveInfo=reserveinfo1,
        email=data['email'],
        condition=0
    )
    result=db.save() 
    
    if result == None:
        text='添加成功'
    else:
        status=400
        text='请求失败'
    return JsonResponse({
                "status" : status,
                "text" : text,
                "reserveID": reserveID
            })

def WithdrawReserve(request):
    #传入roomID，和resereveID,修改会议室的condition=0,并根据reserveID删除reserve中对应ID的元素
    status = 200
    data=request.POST
    reserveinfo=data['reserveID']
    ID=data['roomID']
    try:
        reserve.objects.get(ID=ID)
        room.objects.filter(ID=ID).update(condition=0)
        reserve.objects.filter(reserveInfo=reserveinfo).delete()
        status = 200
        text = '处理成功'

    except:
        status = 400
        text = '处理失败'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def BackRoom(request):
    #传入会议室ID，和resereveID,修改会议室的condition=0,并根据reserveID修改reserve中condition=2
    status = 200
    data=request.POST
    reserveinfo=data['reserveInfo']
    ID=data['ID']
    try:
        db = reserve.objects.get(ID=ID)
        text = '处理成功'
        room.objects.filter(ID=ID).update(condition=0)
        reserve.objects.filter(reserveInfo=reserveinfo).update(condition=2)
    except:
        status = 400
        text = '处理失败'
    return JsonResponse({
                "status" : status,
                "text" : text
            })