# 简介
本项目是业余时间开发的一个webshell  基于go语言开发  主要用于扩展通过cmdb平台登录到远程服务器和k8s内部环境  或者用于开发堡垒机都可以 目前本人主要在cmdb用来实时看日志和登录容器  

# 打包
```bash
make build_mac or make build_linux
```
# 本地运行
```bash

make run 
```
# 打包成docker
```bash
docker build -t huangchengwu6904/webshell .
```
# 演示

## 启动服务
docker run -p8080:8080 -p 3002:3002 -it huangchengwu6904/webshell 
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/运行服务.jpg)


## 运行kubectl 命令
http://127.0.0.1:8080/?Cmd=kubectl,logs,nginx,-n,default,-f&ws=127.0.0.1&LocalMode=yes
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/执行命令.jpg)

##### 运行本地终端
http://127.0.0.1:8080/?Cmd=/bin/sh&ws=127.0.0.1&LocalMode=yes
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/本地登录.jpg)

## 代理远程终端
http://127.0.0.1:8080/?Username=root&Password=Odej7fvOsYh@jh0nR0sa&Host=192.168.254.16:22&Cmd=/bin/bash&ws=127.0.0.1&LocalMode=no
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/代理登录.jpg)


# 扩展到cmdb
以下开发可以登录到容器  主要排查容器内部网络是否没问题  还有就是实时看日志
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/cmdb任务功能.jpg)



##  看日志
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/日志查看.jpg)

##  登录容器
 ![演示图片](https://gitee.com/huangchengwu/fortress/raw/master/demo-img/登录容器.jpg)







