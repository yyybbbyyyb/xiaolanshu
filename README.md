# xiaolanshu

- 可能得要求python3.8以上的版本
- 不要在本地pip，在虚拟环境中pip
  - 及时更新requirements.txt，保证项目可运行

### 创建虚拟环境
- 虚拟环境创建+进入

```bash
python3 -m venv venv

source venv/bin/activate
```

- 安装依赖

```bash
pip install -r requirement.txt
```


### 创建配置文件
- 在项目根目录下创建一个`config.yaml`文件
- 配置文件内容如下，需要修改的只是本机数据库的用户名密码
  - 阿里云oss的账号密码，Django的密码，AI_KEY问我私下要
```yaml
# database
database:
  engine: 'django.db.backends.mysql'
  name: 'xiaolanshu'
  host: 'localhost'
  port: '3306'
  user: ''
  password: ''


# aliyun oss
oss:
    oss_access_key_id: ""
    oss_access_key_secret: ""
    oss_end_point: "oss-cn-beijing.aliyuncs.com"
    oss_bucket_name: "buaaxiaolanshu"
    oss_bucket_alc_type: "public-read"
    oss_prefix_url: "https://"

# secret
django_secret_key: ''

# AI
ai_api_key: ""
```

### 迁移数据库
- 在项目根目录下运行
- 会自动创建数据库，表，可在本地查看下
```bash
python manage.py makemigrations
python manage.py migrate
```

### 建立搜索引擎表
- 在项目根目录下运行
- 会自动创建搜索引擎表，可在本地查看下
```bash
python manage.py rebuild_index
```

### 创建超级用户
- 在项目根目录下运行
- 会提示输入用户名，邮箱，密码
- 此账户可用于登录后台管理系统
```bash
python manage.py createsuperuser
```

