from flask import Flask,request

# 使用Flask类创建一个app对象
# __name__: 代表当前app.py 这个模块
#  作用：
# 1 以后出现bug可以帮我们快速定位
# 2 对于寻找模版文件，有一个相对路径
app = Flask(__name__)

# 创建一个路由和视图函数的映射
# url与视图：path与视图
# /home/use
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World1!'

@app.route('/profile')
def profile():  # put application's code here
    return '我是个人中心'

@app.route('/blog/list')
def blog_list():
    return "我是博客列表"

@app.route('/blog/<int:blog_id>') #定义整型
def blog_detail(blog_id):
    return "您访问的博客是：%s" % blog_id


# /book/list: 会给我返回第一页的数据
# /book/list?page=2
# http://localhost:8000/book/list?page=100
@app.route('/book/list')
def book_list():
    # arguments:参数
    # request.args:类字典类型
    page = request.args.get("page", default=1, type=int)
    return f"您获取的是第{page}页的图书列表数据"  # f字符串



if __name__ == '__main__':
    app.run()


# 1.debug模式：
# 1.1 改完代码 按 ctrl+s 就会刷新更新 看到最新的代码
# 1.2 如果开发的时候，出现bug 如果开启了debug模式，在浏览器就可以看到出错信息

# 2.修改host：
# 别的电脑访问我，别人就可以通过 修改为0.0.0.0别人就可以访问了

# 3.修改端口号 port
