# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid
from django.forms.models import model_to_dict

def GetRoom(request):#不需要传入信息，直接读取所有房间信息并返回
    status = 200
    text = '获取' 
    rooms = []

    data = request.POST
    list = room.objects.all()

    for i in list:
        ID1 = i.ID
        room1 = model_to_dict(i)
        room1.update({"ID":ID1})
        rooms.append(room1)

    return JsonResponse({
                "status" : status,
                "rooms" : rooms
            })

def AddRoom(request): #添加会议室
    status = 200
    text = ''
    data=request.POST
    ID=uuid.uuid4()
    db=room(
        ID=ID,
        place=data['place'],
        maxPeople=data['maxPeople'],
        introduction=data['introduction'],
    )
    result=db.save() 
    print(data)
    if result == None:
        text='添加成功'
    else:
        status=400
        text='请求失败'


    return JsonResponse({
                "status":status,
                "text":text
            })

def ChangeRoom(request):#传入会议室的ID、修改后的信息（place,maxPeople,introduction），返回修改结果
    status = 200
    text = '' 

    data = request.POST
    ID1 = data['ID']
    place1 = data['place']
    maxPeople1 = data['maxPeople']
    introduction1 = data['introduction']

    room1 = room.objects.get(ID=ID1)
    room1.place = place1
    room1.maxPeople = maxPeople1
    room1.introduction = introduction1
    result = room1.save()

    if result == None:
        text = '修改成功'
    else:
        status = 400
        text = '修改失败'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def RemoveRoom(request):#传入会议室的ID，返回处理结果
    status = 200
    text = '删除成功' 

    data = request.POST
    ID1 = data['ID']
    room1 = room.objects.get(ID=ID1)
    room1.delete()
    

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def DealReserve(request):
    #传入roomID、修改后的condition，传入reserveID修改对应reserve的contion
    status = 200
    text = '处理预定'
    data=request.POST
    id=data['roomID']
    list=room.objects.get(ID=id)
    list.condition=data['condition']
    list.save()
    list1=reserve.objects.get(ID=data['reserveID'])
    if(list.condition==0):
        list1.condition=-1
    elif (list.condition==1):
        list1.condition=0
    elif(list.condition==2):
        list1.condition=1
    list1.save()
    text="处理成功"
    

    return JsonResponse({
                "status" : status,
                "text" : text
            })
def WithdrawRoom(request):
    #传入roomID和reserveID，修改room的condition=0,清空reserveInfo.删除reserve
    status = 200
    text = '撤回预定成功' 
    data=request.POST
    bb=room.objects.get(ID=data['roomID'])
    bb.condition=0
    bb.reserveInfo=0
    bb.save()
    return JsonResponse({
                "status" : status,
                "text" : text
            })
