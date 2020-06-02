"""
模拟登录注册
1. 在stu库创建一个user表
    CREATE TABLE user (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(32) NOT NULL,
        password VARCHAR(32) NOT NULL
    );
2. 编写程序模拟登录和注册的功能
    注册：向数据库中插入一条用户记录
    登录：查询用户信息，如果有结果则打印登陆成功，否则重新登录
"""
import pymysql

# 连接数据库
db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    database="stu",
    charset="utf8"
)

# 获取游标(操作数据库，执行sql语句)
cur = db.cursor()


def register():
    """
    不能有重复的用户名
    如果注册成功 return True，如果失败return False
    :return:
    """
    username = input("用户名：")
    password = input("密码：")
    tup = (username, password)
    # 判断是否有重复的用户名
    sql = "SELECT * FROM user WHERE name='%s'" % username
    cur.execute(sql)
    result = cur.fetchone()
    if result:
        return False
    # 向数据库中插入数据
    try:
        sql = "INSERT INTO user (name, password) VALUES (%s, %s);"
        cur.execute(sql, tup)
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()


def login():
    """
    如果登录成功 return True，如果失败return False
    :return:
    """
    username = input("用户名：")
    password = input("密码：")
    tup = (username, password)
    sql = "SELECT * FROM user WHERE name=%s and password=%s;"
    cur.execute(sql, tup)
    result = cur.fetchone()
    if result:
        return True

while True:
    print("1 注册   2 登录")
    cmd = input("请输入指令：")
    if cmd == "1":
        # 注册请求   封装成函数：register()
        if register():
            print("注册成功～")
        else:
            print("注册失败！")
    elif cmd == "2":
        # 登录请求  封装成login()
        if login():
            print("登录成功～")
        else:
            print("登录失败！")
    else:
        print("请重新选择功能～")



# 关闭数据库以及游标
cur.close()
db.close()


