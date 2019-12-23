<template>
  <div class="manager">
		<h2>管理员登录</h2>
		<div class="camera">
      <video v-show="showVideo" id="video" width="250px" height="250px" autoplay="autoplay"></video>
      <div
        class="photo"
        :class="showVideo ? 'discerning' : ''"
        @click="discern"
       >
        {{remarkText}}
       </div>
		</div>
    <canvas v-show="false" id="canvas" width="500px" height="500px"></canvas>

    <!-- 添加管理员 -->
		<button class="add-manager" @click="NewManager">添加管理员</button>
    <div v-if="AddManager" class="mask"></div>
    <div v-if="AddManager" class="Popup">
      <input class="form-control" type="text" placeholder="输入你的名字" v-model="name">
      <input class="form-control" type="email" placeholder="输入你的邮箱地址" v-model="email">

      <!-- 确认，取消键 -->
      <div class="Btn">
      	<div style="color: #cd2d2d;" @click="Close">取消</div>
      	<span>|</span>
      	<div style="color: #088573;" @click="SureAdd">确认</div>
      </div>
    </div>

    <router-link class="back" :to="{name : 'login'}">
      返回登录
    </router-link>
  </div>
</template>

<script>
  export default{
    data(){
      return{
        showVideo : false,
        remarkText : '点击识别',
        getTimes : 0,

        login : true,

        AddManager : false,
        name : '',
        email : ''
      }
    },
    methods:{
      discern(){
        if(this.remarkText === '点击识别' || this.remarkText === '点击重试'){
          this.login = true
          this.startDiscern()
          this.remarkText = '识别中...'
        }
      },
      startDiscern(){//开始人脸识别
        this.showVideo = true
        let video = document.getElementById("video");
        let constraints = {
            video: {width: 250, height: 250}
        }
        // 调用摄像头
        let promise = navigator.mediaDevices.getUserMedia(constraints)
        promise.then((MediaStream) => {
            video.srcObject = MediaStream
            video.play()
            if(this.login)
              this.mangerLogin()
            else
              this.managerRegister()
        }).catch((PermissionDeniedError) => {
            console.log(PermissionDeniedError)
        })
      },
      stopDiscern(){//停止人脸识别
        this.showVideo = false
        let video = document.getElementById('video')
        video.srcObject.getTracks()[0].stop()
      },
      mangerLogin() {//管理员登录
        if(this.getTimes === 10)
          this.failreq('识别失败')
        else{
          let img = this.getPhoto()
          const data = new URLSearchParams()
          data.append('base',img)
          this.$axios.post('/MeetingRoom/user/managerLogin',data)
            .then(res => {
              console.log(res.data)
              if(res.data.status === 200){
                this.getTimes = 0
                const user = JSON.stringify({
                  name : res.data.name,
                  email : res.data.email,
                  ID : res.data.ID
                })
                sessionStorage.setItem('manager',user)
                this.stopDiscern()
                global.showToast(this,'登录成功','success')
                global.Router(this,'manager')
              }
              else{
                this.getTimes++
                this.mangerLogin()
              }
            })
            .catch(err => {
              console.log(err)
              this.failreq('网络错误')
            })
        }
      },
      managerRegister(){//注册管理员
        if(this.getTimes === 30)
          this.failreq('录入失败')
        else{
          let img = this.getPhoto()
          const data = new URLSearchParams()
          data.append('base',img)
          data.append('name',this.name)
          data.append('email',this.email)

          this.$axios.post('/MeetingRoom/user/managerRegister',data)
            .then(res => {
              if(res.data.status === 400){
                this.getTimes++
                this.managerRegister()
              }
              else{//录入完成
                this.getTimes = 0
                this.stopDiscern()
                global.showToast(this,'录入成功','success')
                this.remarkText = '点击识别'
                this.name = ''
                this.email = ''
                console.log(res.data)
              }
            })
            .catch(err => {
              console.log(err)
              this.failreq('网络错误')
            })
        }
      },
      failreq(text){
        this.remarkText = '点击重试'
        this.stopDiscern()
        this.getTimes = 0
        global.showToast(this,text,'cross')
      },
      getPhoto(){//获取屏幕截图照片
        let video = document.getElementById('video')
        let canvas = document.getElementById("canvas")
        let ctx = canvas.getContext('2d')
        ctx.drawImage(video, 0, 0, 250, 250)
        let img = document.getElementById('canvas').toDataURL(); //base64格式
        // 这里的img就是得到的图片
        return img
      },

			NewManager(){
				this.AddManager = true
			},
      Close(){
        this.name = ''
        this.email = ''
        this.AddManager = false
      },
      SureAdd(){
        let mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
        if(this.name === '')
          global.showToast(this,'请输入名字','cross')
        else if(this.email === '')
        	global.showToast(this,'请输入邮箱','cross')
        else if(!mailReg.test(this.email))
        	global.showToast(this,'邮箱格式错误','cross')
        else{
          this.login = false
          this.remarkText = '录取脸部信息中'
          this.startDiscern()
          this.AddManager = false
        }
      }
    },//methods结束
  }
