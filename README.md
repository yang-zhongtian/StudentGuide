# 北京十一学校2020.9开学典礼在线学生手册
寰桐阁 HCC Computer Community, Richard Yang
## [Gitee](https://gitee.com/bjbnds/StudentGuide) [Github](https://github.com/yangzhongtian001/StudentGuide)
![mit-licence](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)
![python](https://img.shields.io/badge/python-%3E%3D%203.5-blue)
![platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-blue)
![branch](https://img.shields.io/badge/branch-master-brightgreen.svg?longCache=true)
[![gitee](https://gitee.com/bjbnds/StudentGuide/badge/star.svg?theme=dark)](https://gitee.com/bjbnds/StudentGuide/stargazers)
[![github](https://img.shields.io/github/stars/yangzhongtian001/StudentGuide?logo=github&color=brightgreen)](https://github.com/yangzhongtian001/StudentGuide/stargazers)
[![github contributors](https://img.shields.io/github/contributors/yangzhongtian001/StudentGuide?logo=github)](https://github.com/yangzhongtian001/StudentGuide/stargazers)
## 基本架构
Python-Flask + MongoDB(CE)
## 第三方依赖
| 名称 | 用途 |
| ---- | ---- |
| flask | WEB框架 |
| flask_pymongo | flask mongodb连接扩展 |
| flask_wtf | CSRF保护 |
| requests | 云校登录 |
| pycrypto | 外置登录验证 |
## 目录结构
    |-log 日志文件存放
    |-static 静态文件目录
      |-img 图片静态，主要为弹幕页背景备份
      |-css
      |-js
    |-template 渲染模板
    |-main.py 网站主程序
    |-config.py 网站配置文件
    |-unicorn.py gunicorn配置文件
## 版本迭代
* v1 纯前端半成品，已托管至Gitee Pages
* v2 完整版，为2020.9 开学典礼提供服务
* v3 精简修改版（当前版本），只保留弹幕功能，修改显示方案为列表，为2020.9.10感恩日提供留言服务 
## 已知BUG
* [ ] Chrome浏览器禁止弹幕页音乐自动播放，目前没有解决方法。
## 注意事项
* ~~大部分静态文件均已托管至Github，使用jsdelivr加载~~static目录服务器nginx处理
* 当前版本未使用Flask-Cache，请在nginx处设置静态缓存
* ~~未防高并发请在nginx处限流~~已限制请求量
* 解释权归北京十一学校寰桐阁技术联盟HCC网络技术社所有
* 本项目使用MIT开源协议

Enjoy :)

