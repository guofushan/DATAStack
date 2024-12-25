import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import layout from '@/components/layout'
import yunwei_center from '@/components/yunwei_center'
import mysql_instance from '@/components/mysql_instance'
import mysql_adduser from '@/components/mysql_adduser'
import mysql_dbcreate from '@/components/mysql_dbcreate'
import mysql_layout from '@/components/mysql_layout'
import mysql_slowlog from '@/components/mysql_slowlog'
import mysql_detail from '@/components/mysql_detail'
import mysql_monitor from '@/components/mysql_monitor'
import mysql_binlog2sql from '@/components/mysql_binlog2sql'
import mysql_topsql from '@/components/mysql_topsql'
import mysql_bakdetail from '@/components/mysql_bakdetail'
import mysql_setmodify from '@/components/mysql_setmodify'
import redis_layout from '@/components/redis_layout'
import redis_instance from '@/components/redis_instance'
import redis_detail from '@/components/redis_detail'
import redis_monitor from '@/components/redis_monitor'
import redis_adduser from '@/components/redis_adduser'
import mysql_table_size from '@/components/mysql_table_size'
import pg_instance from '@/components/pg_instance'
import pg_layout from '@/components/pg_layout'

Vue.use(Router)

const router = new Router({
	mode: 'history',
	routes: [{
			path: '/',
			name: 'helloworld',
			component: HelloWorld
		},
		{
			path: '/home',
			name: 'home',
			component: layout,
			children: [
			
				{
					path: 'mysql_setmodify',
					component: mysql_setmodify
				},
				{
					path: 'mysql_instance',
					component: mysql_instance
				},
				{
					path: 'redis_instance',
					component: redis_instance
				},
				{
					path: 'yunwei_center',
					component: yunwei_center
				},	
				{
					path: 'mysql_adduser',
					component: mysql_adduser
				},
				{
					path: 'pg_instance',
					component: pg_instance
				}
				
			]
		},
		{
			path: '/home/mysql',
			name: 'home2',
			component: mysql_layout,
			children: [
				
				{
					path: 'mysql_adduser',
					component: mysql_adduser
				},
				{
					path: 'mysql_dbcreate',
					component: mysql_dbcreate
				},
				{
					path: 'mysql_slowlog',
					component: mysql_slowlog
				},
				{
					path: 'mysql_detail',
					component: mysql_detail
				},
				{
					path: 'mysql_monitor',
					component: mysql_monitor
				},
				{
					path: 'mysql_binlog2sql',
					component: mysql_binlog2sql
				},
				{
					path: 'mysql_topsql',
					component: mysql_topsql
				},
				{
					path: 'mysql_bakdetail',
					component: mysql_bakdetail
				},
				{
					path: 'mysql_table_size',
					component: mysql_table_size
				},
				
			]
		},
		{
			path: '/home/redis',
			name: 'home3',
			component: redis_layout,
			children: [
		
				{
					path: 'redis_detail',
					component: redis_detail
				},
				{
					path: 'redis_monitor',
					component: redis_monitor
				},
				{
					path: 'redis_adduser',
					component: redis_adduser
				},
				
			]
		},
		{
			path: '/home/pg',
			name: 'home4',
			component: pg_layout,
			children: [
				{
					path: 'mysql_detail',
					component: mysql_detail
				},
				{
					path: 'mysql_monitor',
					component: mysql_monitor
				},
			
				
			]
		},
	]
})


router.beforeEach((to, from, next) => {
	if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
		if (localStorage.token) { // 获取当前的token是否存在
			next();
		} else {
			next({
				path: '/', // 将跳转的路由path作为参数，登录成功后跳转到该路由
				query: {
					redirect: to.fullPath
				}
			})
		}
	} else { // 如果不需要权限校验，直接进入路由界面
		next();
	}
});

export default router;
