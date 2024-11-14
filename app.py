from flask import Flask,request,render_template
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


# 使用Flask类创建一个app对象
# __name__: 代表当前app.py 这个模块
#  作用：
# 1 以后出现bug可以帮我们快速定位
# 2 对于寻找模版文件，有一个相对路径
app = Flask(__name__)



# MySQL所在的主机名
HOSTNAME = "127.0.0.1"

# MySQL监听的端口号，默认3306
PORT = 3306

# 连接MySQL的用户名，读者用自己的设置的
USERNAME = "root"

# 连接MySQL的密码，读者用自己的
PASSWORD = "rootroot"

# MySQL上创建的数据库名称
DATABASE = "rest_reservation"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"



# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)中创建一个db对象
# 在SQLAlchemy 会自动读取app.config中连接数据库的信息
db = SQLAlchemy(app)

# 连接数据库
with app.app_context():
    with db.engine.connect() as conn:
        # 这个地方一直报错，改成stmt这样才可以，直接信
        #  使用 text 函数来创建可执行的 SQL 查询对象，以确保查询被正确执行
        stmt  = text("SELECT 1")
        rs = conn.execute(stmt)
        print(rs.fetchone())




# 定义一个函数 把这个函数定义为过滤器
def datetime_format(value, format="%Y年%m月%d日 %H:%M"):
    return value.strftime(format)

app.add_template_filter (datetime_format, 'dformat')


# 创建一个路由和视图函数的映射
# url与视图：path与视图
# /home/use

# 定义一个类
class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

@app.route('/')
def hello_world():  # put application's code here
    user = User(1, '张三名称', '<271717666@qkw.com>', '99password')
    person = {
        "username": "李四",
        "email": "lisi@qq.com",
    }
    return render_template('index.html', user=user,person=person)

@app.route('/profile')
def profile():  # put application's code here
    return '我是个人中心'

@app.route('/blog/list')
def blog_list():
    return "我是博客列表"

# @app.route('/blog/<int:blog_id>') #定义整型
# def blog_detail(blog_id):
#     return "您访问的博客是：%s" % blog_id


@app.route('/blog/<int:blog_id>') #定义整型
def blog_detail(blog_id):
    return render_template("blog_detail.html",
                           blog_id=blog_id,user_name="名称为当前用户")


# /book/list: 会给我返回第一页的数据
# /book/list?page=2
# http://localhost:8000/book/list?page=100
@app.route('/book/list')
def book_list():
    # arguments:参数
    # request.args:类字典类型
    page = request.args.get("page", default=1, type=int)
    return f"您获取的是第{page}页的图书列表数据"  # f字符串

# 过滤器 length：求长度，abs：求绝对值
@app.route('/filter')
def filter_demo():
    user = User(id=2,username="知了lll", email="<EMAIL>@qq.com", password="<mmPASSWORD>")

    mytime = datetime.now()
    return render_template("filter.html", user=user,mytime=mytime)

# 控制语句

@app.route('/control')
def control_statement():
    age = 17
    book = [{
        "name":"三国演义",
        "author":"罗贯中"
    }],[{
        "name":"西游记",
        "author":"吴承恩"
    }]
    # book = book 传入模版当中
    return render_template("control.html",age=age,book=book)

@app.route('/child1')
def child1():
    return render_template( "child1.html")

@app.route('/child2')
def child2():
    return render_template( "child2.html")

@app.route('/static')
def static_demo():
    return render_template( "static.html")
















if __name__ == '__main__':
    app.run()


# 1.debug模式：
# 1.1 改完代码 按 ctrl+s 就会刷新更新 看到最新的代码
# 1.2 如果开发的时候，出现bug 如果开启了debug模式，在浏览器就可以看到出错信息

# 2.修改host：
# 别的电脑访问我，别人就可以通过 修改为0.0.0.0别人就可以访问了

# 3.修改端口号 port
