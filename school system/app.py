from flask import Flask, request, redirect,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://db_experiment3:12345@192.168.15.179/db_experiment3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    sname = db.Column(db.String(20))
    ssex = db.Column(db.String(4))
    sage = db.Column(db.Integer)
    pwd = db.Column(db.String(20))

class Teacher(db.Model):
    tno = db.Column(db.String(7), primary_key=True)
    tname = db.Column(db.String(20))
    tposition = db.Column(db.String(3))
    tsalary = db.Column(db.Integer)
    pwd = db.Column(db.String(20))

class Course(db.Model):
    cno = db.Column(db.String(4), primary_key=True)
    cname = db.Column(db.String(40))
    tno = db.Column(db.String(7))
    ccredit = db.Column(db.Integer)

class SC(db.Model):
    cno = db.Column(db.String(4),db.ForeignKey('course.cno'), primary_key=True)
    sno = db.Column(db.String(10),db.ForeignKey('student.sno'), primary_key=True)
    grade = db.Column(db.Integer)
    tno = db.Column(db.String(7))

class Admin(db.Model):
    ano = db.Column(db.String(10), primary_key=True)
    pwd = db.Column(db.String(20))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        if request.form['login-method'] == 'student':
            to_login = db.session.query(Student).get(request.form['account'])
            if to_login is None:
                return "没有此用户"
            if to_login.pwd == request.form['password']:
                print(to_login.sno + "登录成功")
                return redirect('/'+request.form['login-method']+'/'+request.form['account'])
            else:
                print(to_login.sno + "密码错误")
                return "密码错误"

        elif request.form['login-method'] == 'teacher':
            to_login = db.session.query(Teacher).get(request.form['account'])
            if to_login is None:
                return "没有此用户"
            if to_login.pwd == request.form['password']:
                print(to_login.tno + "登录成功")
                return redirect('/'+request.form['login-method']+'/'+request.form['account'])
            else:
                print(to_login.tno + "密码错误")
                return "密码错误"

        elif request.form['login-method'] == 'admin':
            to_login = db.session.query(Admin).get(request.form['account'])
            if to_login is None:
                return "没有此用户"
            if to_login.pwd == request.form['password']:
                print(to_login.ano + "登录成功")
                return redirect('/'+request.form['login-method']+'/'+request.form['account'])
            else:
                print(to_login.ano + "密码错误")
                return "密码错误"

@app.route('/student/<sno>', methods=['GET', 'POST'])
def student(sno):
    user_info = db.session.query(Student).get(sno)
    user_course = db.session.query(SC,Course).join(SC,SC.cno == Course.cno).filter(SC.sno == sno).all()
    course_list = db.session.query(Course).all()
    credit_sum = sum([x[1].ccredit for x in user_course])
    temp = [user_course[x][1] for x in range(len(user_course))]
    selectable_course = [x for x in course_list if x not in [user_course[x][1] for x in range(len(user_course))]]

    if request.method == 'GET':
        return render_template('student.html',
                               username = user_info.sname,usergender = user_info.ssex,userage = user_info.sage,
                               usercourse = user_course,totalcredit = credit_sum,
                               selectablecourse = selectable_course)
    if request.method == 'POST':
        if request.form['type'] == 'changeinfo':
            if user_info:
                user_info.sname = request.form['name']
                user_info.ssex = request.form['gender']
                user_info.sage = request.form['age']
                if request.form['password'] != "":
                    user_info.pwd = request.form['password']
                db.session.commit()
            return "个人信息修改完毕"
        elif request.form['type'] == 'courseselection':
            to_select = next(filter(lambda x: x.cno == request.form['course'],selectable_course))
            to_submit = SC(cno = request.form['course'],sno = sno,tno = to_select.tno,grade = 0)
            db.session.add(to_submit)
            db.session.commit()
            return "选课成功"

@app.route('/admin/<ano>', methods=['GET', 'POST'])
def admin(ano):
    student_list = db.session.query(Student,db.func.coalesce(db.func.sum(Course.ccredit),0)).\
        join(SC,Student.sno == SC.sno, isouter=True).join(Course,SC.cno == Course.cno, isouter=True).group_by(Student.sno).all()

    teacher_list = db.session.query(Teacher).all()
    teacher_position_list = db.session.query(Teacher.tposition,db.func.avg(Teacher.tsalary),db.func.count(Teacher.tno)).\
        group_by(Teacher.tposition).all()

    course_list = db.session.query(Course,db.func.max(SC.grade),db.func.min(SC.grade),db.func.avg(SC.grade)).\
        join(SC,Course.cno == SC.cno).group_by(Course.cno).all()

    sc_list = db.session.query(SC).group_by(SC.cno).all()

    if request.method == 'GET':
        return render_template("admin.html",studentlist=student_list,
                               teacherlist=teacher_list,
                               salary=teacher_position_list,
                               courselist=course_list,
                               sclist=sc_list)

    if request.method == 'POST':
        if request.form['type'] == 'changestudent':
            student = db.session.query(Student).get(request.form['sno'])
            student.sname = request.form['sname']
            student.sage = request.form['sage']
            student.pwd = request.form['pwd']
            student.ssex = request.form['ssex']
            db.session.commit()
            return "修改学生信息成功"
        elif request.form['type'] == 'addstudent':
            db.session.add(Student(sno = request.form['sno'],
                           sname=request.form['sname'],
                           sage = request.form['sage'],
                           pwd = request.form['pwd'],
                           ssex=request.form['ssex']
            ))
            db.session.commit()
            return "添加学生成功"
        elif request.form['type'] == 'deletestudent':
            db.session.delete(Student.query.get(request.form['sno']))
            db.session.commit()
            return "学生已删除"

        elif request.form['type'] == 'changeteacher':
            teacher = db.session.query(Teacher).get(request.form['tno'])
            teacher.tname = request.form['tname']
            teacher.tposition = request.form['tposition']
            teacher.pwd = request.form['pwd']
            teacher.tsalary = request.form['tsalary']
            db.session.commit()
            return "修改教师信息成功"
        elif request.form['type'] == 'addteacher':
            db.session.add(Teacher(tno = request.form['tno'],
                           tname=request.form['tname'],
                           tposition = request.form['tposition'],
                           pwd = request.form['pwd'],
                           tsalary=request.form['tsalary']
            ))
            db.session.commit()
            return "添加教师成功"
        elif request.form['type'] == 'deleteteacher':
            db.session.delete(Teacher.query.get(request.form['tno']))
            db.session.commit()
            return "教师已删除"

        elif request.form['type'] == 'changesc':
            sc = db.session.query(SC).filter_by(sno=request.form['sno'],cno=request.form['cno']).first()
            sc.grade = request.form['grade']
            db.session.commit()
            return "成绩修改成功"
        elif request.form['type'] == 'addsc':
            db.session.add(SC(cno = request.form['cno'],
                           sno=request.form['sno'],
                           grade = request.form['grade']
            ))
            db.session.commit()
            return "选课信息添加成功"
        elif request.form['type'] == 'deletesc':
            db.session.delete(Teacher.query().filter_by(sno=request.form['sno'],cno=request.form['cno']).first())
            db.session.commit()
            return "选课信息已删除"




@app.errorhandler(404)
def page_not_found(e):
    return redirect('/login')


with app.app_context():
    db.engine.connect()


if __name__ == '__main__':
    app.run()
