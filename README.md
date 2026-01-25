## EasyApi

> 本项目由django开发，用于创建一个简易管理层面的api接口服务。

例如你有个**项目**功能是生成小说，你需要将这个功能提供到互联网上并**希望是一部分人可用**(免费API容易泛滥导致影响成本)，所以需要个管理系统，需要用户注册登录才可用。

每个项目都会有**多个接口**，例如生成恐怖小说是接口a，生成玄幻小说是接口b。每个接口独立设置接口价格、请求方式、响应内容，以及**对应的函数**等。

点数相当于是**计费**用的，每个用户都会有点数，每次访问接口都会**根据接口函数返回的状态码是否为200来决定是否扣除点数**。当接口的函数执行失败，返回了非200状态码则不扣用户的 `点数` 。


内置功能：EasyApi实现了用户登录、注册、后台管理(django后台)、套餐显示、项目与接口的创建、项目与接口的显示/隐藏，页面采用响应式布局。


> `util/apis.py` 文件添加你的自定义脚本后在 `dashboard/views.py` 中找到 `todo` 函数，在其内部根据接口id调用函数即可。

每个函数都需要返回一个字典，字典中需要包含 `code:整数状态码` ，因为接口的函数有可能执行失败，失败后就不扣除用户的 `点数` 了（优化用户体验）。

例如：

```python
    return data = {
        'code': 200,
        'data':'abcd',
        'info':'调试成功'
    }
```

### 使用教程
克隆本项目后，在项目目录下编写 `.env` 文件

```dotenv
# Django 基础配置
DEBUG=True
SECRET_KEY=your_django_secret_key_here

# MySQL 数据库配置
ENGINE=django.db.backends.mysql
DB_NAME=api_db
DB_USER=your_db_username_here
DB_PASSWORD=your_db_password_here
DB_HOST=127.0.0.1
DB_PORT=3306
```
运行 `pip install -r requirements.txt` 安装依赖

安装完成后运行 `python manage.py migrate` 执行迁移创建数据表。

创建超级管理员 `python manage.py createsuperuser`

最后 `python manage.py runserver` 访问 `/admin` 后台。

enjoy my first project!