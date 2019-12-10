# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid,json
from django.forms.models import model_to_dict

def GetInfo(request):#传入email,读取condition=0的房间，跟符合email的record
    status = 200
    rooms1=list(room.objects.filter(condition=0))
    for i in range(len(rooms1)):
        id=room.objects.all()[i].ID
        rooms1[i]=model_to_dict(rooms1[i])
        rooms1[i].update({"ID":id})

    return JsonResponse({
                "status" : status,
                "rooms" : rooms1,
                # "reserveRecord" : reserveRecord
            })

def ReserveRoom(request):
    #传入roomInfo,reserveInfo,生成随机ID，并向reserveInfo添加reserveID属性，之后将两个数据存储，最后将reserveID返回
    status = 200
    data=request.POST

    reserveID=uuid.uuid4()

    reserveinfo1= json.loads(data['reserveInfo'])

    reserveinfo1.update({"reserveID":str(reserveID)})
    #没改room的condition
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
    #传入会议室ID，和resereveInfo,修改会议室的condition=0,并根据reserveInfo里的reserveID删除reserve中对应ID的元素
    status = 200
    data=request.POST
    reserveinfo=data['reserveInfo']
    ID=data['ID']
    try:
        reserve.objects.get(ID=ID)
        # 判断reserve里是否存在该reserveInfo
        # if db != None:
        text = '处理成功'
        # reserveinfo=room.objects.filter(ID=ID).get(reserveInfo)
        room.objects.filter(ID=ID).update(condition=0)
        reserve.objects.filter(reserveInfo=reserveinfo).delete()
        # db = reserve.objects.get(reserveInfo=reserveinfo)
        # db.delete()
    

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