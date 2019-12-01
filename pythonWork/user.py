# -*- coding: utf-8 -*-
from django.http import JsonResponse
from MeetingRoom.models import user,manager
import face_recognition
import uuid

def verifyUser(request):#验证用户登录凭证
    status = 200
    text = '' 

    data = request.POST
    email = data["email"]
    dbuser = user.objects.filter(email=email)[0]

    if dbuser.ID == data["ID"]:
        status = 200
        text = '登录成功'
    else:
        status = 400
        text = '信息已过期'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def login(request):#用户登录情况
    status = 200
    text = ''

    data = request.POST
    email = data["email"]
    dbuser = user.objects.filter(email=email)

    if len(dbuser) == 0:
        status = 400
        text = '用户不存在'
    else:
        password = data["password"]
        dbpassword = dbuser[0].password
        if password != dbpassword:
            status = 400
            text = '密码错误'
        else:
            return JsonResponse({
                "status" : 200,
                "ID" : dbuser[0].ID,
                "name" : dbuser[0].name
            })

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def findpsw(request):#找回密码
    status = 200
    text = '' 

    data = request.POST
    email = data["email"]
    dbuser = user.objects.filter(email=email)

    if len(dbuser) == 0:
        status = 400
        text = '用户不存在'
    else:
        newpsw = data["password"]
        ID  = uuid.uuid4()
        dbuser = user.objects.get(email=email)
        dbuser.password = newpsw
        dbuser.ID = ID
        dbuser.save()

        status = 200
        text = '密码修改成功'

    return JsonResponse({
                "status" : status,
                "text" : text
            })

def register(request):#用户注册
    status = 200
    text = '' 

    data = request.POST
    email = data["email"]
    dbuser = user.objects.filter(email=email) #根据email筛选数据库信息

    if len(dbuser) > 0:
        status = 400
        text = '用户已存在'
    else:
        ID = uuid.uuid4()
        db = user(
            ID = ID,
            name = data["name"],
            password = data["password"],
            email = data["email"]
        )
        dbctr = db.save()

        if dbctr == None:
            status = 200
            text = ID
        else:
            status = 400,
            text = dbctr

    return JsonResponse({
                "status" : status,
                "text" : text
            })

import random
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendEmail(request): #发送邮件
    # 用户信息
    data = request.POST
    email = data["email"]
    name = data["name"]
    rand = ''
    for i in range(6):
        rand += str(random.randint(1,9))

    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="2979223533@qq.com"    #用户名
    mail_pass="hlrfpzawvuzadcfe"   #口令 
    
    sender = '2979223533@qq.com'
    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('你的验证码为：' + rand, 'plain', 'utf-8') #邮件内容

    message['From'] = Header("会议室预订系统", 'utf-8') #发件人
    message['To'] =  Header(name, 'utf-8') #收件人

    subject = '会议室预订系统-用户注册' #邮件标题
    message['Subject'] = Header(subject, 'utf-8')
      
    status = 200
    text = ''
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        status = 200
        text = rand
    except smtplib.SMTPException:
        status = 400
        text = '发送邮件失败'
    return JsonResponse({
                "status" : status,
                "text" : text
            })

import base64
face_encode = []
def managerRegister(request):#管理员注册
    status = 400
    text = ''

    # 将base64格式照片保存
    data = request.POST
    base = data["base"]
    b64_data = base.split(';base64,')[1]
    with open('test.jpg','wb') as f:
        f.write(base64.b64decode(b64_data))

    image = face_recognition.load_image_file("test.jpg")
    new_face = face_recognition.face_encodings(image)

    if len(new_face) == 0:
        status = 400
        text = '继续录入'
    else:
        global face_encode
        global known_face
        status = 400
        text = '继续录入'

        results = face_recognition.compare_faces(face_encode, new_face[0], tolerance=0.3)
        print(results)
        if False in results:
            face_encode = []
        else:
            face_encode.append(list(new_face[0]))

        if len(face_encode) == 3:
            ID = uuid.uuid4()
            db = manager(
                ID = ID,
                name = data["name"],
                email = data["email"],
                encode = face_encode
            )
            db.save()

            user = {
                "ID" : ID,
                "name" : data["name"],
                "email" : data["email"],
                "encode" : face_encode
            }
            known_face.append(user)
            face_encode = []
            status = 200
            text = '添加成功'

    return JsonResponse({
        "status" : status,
        "text" : text
    })

last_image = face_recognition.load_image_file("test.jpg")
last_face = face_recognition.face_encodings(last_image)
def managerLogin(request):#管理员登录
    status = 400
    text = ''

    # 将base64格式照片保存
    data = request.POST
    base = data["base"]
    b64_data = base.split(';base64,')[1]
    with open('test.jpg','wb') as f:
        f.write(base64.b64decode(b64_data))
    # 要识别的图片
    unknown_image = face_recognition.load_image_file("test.jpg")
    unknown_face = face_recognition.face_encodings(unknown_image)

    if len(unknown_face) == 0:
        status = 400
        text = '识别失败'
    else:#与已经知道的脸部信息对比
        global last_face #与上一张照片比较，如果相似度太高认为是静态照片
        results = face_recognition.compare_faces(last_face,unknown_face[0],tolerance=0.2)
        last_face = unknown_face 
        if results[0]:
            status = 400
            text = '同一张照片'
        else:
            for face in known_face:
                results = face_recognition.compare_faces(face['encode'],unknown_face[0],tolerance=0.3)
                if True in results:
                    return JsonResponse({
                            "status" : 200,
                            "name" : face['name'],
                            "email" : face['email'],
                            "ID" : face['ID']
                        }) 
                else:
                    status = 400
                    text = '识别失败' 
    return JsonResponse({
        "status" : status,
        "text" : text
    })

from ast import literal_eval
from django.forms.models import model_to_dict
def getKnownFace():
     # 引入已知人脸编码
    known_face = list(manager.objects.all())
    for i in range(len(known_face)):
        ID = known_face[i].ID
        known_face[i].encode = literal_eval(known_face[i].encode)#转化成list格式
        known_face[i] = model_to_dict(known_face[i])
        known_face[i]["ID"] = ID
    return known_face

known_face = getKnownFace()