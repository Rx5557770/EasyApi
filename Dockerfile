FROM python:3.11.14-slim

# 容器的工作目录
WORKDIR /app

# 关闭 Python 输出缓冲，日志实时打印
ENV PYTHONUNBUFFERED=1
# 不生成 .pyc 文件，减小镜像体积
ENV PYTHONDONTWRITEBYTECODE=1


# 系统依赖安装后，再复制项目依赖清单
COPY requirements.txt /app

# 再运行依赖安装命令
RUN pip install --no-cache-dir -r requirements.txt

# 依赖安装后，复制本地代码到容器内
COPY . .

# 声明对外暴露端口
EXPOSE 8000

# 容器启动时运行的命令
CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000"]