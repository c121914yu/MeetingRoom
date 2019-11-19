<template>
  <div class="home">
    <div class="title">
      <p>当前账号：{{UserInfo.name}}</p>
      <span @click="logout">注销</span>
    </div>

    <div class="overview">
      <div class="item" :class="current === 0 ? 'current' : ''"
        style="border-right: 1px solid #42B983;" @click="currentChange(0)">
        <span>可预定会议室</span>
        <span class="num">5</span>
      </div>
      <div class="item" :class="current === 1 ? 'current' : ''"
        style="border-right: 1px solid #42B983;" @click="currentChange(1)">
        <span>我的预定</span>
        <span class="num">5</span>
      </div>
      <div class="item" :class="current === 2 ? 'current' : ''" @click="currentChange(2)">
        <span>预定记录</span>
        <span class="num">5</span>
      </div>
    </div>

  </div>
</template>

<script>
  export default{
    data(){
      return{
        UserInfo : {},
        current : 0,
      }
    },
    methods:{
      currentChange(index){//选择导航栏
        this.current = index
      },
      logout(){//退出登录
        localStorage.clear()
        global.Router(this,'login')
        global.showToast(this,'已退出登录','success')
      }
    },
    beforeRouteEnter(to,from,next) {
      //直接进入管理界面时先判断登录信息是否过期
      let UserInfo= JSON.parse(localStorage.getItem("UserInfo"))
      next(vm=>{vm.UserInfo = UserInfo})
     /* if(from.path === '/'){
        next(vm=>{
          if(UserInfo){
            const data = new URLSearchParams()
            data.append('email',UserInfo.email)
            data.append('ID',UserInfo.ID)
            vm.$axios.post('/MeetingRoom/user/verifyUser',data)
              .then(res => {
                if(res.data.status === 200){
                  vm.UserInfo = UserInfo
                  global.showToast(vm,'登录成功','success')
                }
                else{
                  global.Router(vm,'login')
                  global.showToast(vm,res.data.text,'cross')
                }
              })
              .catch(err => {
                global.Router(vm,'login')
                global.showToast(vm,'服务器异常','cross')
              })
          }
          else{
            global.Router(vm,'login')
            global.showToast(vm,'请先登录','fail')
          }
        })
      }
      else{//从登录界面进入
        next(vm=>{
          vm.UserInfo = UserInfo
          global.showToast(vm,'登录成功','success')
        })
      } */
    },
  }
</script>

<style>
  body{
    background: #F4F4F4;
  }
  .title{
    text-align: center;
    margin: 10px auto;
    display: flex;
    align-items: center;
  }
  .title p{
    line-height: 1;
    font-size: 20px;
    margin-left: 20px;
  }
  .title span{
    line-height: 1;
    color: #b62323;
    margin-left: 15px;
    margin-top: -5px;
  }

  .overview{
    display: flex;
    border-top: 1px solid #42B983;
    border-bottom: 1px solid #42B983;
  }
  .overview .item{
    width: 33.33%;
    line-height: 1.5;
    padding-top: 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .overview .item .num{
    font-size: 18px;
  }
  .overview .current{
    color: #f1fd00;
    background-color: rgba(66,185,131,0.7);
    animation: changeCurrent 0.5s;
  }
  @keyframes changeCurrent{
    0%{
      color: #333333;
  		background-color: rgba(66,185,131,0);
  	}
    100%{
      color: #f1fd00;
    	background-color: rgba(66,185,131,0.7);
    }
  }
</style>
