<template>
  <div class="login">
    <h2 class="title">会议室预定系统</h2>
    <img class="logo" src="../../assets/logo.png">

    <input class="form-control" type="email" placeholder="输入你的邮箱地址" v-model="email">
    <input class="form-control" type="password" placeholder="输入密码" v-model="password">
    <button class="Sign-in" @click="login">登录</button>

    <div class="problem">
      <router-link :to="{name:'findpsw'}">
        <span>找回密码</span>
       </router-link>
      <span style="color: #525252;">&emsp;|&emsp;</span>
      <router-link :to="{name:'register'}">
        <span>注册账户</span>
       </router-link>
    </div>

    <router-link class="manager" :to="{name:'managerLogin'}">
      管理员登录
    </router-link>
  </div>
</template>

<script>
  var mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
  export default{
    data(){
      return{
        email : '',
        password : ''
      }
    },
    methods:{
      login(){
        if(this.email === '')
        	global.showToast(this,'请输入邮箱','cross')
        else if(!mailReg.test(this.email))
        	global.showToast(this,'邮箱格式错误','cross')
        else if(this.password === '')
        	global.showToast(this,'请输入密码','cross')
        else{
          global.showLoading(this,'登录中')
          const data = new URLSearchParams()
          data.append('password',this.password)
          data.append('email',this.email)
          this.$axios.post('/MeetingRoom/user/login',data)
          	.then(res => {
              if(res.data.status === 200){
                const user = JSON.stringify({
                  ID : res.data.ID,
                  name : res.data.name,
                  email : this.email
                })
                localStorage.setItem("UserInfo",user)
                global.Router(this,'home')
              }
              else
                global.showToast(this,res.data.text,'cross')
          	})
            .catch(err => {console.log(err)})
        }
      }
    }
  }
</script>

<style>
  .login{
    width: 90%;
    max-width: 700px;
    margin: 10px auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .login .title{
    text-align: center;
  }
  .login .logo{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin: 10px 0;
  }
  .login input{
    font-size: 18px;
    height: 40px;
    margin: 5px 0;
  }
  .login .Sign-in{
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
  .login .Sign-in:active{
    background: linear-gradient(-90deg,rgba(188,226,158,1),rgba(63,205,235,1));
    box-shadow: 1px 1px 1px #bebebe;
  }

  .login .problem{
    margin-top: 20px;
  }
  .login .problem span{
    color: #FFA800;
  }

  .login .manager{
    font-size: 13px;
    color: #fdd930;
    background-color: rgba(45,161,109,0.8);
    padding: 5px;
    position: absolute;
    right: 0;
    top: 110px;
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
  }
</style>
