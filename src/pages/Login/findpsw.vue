<template>
  <div class="findpsw">
    <h2 class="title">找回密码</h2>
    <img class="logo" src="../../assets/logo.png">

    <input class="form-control" type="email" placeholder="输入邮箱地址" v-model="email">
    <input class="form-control" type="password" placeholder="输入密码" v-model="password">
    <input class="form-control" type="password" placeholder="再次输入密码" v-model="surePsw">

    <div class="rand">
      <input class="form-control" type="email" placeholder="输入验证码" v-model="rand">
      <div class="getrand" :class="{ wait: second>0 }" @click="getrand">{{SendRand}}</div>
    </div>

    <button class="Sign-in" @click="findPsw">找回密码</button>

    <router-link class="back" :to="{name : 'login'}">
      返回登录
    </router-link>
  </div>
</template>

<script>
  var time
  var mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
  export default{
    data(){
      return{
        second : 0,
        email : '',
        password : '',
        surePsw : '',
        rand : '',
        sure_rand : ''
      }
    },
    methods:{
      findPsw(){//找回密码
        if(this.email === '')
        	global.showToast(this,'请输入邮箱','cross')
        else if(!mailReg.test(this.email))
        	global.showToast(this,'邮箱格式错误','cross')
        else if(this.password === '')
        	global.showToast(this,'请输入密码','cross')
        else if(this.password.length < 6)
        	global.showToast(this,'密码小于6位','cross')
        else if(this.surePsw === '')
        	global.showToast(this,'请确认密码','cross')
        else if(this.surePsw != this.password)
        	global.showToast(this,'两次密码不一致','cross')
        else if(this.rand === '')
        	global.showToast(this,'请输入验证码','cross')
        else if(this.rand != this.sure_rand)
        	global.showToast(this,'验证码错误','cross')
        else{
          global.showLoading(this,'找回密码中')
          const data = new URLSearchParams()
          data.append('name',this.name)
          data.append('password',this.password)
          data.append('email',this.email)
          this.$axios.post('/MeetingRoom/user/findpsw',data)
          	.then(res => {
              if(res.data.status === 200){
                global.Router(this,'login')
                global.showToast(this,'密码已修改','success')
              }
              else
                global.showToast(this,res.data.text,'cross')
          	})
            .catch(err => {console.log(err)})
        }
      },
      getrand(){//获取验证码
        if(this.second === 0){
      		/* 发送邮件 */
      		if(this.email === '')
      			global.showToast(this,'邮箱不能为空','cross')
      		else if(!mailReg.test(this.email))
      			global.showToast(this,'邮箱格式错误','cross')
      		else{
            global.showLoading(this,'发送中')
            const data = new URLSearchParams()
            data.append('name',this.name)
            data.append('email',this.email)
            this.$axios.post('/MeetingRoom/user/sendEmail',data)
            	.then(res => {
                if(res.data.status === 200){
                  this.sure_rand = res.data.text
                  global.showToast(this,'已发送','success')
                  /* 重置计时器*/
                  this.second = 5;
                  time = setInterval(()=>{//setInterval可以重复计时,直到clearInterval
                  	this.second--;
                  	if(this.second === 0){
                  		clearInterval(time)
                  	}
                  },1000)
                }
                else
                  global.showToast(this,res.data.text,'cross')
            	})
              .catch(err => {console.log(err)})
          }}
      },
    },
    computed:{
      SendRand(){//判断获取验证码框的值，返回不同文本
      	if(this.second === 0)
      		return '获取验证码'
      	else
      		if(this.second < 10)
      			return '重新获取0' + this.second
      		else
      			return '重新获取' + this.second
      }
    }
  }
</script>

<style scoped>
  .findpsw{
    width: 90%;
    max-width: 700px;
    margin: 10px auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .findpsw .title{
    text-align: center;
  }
  .findpsw .logo{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin: 10px 0;
  }
  .findpsw input{
    font-size: 18px;
    height: 40px;
    margin: 5px 0;
  }
  .findpsw .Sign-in{
    color: #f4f4f4;
    background:linear-gradient(-90deg,rgba(63,205,235,1),rgba(188,226,158,1));
    width: 100%;
    height: 40px;
    margin-top: 5px;
    border: none;
    outline: none;
    border-radius: 10px;
    cursor: pointer;
  }
  .findpsw .Sign-in:active{
    background: linear-gradient(-90deg,rgba(188,226,158,1),rgba(63,205,235,1));
    box-shadow: 1px 1px 1px #bebebe;
  }

  .findpsw .back{
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

  .findpsw .rand{
    width: 100%;
    display: flex;
    align-items: center;
  }
  .findpsw .rand input{
    width: 70%;
  }
  .findpsw .rand .getrand{
  	/*获取验证码按键*/
    flex: 1;
  	color: #FF7D13;
  	font-size: 15px;
    padding: 9px 0;
  	border:1px solid rgba(255,168,0,0.8);
  	border-radius: 5px;
    margin-left: 5px;
  	text-align: center;
  	z-index: 2;
  }
  .findpsw .rand .wait{
  	/*等待重新获取*/
  	color: #999999 !important;
  	border:1px solid #999999;
  }
</style>
