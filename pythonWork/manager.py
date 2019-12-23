# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import room,reserve
import uuid
from django.forms.models import model_to_dict

def GetRoom(request):#不需要传入信息，直接读取所有房间信息并返回
    status = 200

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
                "text" : text,
                "ID" : ID
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
    #传入会议室的ID、修改后room的condition，0代表拒绝,1代表同意,reserveID，并根据reserveID寻找对应的reserve，修改对应reserve的condition
    status = 200
    text = '处理预定' 
    data = request.POST

    changeRoom = room.objects.get(ID=data['roomID'])
    changeRoom.condition = data['condition']

    reserveRecord = reserve.objects.get(ID=data['reserveID'])

    message = ''
    if data['condition'] == '0':
        reserveRecord.condition = 3
        changeRoom.reserveInfo = ''
        text = '拒绝预订'
        message = '您的预订被拒绝'
    else:
        reserveRecord.condition = 1
        text = '同意预定'
        message = '您已成功预订:' + changeRoom.place

    sendEmail(reserveRecord.email,message)#发送邮件提示

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
    #传入会议室的ID、修改room的condition=0,删除reserve记录
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

    sendEmail(reserveRecord.email,'管理员已为你撤回预定')#发送邮件提示

    return JsonResponse({
                "status" : status,
                "text" : text
            })

import smtplib
from email.mime.text import MIMEText
from email.header import Header
def sendEmail(email,text): #发送邮件
    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="545436317@qq.com"    #用户名
    mail_pass="bcmvluovmjrabbag"   #口令 
    sender = '545436317@qq.com'
    
    receivers = email  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(text,'plain') #邮件内容

    message['From'] = Header("会议室预订系统") #发件人
    message['To'] =  Header(email) #收件人

    message['Subject'] = Header('会议室预订系统-预订提醒')#邮件标题
      
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
    except smtplib.SMTPException:
        print('发送邮件失败') 
    print('发送成功') 
