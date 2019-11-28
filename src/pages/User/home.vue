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
        <span class="num">5</span>
      </div>
      <div class="item" :class="current === 2 ? 'current' : ''" @click="currentChange(2)">
        <span>预定记录</span>
        <span class="num">5</span>
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
        v-if="item.condition != 2"
      >
        <span class="detail" @click="Detail(index)">查看详细</span>
        <p v-if="item.condition === 0"><span>状态：</span>待确定</p>
        <p v-if="item.condition === 1"><span>状态：</span>使用中</p>
        <p v-if="item.condition === 2"><span>状态：</span>已归还</p>
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
        <p v-if="item.condition === 0"><span>状态：</span>待确定</p>
        <p v-if="item.condition === 1"><span>状态：</span>使用中</p>
        <p v-if="item.condition === 2"><span>状态：</span>已归还</p>
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
        rooms : [//condition 0代表闲置，1预定中，2同意预定
          {place:'广A404',maxPeople:2,introduction:'碍事法师沙发垫安抚安抚多试试宿舍宿舍是是是是宿舍发发阿斯蒂芬安抚大师傅大师傅啊',condition:0,reserveInfo:''},
          {place:'广A404',maxPeople:4,introduction:'碍事法师',condition:0,reserveInfo:''},
        ],
        recordInfo : {},
        reserveRecord : [//condition 0代表待确认 1使用中 2已归还
          {condition:0,roomInfo:{place:'广A404',maxPeople:4,introduction:'碍事法师'},reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10 - 16:20',use:'开会萨法萨法发士大夫撒大师傅add是发多少发撒安抚大奥德赛发多少奥德赛啊啊'}},
          {condition:0,roomInfo:{place:'广A404',maxPeople:4,introduction:'碍事法师'},reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10 - 16:20',use:'开会萨法萨法发士大夫撒大师傅add是发多少发撒安抚大奥德赛发多少奥德赛啊啊'}},
          {condition:1,roomInfo:{place:'广A404',maxPeople:4,introduction:'碍事法师'},reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10 - 16:20',use:'开会萨法萨法发士大夫撒大师傅add是发多少发撒安抚大奥德赛发多少奥德赛啊啊'}},
          {condition:2,roomInfo:{place:'广A404',maxPeople:4,introduction:'碍事法师'},reserveInfo:{name:'余金隆',email:'555@qq.com',date:'2019/11/18',time:'14:10 - 16:20',use:'开会萨法萨法发士大夫撒大师傅add是发多少发撒安抚大奥德赛发多少奥德赛啊啊'}},
        ]
      }
    },
		created(){
			this.GetRoom()
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
        if(e === 'reserve')//预定会议室
          this.rooms.splice(this.index,1)
        else if(e === 'back')//归还会议室
          this.reserveRecord[this.index].condition = 2
        else if(e === 'widthdraw')
          this.reserveRecord.splice(this.index,1)
        console.log(this.reserveRecord)
        this.reserve = false
        this.detail = false
      },
      Close(){
        this.detail = false
        this.reserve = false
      },
			GetRoom(){
				this.$axios.post('/MeetingRoom/reserve/GetRoom')
				  .then(res => {
				    console.log(res.data)
				  })
				  .catch(err => console.log(err))
			},
      logout(){//退出登录
        localStorage.clear()
        global.Router(this,'login')
        global.showToast(this,'已退出登录','success')
      }
    },
    beforeRouteEnter(to,from,next) {
      let UserInfo= JSON.parse(localStorage.getItem("UserInfo"))
      next(vm=>{vm.UserInfo = UserInfo})
     if(from.path === '/'){//直接进入需要判断信息
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
