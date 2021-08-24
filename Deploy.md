## 预备操作
### 手动配置:
#### 1. 设置mysql服务器
```sql
mysql> create database asoulcnki;
mysql> use asoulcnki;
mysql> source cnki.sql;
```
#### 2. 设置redis服务器
略  
### 自动配置:
参见[ASoulCnkiBackend](https://github.com/ASoulCnki/ASoulCnkiBackend)中操作
## 爬虫机器操作(可在多台机器上部署)
### 1. 下载爬虫端代码  
```bash
git clone https://github.com/ASoulCnki/ASoulCnki
cd ASoulCnki
```
### 2. 安装依赖
```bash
pip3 install -r requirements.txt
```
### 3. 更改配置文件
将 `app/config` 下 `secure_demo.py` 复制(或重命名)为 `secure.py`

```bash
mv app/config/secure_demo.py app/config/secure.py
vim app/config/secure.py
```

#### 3.1 配置文件需要修改的项
1. member_ids 爬取评论区对应的 uid

2. mysql 连接配置 (用户名 密码 地址 端口 数据库)

3. redis 连接配置 (密码 端口)

4. 爬虫异常邮件提醒(可选, 请自行更换自己的邮箱的对应的配置)

5. 后端信息 (如需使用请按照[后端项目](https://github.com/AsoulCnki/AsoulCnkiBackEnd)自行搭建并更换为自己的配置)

连接配置需修改的项使用 `[]` 做了标注, 例如 `[host]`, **请将相关配置信息修改为自己的配置信息(去掉括号)**, 下面是一个范例

```py
# 原配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[username]:[password]@[host]:[port]/[database]"
# 修改为
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/asoulcnki"
```

> 值得注意的是，发送邮件使用的是SMTP, 所以配置邮箱 `mail_license` 的 **并不是登陆邮箱的密码**
>
>  具体如何获取SMTP的 `mail_license` 并启用, 请咨询您的邮件服务提供商

### 4. 启动爬虫
#### 4.1 初始化操作:
启动worker:
```bash
celery -A tasks worker -l info
```
爬取并初始化动态和评论:
```bash
vim start.py # 修改爬取用户id
python3 start.py init_dynamic
python3 start.py init_reply
```
#### 4.2 爬取操作:
自动化爬取:
```bash
celery -A tasks beat -l info
```
手动爬取:
```bash
python3 start.py update_database
```
#### 4.3 一键启停
```bash
chmod +x start.sh stop.sh
./start.sh # 启动爬虫 日志默认在项目路径下 nohup.out
./stop.sh # 停止爬虫
```