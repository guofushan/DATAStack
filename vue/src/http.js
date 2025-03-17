import axios from 'axios';
import router from './router';
import qs from 'qs'

// axios 配置
// axios.defaults.timeout = 10000;

// http request 拦截器
axios.interceptors.request.use(
	config => {
		if (localStorage.token) { //判断token是否存在
			config.headers.Authorization = localStorage.token; //将token设置成请求头
		}
		if (config.method === 'post') {
			//将请求参数进行转换，这里是全局配置post请求参数
			config.data = qs.stringify(config.data)
		}
		return config;
	},
	err => {
		return Promise.reject(err);
	}
);

// http response 拦截器
axios.interceptors.response.use(
	response => {
		if (response.data.status === 'timeout') {
			router.replace('/');
			//console.log("token过期");
		}
		return response;
	},
	error => {
		return Promise.reject(error);
	}
);
export default axios;
