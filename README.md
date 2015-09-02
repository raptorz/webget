# webget

一个web版离线下载工具，用于在服务端进行下载操作，功能类似网盘的离线下载工具。

## 基本功能

1. 列出当前进行的下载任务，任务参数包括：文件名（含URL），大小，进度（如完成则为下载链接），删除任务（已完成或已取消）、重启任务（已失败或已取消）和取消任务（进行中）
1. 增加下载任务，提供两个参数：一个是URL，一个是文件名（默认通过URL解析而来，可能不正确）

## 安装

    pkg install wget # for FreeBSD
    pip install -r requirements.txt
    python webget.py

## 配置

配置文件为当前目录下的config.json，内容为：

    {
        "down_dir" : "下载目录，默认为：~/down",
        "wget_dir" : "wget所在的目录，默认为：/usr/local/bin",
        "web_down" : "webserver的下载路径，默认为/webdown，配置webserver映射到下载目录",
        "web_path" : "webserver的webget路径，默认为/wget",
        "web_addr" : "绑定的IP，默认为：0.0.0.0，允许所有地址访问，如有可作反向代理的webserver，建议改为127.0.0.1",
        "web_port" : "绑定的端口，默认为：8111",
        "debug"    : "默认为False",
    }

反向代理的配置：

* nginx:

    location /wget {
        proxy_pass http://127.0.0.1:8111;
        include        wsgi_params;
    }

    location /webdown {
        root /path_to/webget;
        index index.html;
        autoindex off;
    }

注意：网访问建议使用https加basic auth",

## 依赖

* wget
* python 2.7+ or python 3.4+（其它版本未测试）
* bottle, mako, requests
* 可选webserver前端（Apache/Nginx...）

## 贡献

程序代码中包含以下第三方前端库：

* jquery
* bootstrap
* bootstrap-material-design
* jquery-validation