</script>

<style scoped>
  .manager{
    width: 100%;
    height: 100%;
    text-align: center;
  }
	.manager .camera{
    background: #BEBEBE;
    width: 250px;
    height: 250px;
    border: 1px solid #969799;
		border-radius: 50%;
    margin: 50px auto;
	}
  .manager .camera .photo{
    color: #F7F7F7;
    font-size: 20px;
    position: relative;
    top: 50%;
    transform: translateY(-50%);
    z-index: 99;
  }
  .manager .camera .discerning{
    color: rgba(255,255,255,0.6);
  }
  .manager .camera #video{
    position: absolute;
    margin-top: 0;
    border-radius: 50%;
    transform: translateX(-50%);
  }

  /* 新增管理员*/
  .manager .add-manager{
    color: #f4f4f4;
    background:linear-gradient(-90deg,rgba(63,205,235,1),rgba(188,226,158,1));
    width: 70%;
    height: 40px;
    margin: 5px auto;
    border: none;
    outline: none;
    border-radius: 10px;
    cursor: pointer;
  }
  .manager .add-manager:active{
    background: linear-gradient(-90deg,rgba(188,226,158,1),rgba(63,205,235,1));
    box-shadow: 1px 1px 1px #bebebe;
  }

  /* 蒙层样式 */
  .mask{
  	width:100%;
  	height:100%;
  	position:fixed;
  	background-color:#b2b2b2;
  	z-index:99;
  	top:0;
  	left:0;
  	opacity:0.8;
  }
  /* 弹框样式 */
  .Popup{
  	background: #FFFFFF;
  	width: 90%;
  	border-radius: 10px;
  	margin-bottom: 10%;
  	box-shadow:2px 2px 5px #7b7b7b;
    padding: 10px;
  	position: absolute;
  	top: 20%;
  	left: 5%;
  	z-index: 999;
  	animation: appear 0.5s ease-out;
  }
  @keyframes appear{
    0%{
  		opacity: 0;
  		transform: translateY(-100px);
  	}
    100%{
    	opacity: 1;
    	transform: translateY(0);
    }
  }
  .Popup input{
    margin: 5px 0;
  }
  .Popup .Btn{
  	margin-top: 10px;
  	display: flex;
  }
  .Popup .Btn div{
  	width: 50%;
  	text-align: center;
  }
  .Popup .Btn span{
  	color: rgba(174,174,174,0.6);
  }
  /* 弹框样式 */

  .manager .back{
    font-size: 13px;
    color: #fdd930;
    background-color: rgba(45,161,109,0.8);
    padding: 5px;
    position: absolute;
    left: 0;
    top: 35px;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
  }
</style>
