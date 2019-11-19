import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

import axios from 'axios'
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
Vue.prototype.$axios = axios//全局使用axios

import { Toast } from 'vant';
import { Button } from 'vant';
import { RadioGroup, Radio } from 'vant'
import { Dialog } from 'vant';
import { Popup } from 'vant';
import { DatetimePicker } from 'vant';
Vue.use(Toast).use(Button).use(RadioGroup).use(Radio).use(Dialog).use(Popup).use(DatetimePicker);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
