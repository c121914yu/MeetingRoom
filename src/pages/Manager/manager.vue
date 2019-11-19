<template>
  <div class="manager">
    <div class="title">
      <p>欢迎回来,{{UserInfo.name}}</p>
      <span @click="logout">注销</span>
    </div>

    <div class="overview">
      <div class="item" :class="current === 0 ? 'current' : ''"
        style="border-right: 1px solid #42B983;" @click="currentChange(0)">
        <span>会议室总数</span>
        <span class="num">5</span>
      </div>
      <div class="item" :class="current === 1 ? 'current' : ''"
        style="border-right: 1px solid #42B983;" @click="currentChange(1)">
        <span>已预订</span>
        <span class="num">5</span>
      </div>
      <div class="item" :class="current === 2 ? 'current' : ''" @click="currentChange(2)">
        <span>待处理预定</span>
        <span class="num">5</span>
      </div>
    </div>

    <!-- 全部会议室 -->
    <div class="all-room" :class="current === 0 ? 'showAnimation':''">
      <div
        class="item"
        v-for="(room,index) in rooms"
        :key="index"
        v-if="current === 0"
      >
        <span class="detail" @click="readDetail(room,index)">查看详细</span>
        <p class="conditon" v-if="room.condition === 0">状态：空闲</p>
        <p class="conditon" v-if="room.condition === 1">状态：待处理</p>
        <p class="conditon" v-if="room.condition === 2">状态：已预订</p>
        <p>地点：{{room.place}}</p>
        <p>可容纳人数：{{room.maxPeople}}</p>
      </div>
    </div>

    <!-- 已预订 -->
    <div class="booked" :class="current === 1 ? 'showAnimation':''">
      <div
        class="item"
        v-for="(room,index) in rooms"
        :key="index"
        v-if="room.condition === 2 && current === 1"
      >
        <div class="room-info">
          <span>{{room.place}}</span>
          <span class="detail" @click="readDetail(room,index)">查看详细</span>
        </div>
        <div class="user-info">
          <p>预订人：{{room.reserveInfo.name}}</p>
          <p>邮&emsp;箱：{{room.reserveInfo.email}}</p>
          <p>时&emsp;间：{{room.reserveInfo.date}}&ensp;{{room.reserveInfo.time}}</p>
        </div>
      </div>
    </div>

    <!-- 待处理 -->
    <div class="booked" :class="current === 2 ? 'showAnimation':''">
      <div
        class="item"
        v-for="(room,index) in rooms"
        :key="index"
        v-if="room.condition === 1 && current === 2"
      >
        <div class="room-info">
          <span>{{room.place}}</span>
          <span class="detail" @click="readDetail(room,index)">查看详细</span>
        </div>
        <div class="user-info">
          <p>预订人：{{room.reserveInfo.name}}</p>
          <p>邮&emsp;箱：{{room.reserveInfo.email}}</p>
          <p>时&emsp;间：{{room.reserveInfo.date}}&ensp;{{room.reserveInfo.time}}</p>
        </div>
      </div>
    </div>

    <img class="add-room" src="../../assets/AddRoom.png" @click="AddRoom">

    <manage-room v-if="detail" :roomInfo="roomInfo"
      @Close="detail=false" @Sure="Sure">
    </manage-room>
  </div>
</template>

<script>
  import manageRoom from './manageRoom'
  export default{
    data(){
      return{
        UserInfo : '',
        current : 2,
        detail : false,
        index : 0,//-1代表添加会议室
        roomInfo : '',
        rooms : [//condition 0代表闲置，1预定中，2同意预定
          {place:'广A404',maxPeople:1,introduction:'碍事法师',condition:1,reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10-16:20',use:'开会萨法萨法发士大夫撒大师傅add是发多少发撒安抚大奥德赛发多少奥德赛啊啊'}},
          {place:'广A404',maxPeople:2,introduction:'碍事法师',condition:0,reserveInfo:''},
          {place:'广A404',maxPeople:3,introduction:'碍事法师是打发大沙发大厦发达撒师范生法大师傅撒打撒发发撒安抚萨法萨法撒发顺丰撒是送达啊方法打发大锅饭大锅饭萨法萨法sad打发打发撒按时啊大概大大安防工大',condition:2,reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10-16:20',use:'开会'}},
          {place:'广A404',maxPeople:4,introduction:'碍事法师',condition:0,reserveInfo:''},
          {place:'广A404',maxPeople:5,introduction:'碍事法师',condition:1,reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10-16:20',use:'开会'}},
        ]
      }
    },
    methods:{
      currentChange(index){//选择导航栏
        this.current = index
      },
      AddRoom(){//添加会议室
        this.roomInfo = {
          place : '',
          maxPeople : '',
          introduction : '',
          condition : 0,
          reserveInfo : ''
        }
        this.index = -1
        this.detail = true
      },
      readDetail(room,index){//查看详细
        this.roomInfo = room
        this.index = index
        this.detail = true
      },
      Sure(e){
        if(e.way === 'Add')
          this.rooms.push(e.roomInfo)
        else if(e.way === 'Change')
          this.rooms[this.index] = e.roomInfo
        else if(e.way === 'Remove')
          this.rooms.splice(this.index,1)
        else if(e.way === 'Agree')
          this.rooms[this.index].condition = e.condition
        else if(e.way === 'Refuse')
          this.rooms[this.index].condition = e.condition
        else if(e.way === 'Withdraw')
          this.rooms[this.index].condition = e.condition
        this.detail = false
      },
      logout(){//退出登录
        sessionStorage.removeItem('manager')
        global.Router(this,'login')
        global.showToast(this,'已退出登录','success')
      }
    },
    beforeRouteEnter(to,from,next) {
      //进入管理界面时先判断登录
      let UserInfo = JSON.parse(sessionStorage.getItem("manager"))
      next(vm=>{
        if(UserInfo)
          vm.UserInfo = UserInfo
        else{
          global.Router(vm,'login')
          global.showToast(vm,'请先登录','fail')
        }
      })
    },
    components:{
      'manage-room' : manageRoom
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

  .all-room{
    margin: 5px 0;
  }
  .all-room .item{
    font-size: 17px;
    background: #42B983;
    color: #f0f832;
    width: 95%;
    height: 90px;
    box-shadow: 2px 2px 2px #7D7E80;
    margin: 10px auto;
    padding: 8px;
    border-radius: 15px;
    line-height: 1.2;
  }
  .all-room .item .conditon{
    color: #FFFFFF;
  }
  .all-room .item .detail{
    color: #FFFFFF;
    float: right;
    margin-right: 10px;
  }

  .booked{
    margin: 5px 0;
  }
  .booked .item{
    font-size: 17px;
    background: #42B983;
    color: #f0f832;
    width: 95%;
    height: 125px;
    box-shadow: 2px 2px 2px #7D7E80;
    margin: 10px auto;
    padding: 8px;
    border-radius: 15px;
    line-height: 1.2;
  }
  .booked .item .room-info{
    border-bottom: 1px solid #7D7E80;
    padding-bottom: 5px;
  }
  .booked .item .room-info .detail{
    color: #FFFFFF;
    float: right;
    margin-right: 10px;
  }
  .booked .item .user-info{
    padding: 5px 0;
  }

  .add-room{
    width: 50px;
    height: 50px;
    position: absolute;
    right: 10px;
    bottom: 20px;
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

  .add-room{
    margin: 10px 0;
    position: absolute;
    right: 10px;
    border-radius: 10px;
  }
</style>
