import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import http from './http';  //此处问http文件的路径
import md5 from 'js-md5';
import './plugins/element.js'
import store from './store'

Vue.use(ElementUI)
Vue.prototype.$http = http;
Vue.prototype.$md5 = md5;

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  store,
  router
}).$mount('#app')

