<template>
  <div class="room-detail">
    <div class="mask"></div>

    <div class="room">
      <h4>会议室预定</h4>

      <div class="room-info">
        <div class="info">
          <span>地点：{{roomInfo.place}}</span>
        </div>

        <div class="info">
          <span>容纳人数：{{roomInfo.maxPeople}}</span>
        </div>

        <div class="introduction">
          <span>会议室介绍</span>
          <p>{{roomInfo.introduction}}</p>
        </div>
      </div>

      <div class="user-info">
        <span class="title">预订人信息</span>
          <div class="info unchange">
            <span>姓名：{{UserInfo.name}}</span>
          </div>

        <div class="info unchange">
          <span>邮箱：{{UserInfo.email}}</span>
        </div>

        <div class="info">
          <span>日期：</span>
          <div @click="picker('date')">
            <p style="color: #969799;" v-if="!reserveInfo.date">
              选择预定日期
            </p>
            <p v-else>{{reserveInfo.date}}</p>
          </div>
        </div>

        <div class="info">
          <span>时间：</span>
          <div @click="picker('startTime')">
            <p style="color: #969799;" v-if="!reserveInfo.time">
              选择使用的时间
            </p>
            <p v-else>{{reserveInfo.time}}</p>
          </div>
        </div>

        <div class="use">
          <div>用途</div>
          <textarea maxlength="-1" rows="4"
            v-model="reserveInfo.use" placeholder="输入预定会议室的用途">
          </textarea>
        </div>
      </div>

      <div class="control">
        <div style="color: #cd2d2d;" @click="Close">取消</div>
        <span>|</span>
        <div style="color: #088573;" @click="Sure">预定</div>
      </div>
    </div>

    <!-- 选择器 -->
    <van-popup
      v-model="pickering"
      position="bottom"
      :style="{ height: '35%' }"
    >
      <!-- 选择日期 -->
      <van-datetime-picker
        v-if="pickerType === 'date'"
        v-model="currentDate"
        type="date"
        title='选择预定时间'
        :min-date="minDate"
        @confirm="ChooseDate"
        @cancel="pickering=false"
      />
      <!-- 选择时间 -->
      <van-datetime-picker
        v-if="pickerType === 'startTime' || pickerType === 'endTime'"
        v-model="startTime"
        type="time"
        :title="timeTitle"
        @confirm="ChooseTime"
        @cancel="pickering=false"
      />
    </van-popup>
  </div>
</template>

<script>
  var time = ''
  export default{
    data(){
      return{
        currentDate : new Date(),
        minDate: new Date(),
        startTime : '12:30',
        timeTitle : '选择开始时间',

        pickering : false,
        pickerType : '',

        reserveInfo : {}
      }
    },
    methods:{
      picker(type){
        this.pickerType = type
        this.pickering = true
        if(type === 'startTime')
          global.showToast(this,'开始时间','clock-o')
      },
      ChooseDate(e){//选择日期
        this.reserveInfo.date = `${e.getFullYear()}/${e.getMonth()+1}/${e.getDate()}`
        this.pickering = false
      },
      ChooseTime(e){
        if(this.pickerType === 'startTime'){
          this.pickerType = 'endTime'
          time = time + e +' - '
          global.showToast(this,'结束时间','underway-o')
        }
        else{
          this.pickerType = 'startTime'
          time += e
          this.reserveInfo.time = time
          time = ''
          this.pickering = false
        }
      },
      Sure(){//确认
        if(!this.reserveInfo.date)
          global.showToast(this,'请选择日期','cross')
        else if(!this.reserveInfo.time)
          global.showToast(this,'请填写时间','cross')
        else
          this.$dialog.confirm({
            title : '提示',
            message: '确认预定会议室?',
            closeOnPopstate : true,
            closeOnClickOverlay : true,
            confirmButtonColor : '#088573',
            cancelButtonColor : '#cd2d2d',
            className : 'model'
          })
          .then(() => {
            // 数据请求,修改该会议室状态，添加用户预订状态
						global.showLoading(this,'预订中...')

            this.reserveInfo.name = this.UserInfo.name
            this.reserveInfo.email = this.UserInfo.email
						const data = new URLSearchParams()
						data.append('roomInfo',JSON.stringify(this.roomInfo))
						data.append('reserveInfo',JSON.stringify(this.reserveInfo))
            data.append('email',this.UserInfo.email)

            this.$axios.post('/MeetingRoom/reserve/ReserveRoom',data)
              .then(res => {
                if(res.data.status === 200){
                  this.$emit('Sure','reserve')
                }
                else{//预定失败
                  global.showToast(this,res.data.text,'cross')
                  setTimeout(() => {
                    this.$emit('Sure','getInfo')
                  },1500)
                  console.log(res.data)
                }
              })
              .catch(err => global.showToast(this,'网络错误','cross'))
          })
          .catch(res => {
            console.log(res)
          })
      },
      Close(){
        this.$emit('Close',false)
      }
    },
    props:{
      roomInfo : Object,
      UserInfo : Object
    }
  }
</script>

<style scoped>
  p{
    margin: 0;
  }
  input{
    background: none;
    border: none;
    outline: none;
  }

  .room h4{
    font-size: 20px;
    text-align: center;
  }

  .info{
    border-bottom: 1px solid #42B983;
    margin-bottom: 5px;
    line-height: 1.5;
    display: flex;
    align-items: center;
  }

  .room .room-info .introduction p{
    min-height: 50px;
    border: 1px solid #42B983;
    border-radius: 5px;
    padding: 5px;
  }

  .room .user-info{
    margin-top: 5px;
  }
  .room .user-info .title{
    font-weight: 600;
    margin: 0;
  }
  .room .user-info .unchange{
    background: rgba(205,205,205,0.3);
  }
  .room .user-info .info div{
    flex: 1;
  }
  .room .user-info .use textarea{
    width: 100%;
    border: 1px solid #42B983;
    border-radius: 5px;
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
