<template>
  <div class="room-detail">
    <div class="mask"></div>

    <div class="room">
      <div class="remark" v-if="roomInfo.condition != 0 && !addRoom">
        该会议室已被预订,暂不可修改信息
      </div>

      <div class="newRoom" v-if="addRoom">
        添加会议室
      </div>

      <div v-if="roomInfo.condition != 0" class="user-info">
        <p class="title">预订人信息</p>
          <div class="info">
            <span>姓名：</span>
            <span>{{roomInfo.reserveInfo.name}}</span>
          </div>

        <div class="info">
          <span>邮箱：</span>
          <span>{{roomInfo.reserveInfo.email}}</span>
        </div>

        <div class="info">
          <span>时间：</span>
          <span>{{roomInfo.reserveInfo.date}}&ensp;{{roomInfo.reserveInfo.time}}</span>
        </div>

        <div class="info">
          <span>用途：</span>
          <p>{{roomInfo.reserveInfo.use}}</p>
        </div>
      </div>

      <div class="room-info">
        <p class="title">会议室信息</p>
        <div class="info">
          <span>地点：</span>
          <input type="text" placeholder="输入会议室地点" v-model="roomInfo.place"
            :disabled="roomInfo.condition != 0">
        </div>

        <div class="info">
          <span>容纳人数：</span>
          <input type="text" placeholder="输入会议室容纳人数" v-model="roomInfo.maxPeople"
            :disabled="roomInfo.condition != 0">
        </div>

        <div class="introduction">
          <p>会议室介绍</p>
          <textarea maxlength="-1" :rows="roomInfo.condition === 0 ? '10':'3'"
            v-model="roomInfo.introduction"
            placeholder="输入会议室介绍" :readonly="roomInfo.condition != 0">
          </textarea>
        </div>
      </div>

      <van-radio-group v-if="!addRoom" v-model="checkbox">
        <van-radio v-if="roomInfo.condition === 0" name="change" style="margin-bottom: 5px;"  checked-color="#42B983">修改</van-radio>
        <van-radio v-if="roomInfo.condition === 0" name="remove" style="margin-bottom: 5px;"  checked-color="#ee2626">删除</van-radio>

        <van-radio v-if="roomInfo.condition != 0" name="agree" style="margin-bottom: 5px;"  checked-color="#42B983">同意</van-radio>
        <van-radio v-if="roomInfo.condition === 1" name="refuse"  checked-color="#ee2626">拒绝</van-radio>
        <van-radio v-if="roomInfo.condition === 2" name="withdraw"  checked-color="#ee2626">撤回预定</van-radio>
      </van-radio-group>

      <div class="control">
        <div style="color: #cd2d2d;" @click="Close">取消</div>
        <span>|</span>

        <div style="color: #088573;" @click="Sure">
          确认
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default{
    data(){
      return{
        addRoom : false,
        checkbox : ''
      }
    },
    methods:{
      Sure(){//添加/修改信息
        if(this.addRoom) //添加新会议室
          this.AddRoom()
        else if(this.roomInfo.condition === 0)//修改
          this.ChangeRoom()
        else if(this.roomInfo.condition === 1)//处理新预定
          this.dealReserve()
        else if(this.roomInfo.condition === 2)//已预订处理
          this.AlreadyReserve()
      },
      AddRoom(){//添加
        this.$dialog.confirm({
          title : '提示',
          message: '确认添加新会议室',
          closeOnPopstate : true,
          closeOnClickOverlay : true,
          confirmButtonColor : '#088573',
          cancelButtonColor : '#cd2d2d',
          className : 'model'
        })
        .then(res => {
          global.showLoading(this,'添加中...')
          this.$axios.post('/MeetingRoom/manage/AddRoom',this.getRequestdata())
            .then(res => {
              if(res.data.status === 200){
                this.$emit('Sure',{
                  roomInfo : this.roomInfo,
                  way : 'Add'
                })
                global.showToast(this,'添加成功','success')
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
      ChangeRoom(){//修改/删除
        let check
        if(this.checkbox === 'change')
          check = '确认修改会议室信息?'
        else
          check = '确认删除该会议室?'
        this.$dialog.confirm({
          title : '提示',
          message: check,
          closeOnPopstate : true,
          closeOnClickOverlay : true,
          confirmButtonColor : '#088573',
          cancelButtonColor : '#cd2d2d',
          className : 'model'
        })
        .then(res => {
          if(this.checkbox === 'change'){
            global.showLoading(this,'修改中...')
            this.$axios.post('/MeetingRoom/manage/ChangeRoom',this.getRequestdata(this.roomInfo.ID))
              .then(res => {
                if(res.data.status === 200){
                  console.log(res.data)
                  this.$emit('Sure',{
                    roomInfo : this.roomInfo,
                    way : 'Change'
                  })
                  global.showToast(this,'修改成功','success')
                }
                else
                  console.log(res.data)
              })
              .catch(err => global.showToast(this,'网络错误','cross'))
          }
          else{
            global.showLoading(this,'删除中...')
            const data = new URLSearchParams()
            data.append('ID',this.roomInfo.ID)
            this.$axios.post('/MeetingRoom/manage/RemoveRoom',data)
              .then(res => {
                if(res.data.status === 200){
                  console.log(res.data)
                  this.$emit('Sure',{
                    roomInfo : this.roomInfo,
                    way : 'Remove'
                  })
                  global.showToast(this,'删除成功','success')
                }
                else
                  console.log(res.data)
              })
              .catch(err => global.showToast(this,'网络错误','cross'))
          }
        })
        .catch(res => {
          console.log(res)
        })
      },
      dealReserve(){//处理新预定
        let check
        if(this.checkbox === 'agree')
          check = '确认同意预定?'
        else
          check = '确认拒绝预定?'
        this.$dialog.confirm({
          title : '提示',
          message: check,
          closeOnPopstate : true,
          closeOnClickOverlay : true,
          confirmButtonColor : '#088573',
          cancelButtonColor : '#cd2d2d',
          className : 'model'
        })
        .then(res => {
          global.showLoading(this,'处理中...')
          const data = new URLSearchParams()
          data.append('roomID',this.roomInfo.ID)
          data.append('reserveID',this.roomInfo.reserveInfo.reserveID)
          if(this.checkbox === 'agree'){
            data.append('condition',2)
            this.$axios.post('/MeetingRoom/manage/DealReserve',data)
              .then(res => {
                if(res.data.status === 200){
                  console.log(res.data)
                  this.$emit('Sure',{
                    condition : 2,
                    way : 'Agree'
                  })
                  global.showToast(this,'已同意预定','success')
                }
                else
                  console.log(res.data)
              })
              .catch(err => global.showToast(this,'网络错误','cross'))
          }
          else{
            data.append('condition',0)
            this.$axios.post('/MeetingRoom/manage/DealReserve',data)
              .then(res => {
                if(res.data.status === 200){
                  console.log(res.data)
                  this.$emit('Sure',{
                    condition : 0,
                    way : 'Refuse'
                  })
                  global.showToast(this,'已拒绝预定','success')
                }
                else
                  console.log(res.data)
              })
              .catch(err => global.showToast(this,'网络错误','cross'))
          }
        })
        .catch(res => {
          console.log(res)
        })
      },
      AlreadyReserve(){//撤回预订
        if(this.checkbox != 'withdraw')
          this.$emit('Close',false)
        else
          this.$dialog.confirm({
            title : '提示',
            message: '确认撤回预定?',
            closeOnPopstate : true,
            closeOnClickOverlay : true,
            confirmButtonColor : '#088573',
            cancelButtonColor : '#cd2d2d',
            className : 'model'
          })
          .then(res => {
            global.showLoading(this,'处理中...')
            const data = new URLSearchParams()
            data.append('roomID',this.roomInfo.ID)
            data.append('reserveID',this.roomInfo.reserveInfo.reserveID)
            this.$axios.post('/MeetingRoom/manage/WithdrawRoom',data)
              .then(res => {
                if(res.data.status === 200){
                  console.log(res.data)
                  this.$emit('Sure',{
                    condition : 0,
                    way : 'Withdraw'
                  })
                  global.showToast(this,'已撤回预定','success')
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
      getRequestdata(ID=''){
        const data = new URLSearchParams()
        data.append('place',this.roomInfo.place)
        data.append('maxPeople',this.roomInfo.maxPeople)
        data.append('introduction',this.roomInfo.introduction)
        data.append('ID',ID)
        return data
      },
      Close(){
        this.$emit('Close',false)
      }
    },
    created(){
      if(this.roomInfo.place === '')
        this.addRoom = true
      if(this.roomInfo.condition === 0)
        this.checkbox = 'change'
      else if(this.roomInfo.condition != 0)
        this.checkbox = 'agree'
    },
    props:{
      roomInfo : Object
    }
  }
</script>

<style scoped>
  input{
    background: none;
    border: none;
    outline: none;
  }

  .room .remark{
    color: #999999;
    font-size: 13px;
    text-align: center;
  }
  .room .newRoom{
    font-size: 20px;
    text-align: center;
  }

  .info{
    border-bottom: 1px solid #42B983;
    margin-bottom: 10px;
    padding-bottom: 5px;
    display: flex;
    align-items: center;
  }

  .room .user-info{
    margin-top: 5px;
  }
  .room .user-info .title{
    font-weight: 600;
    margin: 5px 0;
  }
  .room .user-info p{
    flex: 1;
  }

  .room .room-info .title{
    font-weight: 600;
    margin: 5px 0;
  }
  .room .room-info input{
    flex: 1;
  }
  .room .room-info .introduction p{
    line-height: 1;
  }
  .room .room-info .introduction textarea{
    width: 100%;
    border-radius: 5px;
    border-color: #42B983;
    padding: 5px;
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
  		transform: translatey(-150px);
  	}
    100%{
    	opacity: 1;
    	transform: translateY(0);
    }
  }
</style>
