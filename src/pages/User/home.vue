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
        <span class="num">{{rooms.length}}</span>
      </div>
      <div class="item" :class="current === 1 ? 'current' : ''"
        style="border-right: 1px solid #42B983;" @click="currentChange(1)">
        <span>正在预定</span>
        <span class="num">{{reserving()}}</span>
      </div>
      <div class="item" :class="current === 2 ? 'current' : ''" @click="currentChange(2)">
        <span>预定记录</span>
        <span class="num">{{reserveRecord.length}}</span>
      </div>
    </div>

    <div v-if="current === 0" class="list" :class="current === 0 ? 'showAnimation':''">
      <div
        class="item"
        v-for="(room,index) in rooms"
        :key="index"
      >
        <span class="detail" @click="Reserve(index)">点击预定</span>
        <p><span>地点：</span>{{room.place}}</p>
        <p><span>可容纳人数：</span>{{room.maxPeople}}</p>
        <p><span>会议室介绍：</span>{{room.introduction}}</p>
      </div>
    </div>

    <div v-if="current === 1" class="list" :class="current === 1 ? 'showAnimation':''">
      <div
        class="item record"
        v-for="(item,index) in reserveRecord"
        :key="index"
        v-if="item.condition === 0 || item.condition === 1"
      >
        <span class="detail" @click="Detail(index)">查看详细</span>
        <p v-if="item.condition === 0"><span>状态：</span>待管理员确认</p>
        <p v-if="item.condition === 1"><span>状态：</span>使用中</p>
        <p><span>地点：</span>{{item.roomInfo.place}}</p>
        <p><span>时间：</span>{{item.reserveInfo.date}} {{item.reserveInfo.time}}</p>
      </div>
    </div>

    <div v-if="current === 2" class="list" :class="current === 2 ? 'showAnimation':''">
      <div
        class="item record"
        v-for="(item,index) in reserveRecord"
        :key="index"
      >
        <span class="detail" @click="Detail(index)">查看详细</span>
        <p v-if="item.condition === 0"><span>状态：</span>待管理员确认</p>
        <p v-if="item.condition === 1"><span>状态：</span>使用中</p>
        <p v-if="item.condition === 2"><span>状态：</span>已归还</p>
        <p v-if="item.condition === 3"><span>状态：</span>拒绝预定</p>
        <p><span>地点：</span>{{item.roomInfo.place}}</p>
        <p><span>时间：</span>{{item.reserveInfo.date}} {{item.reserveInfo.time}}</p>
      </div>
    </div>

    <room-reserve v-if="reserve" :roomInfo="roomInfo" :UserInfo="UserInfo"
      @Close="Close" @Sure="Sure">
    </room-reserve>

    <record-detail v-if="detail" :recordInfo="recordInfo"
     @Sure="Sure"  @Close="Close">
    </record-detail>
  </div>
</template>

<script>
  import roomReserve from './roomReserve'
  import RecordDetail from './Detail'
  export default{
    data(){
      return{
        UserInfo : {},
        current : 2,
        reserve : false,
        detail : false,

        index : 0,
        roomInfo : {},
        rooms : [],//condition 0代表闲置，1预定中，2同意预定

        recordInfo : {},
        reserveRecord : []//condition 0代表待确认 1使用中 2已归还,3拒绝
      }
    },
    methods:{
      currentChange(index){//选择导航栏
        this.current = index
      },
      Reserve(index){
        this.roomInfo = this.rooms[index]
        this.index = index
        this.reserve = true
      },
      Detail(index){
        this.recordInfo = this.reserveRecord[index]
        this.index = index
        this.detail = true
      },
      Sure(e){
        let remind = '获取中...'
        let text = ''
        if(e === 'reserve'){//预定会议室
          remind = '预订中...'
          text = '预订成功'
        }
        else if(e === 'back'){//归还会议室
          remind = '归还中...'
          text = '归还成功'
        }
        else if(e === 'widthdraw'){
          remind = '取消中...'
          text = '已取消预订'
        }
        else if(e === 'getInfo'){
          remind = '重新获取会议室'
          text = '已更新...'
        }
        this.GetInfo(remind,text)
      },
      Close(){
        this.detail = false
        this.reserve = false
      },
			GetInfo(remind,text){
        global.showLoading(this,remind)
        const data = new URLSearchParams()
        data.append('email',this.UserInfo.email)
				this.$axios.post('/MeetingRoom/reserve/GetInfo',data)
				  .then(res => {
				    this.rooms = res.data.rooms
            let reserveRecord = res.data.reserveRecord

            reserveRecord.forEach(item => {
              item.roomInfo = JSON.parse(item.roomInfo)
              item.reserveInfo = JSON.parse(item.reserveInfo)
            })
            this.reserveRecord = reserveRecord
            this.reserving()
            global.showToast(this,text,'success')
            this.reserve = false
            this.detail = false
				  })
				  .catch(err => console.log(err))
			},
      reserving(){//计算预定中的
        let ing = 0
        this.reserveRecord.forEach(item => {
          if(item.condition === 0 || item.condition === 1)
            ing++
        })
        return ing
      },
      logout(){//退出登录
        localStorage.clear()
        global.Router(this,'login')
        global.showToast(this,'已退出登录','success')
      }
    },
    beforeRouteEnter(to,from,next) {
      let UserInfo= JSON.parse(localStorage.getItem("UserInfo"))
      if(from.path === '/'){//直接进入需要判断信息
        next(vm=>{
					global.showLoading(vm,'登录中...')
          if(UserInfo){
            const data = new URLSearchParams()
            data.append('email',UserInfo.email)
            data.append('ID',UserInfo.ID)
            vm.$axios.post('/MeetingRoom/user/verifyUser',data)
              .then(res => {
                if(res.data.status === 200){
                  vm.UserInfo = UserInfo
                  vm.GetInfo('登录中...','登录成功')
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
          vm.GetInfo('登录中...','登录成功')
        })
      }
    },
    components:{
      'room-reserve' : roomReserve,
      'record-detail' : RecordDetail
    }
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

  .list{
    margin: 5px 0;
  }
  .list .item{
    font-size: 17px;
    background: #42B983;
    color: #f0f832;
    width: 95%;
    min-height: 80px;
    box-shadow: 2px 2px 2px #7D7E80;
    margin: 10px auto;
    padding: 8px;
    padding-bottom: 1px;
    border-radius: 15px;
    line-height: 1.2;
  }
  .list .item p span{
    color: #FFFFFF;
  }
  .list .item .detail{
    color: #FFFFFF;
    float: right;
    margin-right: 10px;
  }

  .showAnimation{
    animation: show 0.7s ease-out;
  }
  @keyframes show{
    0%{
  		opacity: 0;
  		transform: translateX(200px);
  	}
    100%{
    	opacity: 1;
    	transform: translateX(0);
    }
  }
</style>
