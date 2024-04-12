<div align="center">

<h1 style="border-bottom: none">
    <b>DATAStack</b><br />
        安全, 高效的MySQL RDS
    <br>
</h1>
<p>
一款开箱即用的公有云RDS替代者<br />
本地部署，安全高效，私有云数据库服务，公有云RDS 替代
</p>
</div>
<div align="center">

![](https://img.shields.io/badge/-x86_x64%20ARM%20Supports%20%E2%86%92-rgb(84,56,255)?style=flat-square&logoColor=white&logo=linux)
[![OSCS Status](https://www.oscs1024.com/platform/badge/cookieY/Yearning.svg?size=small)](https://www.murphysec.com/dr/nDuoncnUbuFMdrZsh7)

![LICENSE](https://img.shields.io/badge/license-AGPL%20-blue.svg)

</div>

## DATAStack是什么
- **降低成本** - 对比公有云RDS的价格，使用DATAStack能够大大降低数据库使用成本，降幅在50%。
- **安全高效** - 本地化部署DATAStack，一键拉起数据库高可用集群。
- **低耦合** - DATAStack与数据库服务低耦合关系，在极端情况下数据库稳定性不受DATAStack平台影响。

## 功能
- **创建数据库实例** - 支持MySQL单实例/高可用实例一键部署。
- **创建DB** - 支持数据库创建、查看功能。
- **权限管理** - 支持页面化操作：创建用户、角色授权。
- **日志查看** - 支持页面汇总展示近期慢SQL。
- **Binlog回滚** - 支持页面操作解析binlog生成相应的SQL和回滚SQL。
- **TOP SQL** - 汇总展示SQL执行频率统计，协助数据库性能诊断排查。
- **数据库监控** - 内置linux、MySQL监控模块。
- **备份恢复** - 内置数据库备份模块，保证数据一致稳定。
- **MySQL高可用** - 集成Orchestrator、Consul服务，做到故障灵活切换，服务不宕机。
- **定时任务** - 内置定时任务模块，可通过页面配置定时任务。

## 在线试用
- [点击在线体验](http://10.88.28.13:8004/)

**登录信息**
|user|password|
|---|---|
|admin|rootroot|

## 安装

#### Docker

```bash
## 下载配置文件
wget -P /usr/local/src https://github.com/guofushan/DATAStack/releases/download/v1.1/datastack.cfg

## 修改配置文件
vi /usr/local/src/datastack.cfg

[section]
#定义后端mysql数据源信息
mysqlip=192.168.56.1
mysqluser=yunwei
mysqlport=35972
mysqlpwd=123456
#定义os用户密码
root_user=root
root_pwd=123456
#告警邮箱
report_email=['1031059192@qq.com']
#定义datastack部署节点ip
datastack_ip=192.168.56.1

## 容器启动
docker run -d -it guofushan/testos /bin/bash

# 访问 DATAStack平台
http://部署节点IP:8004
```
## 页面概况
![image](https://github.com/guofushan/DATAStack/assets/48540932/f87aa1cf-b8f1-46c1-9b48-5fae55d8b2f9)
![image](https://github.com/guofushan/DATAStack/assets/48540932/d8ae85cf-545c-4c0d-be32-b5ce1acc51c9)

</p>


## 联系我们

E-mail: 1031059192@qq.com

DATAStack 使用交流QQ群:  775117644 <br />

