<template>
  <div class="room-detail">
    <div class="mask"></div>

    <div class="room">
      <div class="condition">
        <span class="head">预定状态：</span>
        <span class="body" v-if="recordInfo.condition === 3">拒绝预订</span>
        <span class="body" v-if="recordInfo.condition === 0">待管理员确认</span>
        <span class="body" v-if="recordInfo.condition === 1">已同意预定</span>
        <span class="body" v-if="recordInfo.condition === 2">已归还</span>
      </div>

      <div class="info">
        <span>地点：{{recordInfo.roomInfo.place}}</span>
      </div>

      <div class="info">
        <span>容纳人数：{{recordInfo.roomInfo.maxPeople}}</span>
      </div>

      <div class="introduction">
        <span>会议室介绍</span>
        <p>{{recordInfo.roomInfo.introduction}}</p>
      </div>

      <span class="title">预订人信息</span>

      <div class="info">
        <span>姓名：{{recordInfo.reserveInfo.name}}</span>
      </div>

      <div class="info">
        <span>邮箱：{{recordInfo.reserveInfo.email}}</span>
      </div>

      <div class="info">
        <span>日期：</span>
         <p>{{recordInfo.reserveInfo.date}}</p>
      </div>

      <div class="info">
        <span>时间：</span>
        <p>{{recordInfo.reserveInfo.time}}</p>
      </div>

      <div class="introduction">
        <span>用途</span>
        <p>{{recordInfo.reserveInfo.use}}</p>
      </div>

      <div class="control">
        <div style="color: #cd2d2d;" @click="Close">取消</div>
        <span>|</span>
        <div v-if="recordInfo.condition === 2 || recordInfo.condition === 3" style="color: #088573;" @click="Sure">确定</div>
        <div v-if="recordInfo.condition === 1" style="color: #088573;" @click="Sure">归还会议室</div>
        <div v-if="recordInfo.condition === 0" style="color: #088573;" @click="Sure">取消预定</div>
      </div>

    </div>
  </div>
</template>

<script>
  export default{
    methods:{
      Sure(){//确认
        if(this.recordInfo.condition === 2 || this.recordInfo.condition === 3)
          this.$emit('Close')
        else if(this.recordInfo.condition === 1)
          this.backRoom()
        else
          this.widthdrawRoom()
      },
      backRoom(){
        this.$dialog.confirm({
          title : '提示',
          message: '确认归还会议室?',
          closeOnPopstate : true,
          closeOnClickOverlay : true,
          confirmButtonColor : '#088573',
          cancelButtonColor : '#cd2d2d',
        })
        .then(() => {
          global.showLoading(this,'归还中...')
          const data = new URLSearchParams()
          data.append('roomID',this.recordInfo.roomInfo.ID)
          data.append('reserveID',this.recordInfo.ID)

          this.$axios.post('/MeetingRoom/reserve/BackRoom',data)
            .then(res => {
              if(res.data.status === 200){
                this.$emit('Sure','back')
              }
              else
                console.log(res.data)
            })
            .catch(err => global.showToast(this,'网络错误','cross'))
        })
        .catch(res => {
          console.log(res)
        })
      },
      widthdrawRoom(){
        this.$dialog.confirm({
          title : '提示',
          message: '确认取消预定?',
          closeOnPopstate : true,
          closeOnClickOverlay : true,
          confirmButtonColor : '#088573',
          cancelButtonColor : '#cd2d2d',
        })
        .then(() => {
          global.showLoading(this,'取消中...')
          this.$axios.post('/MeetingRoom/reserve/WithdrawReserve',this.requestData())
            .then(res => {
              if(res.data.status === 200){
                console.log(res.data)
                this.$emit('Sure','widthdraw')
              }
              else
                console.log(res.data)
            })
            .catch(err => global.showToast(this,'网络错误','cross'))
        })
        .catch(res => {
          console.log(res)
        })
        .catch(res => {
          console.log(res)
        })
      },
      requestData(){
        const roomID = this.recordInfo.roomInfo.ID
        const reserveID = this.recordInfo.ID
        const data = new URLSearchParams()
        data.append('roomID',roomID)
        data.append('reserveID',reserveID)
        return data
      },
      Close(){
        this.$emit('Close')
      }
    },
    props:{
      recordInfo : Object
    }
  }
</script>

<style scoped>
  p{
    margin: 0;
  }

  .room .condition{
    font-size: 20px;
  }
  .room .condition .body{
    color: #07C160;
    font-weight: 600;
  }

  .room .info{
    border-bottom: 1px solid #42B983;
    margin-bottom: 5px;
    line-height: 1.5;
    display: flex;
    align-items: center;
  }
  .room .title{
    font-weight: 600;
    margin: 5px 0;
  }
  .room .introduction p{
    border: 1px solid #42B983;
    min-height: 40px;
    border-radius: 5px;
    padding: 5px;
  }

  .room .checkbox{
    margin-top: 5px;
  }
  /* 按键样式 */
  .room .control{
  	margin: 10px 0;
  	display: flex;
  }
  .room .control div{
  	width: 50%;
  	text-align: center;
  }
  .room .control span{
  	color: rgba(174,174,174,0.6);
  }

  /* 提示框 */
  .model{
    font-size: 20px;
  }

  .mask{
  	width:100vh;
  	height:100vh;
  	position:fixed;
  	background-color:#b2b2b2;
  	z-index:99;
  	top:0;
  	left:0;
  	opacity:0.8;
    animation: show 0.5s ease-out;
  }
  @keyframes show{
    0%{
    	opacity: 0;
    }
    100%{
    	opacity: 1;
    }
  }
  .room{
    background: #FFFFFF;
    width: 90%;
    border-radius: 10px;
    margin-bottom: 10%;
    box-shadow:2px 2px 5px #7b7b7b;
    padding: 5px;
    position: absolute;
    top: 5%;
    left: 5%;
    z-index: 999;
    animation: appear 0.5s ease-out;
  }
  @keyframes appear{
    0%{
  		opacity: 0;
  		transform: translatey(-350px);
  	}
    100%{
    	opacity: 1;
    	transform: translateY(0);
    }
  }
</style>
