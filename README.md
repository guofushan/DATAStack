<div align="center">

<h1 style="border-bottom: none">
    <b>DATAStack</b><br />
        一款免费的数据库私有云
    <br>
</h1>
<p>
开箱即用的企业级数据库私有云平台<br />
本地部署，安全高效，数据库私有云平台，公有云RDS替代，下云首选，完全免费
</p>
</div>
<div align="center">

![](https://img.shields.io/badge/-x86_x64%20ARM%20Supports%20%E2%86%92-rgb(84,56,255)?style=flat-square&logoColor=white&logo=linux)
[![OSCS Status](https://www.oscs1024.com/platform/badge/cookieY/Yearning.svg?size=small)](https://www.murphysec.com/dr/nDuoncnUbuFMdrZsh7)

![LICENSE](https://img.shields.io/badge/license-AGPL%20-blue.svg)

</div>

# DATAStack是什么
DATAStack是一款数据库私有云平台，为企业用户提供数据库即服务（DBaaS）的产品。产品已覆盖MySQL、Redis、MongoDB，可无缝运行在ZStack、华为云、DaoCloud、华云数据、浪潮云、VMware等私有云IaaS平台。帮助企业快速构建稳定、安全、经济的全场景数据库解决方案。

# 产品优势
- **降低成本** -对比各数据库厂商，DATAStack完全免费；使用DATAStack能够降低数据库基础建设使用成本。
- **多云融合** - 可无缝运行在ZStack、华为云、DaoCloud、华云数据、浪潮云、VMware等私有云IaaS平台。
- **跨基础设施的平台服务** - 灵活部署，良好的跨平台性，可运行在物理服务器或虚拟机中，支持多种Linux操作系统。
- **安全高效** - 本地化部署DATAStack，一键拉起数据库高可用集群。
- **低耦合** - DATAStack与数据库服务低耦合关系，在极端情况下数据库稳定性不受DATAStack平台影响。

# 产品功能
- **数据库引擎服务** - 支持主流数据库MySQL、Redis、MongoDB。
- **集群创建** - 支持数据库实例一键部署。
- **数据库监控** - 内置OS、DB层链路监控模块。
- **自动备份** - 支持自定义备份策略，确保数据安全一致稳定。
- **高可用** - 秒级探测和切换，90%连接保持无影响。
- **权限管理** - 支持页面化管理，创建用户、角色授权。
- **日志查看** - 支持页面汇总展示近期慢SQL。
- **Binlog回滚** - 支持页面操作解析binlog生成相应的SQL和回滚SQL。
- **TOP SQL** - 汇总展示SQL执行频率统计，协助数据库性能诊断排查。



# 在线试用
- [点击在线体验](http://59.110.126.94:8004/)

**登录信息**
|user|password|
|---|---|
|admin|rootroot|

# 安装

### Docker

```bash
# 1.下载配置文件
## Github下载
wget -P /usr/local/src https://github.com/guofushan/DATAStack/releases/download/v1.1/datastack.cfg
## 或者Gitee下载
wget -P /usr/local/src https://gitee.com/guofushan/DATAStack/releases/download/v1.1/datastack.cfg

# 2.修改配置文件
vi /usr/local/src/datastack.cfg

[section]
#后端mysql数据源信息
mysqlip=192.168.56.1
mysqluser=yunwei
mysqlport=35972
mysqlpwd=123456
#os用户密码
root_user=root
root_pwd=123456
#告警邮箱
report_email=['1031059192@qq.com']
#datastack部署节点ip
datastack_ip=192.168.56.1

# 3.创建DB并授权(在后端mysql数据源操作)
create database yandi;
grant all on *.* to yunwei@'%' identified by '123456';
flush privileges;

# 4.容器启动 (需提前部署docker服务)
docker run -d -v /usr/local/src/datastack.cfg:/app/datastack.cfg -it -p 8004:8004 -p 5001:5001 -p 9090:9090 -p 9093:9093 -p 3000:3000 -p 3001:3001 registry.cn-beijing.aliyuncs.com/datastack/datastack:latest

# 5.访问 DATAStack平台
http://部署节点IP:8004

```
# 页面概况
![11](https://github.com/guofushan/DATAStack/assets/48540932/1ac2cd3c-f7d6-4cfc-9100-2304ab04766f)
![clipboard4](https://github.com/guofushan/DATAStack/assets/48540932/0b23513b-9a12-43d8-aaf7-d1381fa7fda6)
![clipboard1](https://github.com/guofushan/DATAStack/assets/48540932/7daf1014-cea4-4bab-8c3d-4d232b40acf8)
![1](https://github.com/guofushan/DATAStack/assets/48540932/ece697ea-c461-4dc7-bcfc-18c9f9d60fed)
![2](https://github.com/guofushan/DATAStack/assets/48540932/3c10e361-bd13-47e1-82d8-6d316de2ea56)

# 问题反馈
- Bug提交：[Issues](https://github.com/guofushan/DATAStack/issues)


# 联系我们
DATAStack 使用交流QQ群:  775117644 <br />

