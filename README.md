# Pampa
Base Flask CMS for Blog  Python 



# 开发初衷

一个使用Flask开发的**轻量博客**系统，麻雀虽小但五脏也快长全了，功能一直都会不断更新...，你也可以先睹为快地址：

## 用到的技术

- python

- flask

- flask-wtf

- flask-sqlalchemy

- bootstrap4

- 支持mysql等

- 数据库默认使用mysql，

- TinyMCE编辑器

  

## 博客功能

- 撰写文章
- 文章列表
- 文章分类
- 标签管理

## 下一版本机会 To Do

- 推荐文章 [To Do]
- 网站设置  [To Do]
- 会员注册  [To Do]
- 邀请码   [To Do]
- Diy定制模板   [To Do]
- 单页系统 [To Do]



## SEO功能

完全符合SEO  系统结构优化的同时内置多种SEO设置，对网站URL路径设置自由度极高，可自由灵活设置网站的URL，让你的网站免费在搜索引擎中获得好的排名。

> 下一个版本计划
>
> 1. 简单文字图片创造  [To Do]
> 2. 百度推送  [To Do]
> 3. 搜索引擎抓取统计   [To Do]





## 运行

```shell
$ git clone git@github.com:lovebull/Pampa.git
$ cd Pampa
$ python -m venv venv  #创建python虚拟环境
$ source venv/bin/activate
$ 
$ pip install -r requirements.txt # 安装项目依赖，可能不全，根据提示自行安装即可
$ flask initdb #创建数据库
$ export FLASK_ENV=development
$ flask run # 启动
```
