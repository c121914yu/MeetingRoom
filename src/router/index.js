import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

import Home from '../pages/User/home'

import Manager from '../pages/Manager/manager'

import Login from '../pages/Login/login'
import FindPsw from '../pages/Login/findpsw'
import Register from '../pages/Login/register'
import ManagerLogin from '../pages/Login/managerLogin'

export default new Router({
  routes: [
    {path:'*',redirect:'/'},//错误地址重新定向
    {path: '/',name: 'home',component: Home},

    {path: '/manager',name: 'manager',component: Manager},

    {path: '/login',name: 'login',component: Login},
    {path: '/findpsw',name: 'findpsw',component: FindPsw},
    {path: '/register',name: 'register',component: Register},
    {path: '/login/manager',name: 'managerLogin',component: ManagerLogin},
  ],
})
