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
```bash
mv app/config/secure_demo.py app/config/secure.py
vim app/config/secure.py
```
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