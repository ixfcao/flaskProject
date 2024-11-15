from flask import Flask,request,render_template
from datetime import datetime

from flask_migrate import migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.testing.suite.test_reflection import users


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
DATABASE = "flask_project"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)中创建一个db对象
# 在SQLAlchemy 会自动读取app.config中连接数据库的信息
db = SQLAlchemy(app)


# 连接数据库 测试
# with app.app_context():
#     with db.engine.connect() as conn:
#         # 这个地方一直报错，改成stmt这样才可以，直接信
#         #  使用 text 函数来创建可执行的 SQL 查询对象，以确保查询被正确执行
#         stmt  = text("SELECT 1")
#         rs = conn.execute(stmt)
#         print(rs.fetchone())




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

# orm模型
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #自增
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # articles = db.relationship('Article', back_populates='author') #和下面的一一对应

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者外键
    author_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    # author = db.relationship("Student",back_populates="articles") # back_populates

    # 使用这个backref 会自动给模型User添加一个articles的属性用来获取文章列表
    author = db.relationship("Student", backref="articles")

# article = Article("title",content="FalseXXXXXX")

# article.author = Student.query.get(article.author_id)
# print(article.author)
# 拿到所有文章




# student = Student(username="小吴",password="<67678>")
# sql: insert student (username,password) values ('小吴','<67678>')
# 把所有的表映射进数据库 需要手动推一个应用上下文
with app.app_context(): #这行代码创建了一个 Flask 应用上下文。在 Flask 中，某些操作（如数据库操作）需要在一个活动的应用上下文中进行。app.app_context() 提供了这样一个上下文。
                        #with 语句确保在块结束时自动清理上下文。
    db.create_all()

# 添加
@app.route("/student/add")
def add_student():
    # 1.创建学生对象
    student = Student(username="学生张珊11",password="11111")
    # 2.将ORM对象添加到db.session中
    db.session.add(student)
    # 3.将db。session中的改变同步到数据库中
    db.session.commit()
    return "学生创建成功"
# 查找
@app.route("/student/query")
def query_student():
    # 1.get查找：根据主键查找
    # student = Student.query.get(1)
    # print(f"{student.id}:{student.username}:{student.password}")

    # 2.filter_by查找
    # QuerySet
    students = Student.query.filter_by(username="学生张珊")
    for student in students:
        print(student.username)
    return "数据查找成功"
# 修改
@app.route("/student/update")
def update_student():
    # 1.get查找：根据主键查找
    student = Student.query.filter_by(username="学生张珊").first()
    student.password = "222222"
    db.session.commit()
    return "数据修改成功"

@app.route("/student/delete")
def delete_student():
    student = Student.query.get(1)
    db.session.delete(student)
    db.session.commit()
    return "数据删除成功"


@app.route("/article/add")
def add_article():
    article1 = Article(title="Flask学习教程",content="flask-xxx")
    article1.author = Student.query.get(2)

    article2 = Article(title="Java学习教程",content="java好难学")
    article2.author = Student.query.get(2)

    # 添加到session
    db.session.add_all([article1, article2])
    # 同步session中的数据到数据库中
    db.session.commit()
    return "文章添加成功！"

# 根据作者查询文章
@app.route("/article/query")
def query_article():
    student = Student.query.get(2)
    for article in student.articles:
        print(article.title)
    return "文章查找成功"




















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
