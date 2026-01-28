## EasyApi-简易管理接口的面板

> 本项目由django开发，用于创建一个简易管理层面的api接口服务。

首页：

![](public/index.png)

api列表页：

![](public/apihub.png)

套餐页：

![](public/plan.png)

个人中心：

![](public/profile.png)


后台：

![](public/admin.png)

### 项目介绍：

例如你有个**项目**功能是生成小说，你需要将这个功能提供到互联网上并**希望是一部分人可用**(免费API容易泛滥导致影响成本)，所以需要个管理系统，需要用户注册登录才可用。

每个项目都会有**多个接口**，例如生成恐怖小说是接口a，生成玄幻小说是接口b。每个接口独立设置接口价格、请求方式、响应内容，以及**对应的函数**等。

点数相当于是**计费**用的，每个用户都会有点数，每次访问接口都会**根据接口函数返回的状态码是否为200来决定是否扣除点数**。当接口的函数执行失败，返回了非200状态码则不扣用户的 `点数` 。


内置功能：EasyApi实现了用户登录、注册、后台管理(django后台)、套餐显示、项目与接口的创建、项目与接口的显示/隐藏，页面采用响应式布局。


> `util/apis.py` 文件添加你的自定义脚本

每个函数都需要返回一个字典，字典中需要包含 `code:整数状态码` ，因为接口的函数有可能执行失败，失败后就不扣除用户的 `点数` 了（优化用户体验）。

例如：

```python
    return data = {
        'code': 200,
        'data':'abcd',
        'info':'调试成功'
    }
```

### 常规部署

需要提前创建mysql数据库

```shell
cd /home
git pull https://github.com/Rx5557770/EasyApi.git
cd EasyApi
```

克隆本项目后，运行 `pip install -r requirements.txt` 安装依赖

运行 `python -c "import secrets; print(secrets.token_hex(32))"` 获取key。

在项目目录下编写 `.env` 文件 替换 `your_django_secret_key_here` 为刚刚复制的key。

```dotenv
# Django 基础配置
DEBUG=False
SECRET_KEY=your_django_secret_key_here

# MySQL 数据库配置
ENGINE=django.db.backends.mysql
MYSQL_DATABASE=api_db
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=your_db_password_here
DB_HOST=127.0.0.1
DB_PORT=3306

# 允许的域名和IP
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost
```

安装完成后运行 `python manage.py migrate` 执行迁移创建数据表。
创建超级管理员 `python manage.py createsuperuser`

显示页面到浏览器，需要配置nginx

在nginx中（/etc/nginx/conf.d/）添加配置文件 easyapi.conf
```nginx
server {
    listen 80; # 监听端口
    server_name localhost 127.0.0.1; # 域名
    
    # url匹配然后走反向代理
    location / {
        proxy_pass http://localhost:8000;
    }
    
    location /static/ {
        alias /home/EasyApi/staticfiles/;
    }
}

```

运行服务器 `gunicorn config.wsgi:application --bind 0.0.0.0:8000`

访问 `/admin` 后台。

### Docker + Docker-Compose

> 保证环境是干净的，否则可能部署失败。此方法不需要手动创建mysql库

```shell
# 安装
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 设置开机自启
sudo systemctl start docker
sudo systemctl enable docker
```

拉取项目
```shell
cd /home
git pull https://github.com/Rx5557770/EasyApi.git
cd EasyApi
```

编写 `.env` 文件

```dotenv
# Django 基础配置
DEBUG=False
SECRET_KEY=your_django_secret_key_here

# MySQL 数据库配置
ENGINE=django.db.backends.mysql
MYSQL_DATABASE=api_db
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=your_db_password_here
DB_HOST=127.0.0.1
DB_PORT=3306

# 允许的域名和IP
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost
```

运行 `docker-compose up -d`

然后配置nginx，在 `/etc/nginx/conf.d` 中添加 `EasyApi.conf`

```nginx
server {
    listen 80; # 监听端口
    server_name localhost 127.0.0.1; # 域名
    
    # url匹配然后走反向代理
    location / {
        proxy_pass http://easyapi:8000;
    }
    
    location /static/ {
        alias /usr/share/nginx/staticfiles;
    }
}

```

enjoy my first project!