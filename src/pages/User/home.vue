<template>
  <div class="home">
    <button @click="logout">注销</button>
  </div>
</template>

<script>
  export default{
    methods:{
      logout(){
        localStorage.clear()
        global.Router(this,'login')
        global.showToast(this,'已退出登录','success')
      }
    },
    beforeRouteEnter(to,from,next) {
      //进入管理界面时先判断登录
      let UserInfo= JSON.parse(localStorage.getItem("UserInfo"))
      next(vm=>{
        if(UserInfo){
          const data = new URLSearchParams()
          data.append('email',UserInfo.email)
          data.append('ID',UserInfo.ID)
          vm.$axios.post('/MeetingRoom/user/verifyUser',data)
            .then(res => {
              if(res.data.status === 200){
                global.showToast(vm,'登录成功','success')
              }
              else{
                global.Router(vm,'login')
                global.showToast(vm,res.data.text,'cross')
              }
            })
            .catch(err => {console.log(err)})
        }
        else{
          global.Router(vm,'login')
          global.showToast(vm,'请先登录','fail')
        }
      })
    },
  }
</script>

<style>
</style>
