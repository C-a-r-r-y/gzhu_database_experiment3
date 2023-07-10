# 广州大学数据库原理课实验3
## 简介
广州大学数据库原理课实验3的内容，使用模板引擎,flask框架和SQLAlchemy实现，可以拿来应付老师，网上有用C#实现的，mfc实现的，但我没有看到用python web实现的，我要添砖加瓦
## 实验要求（word文档复制）
假设有“教师”、“学生”、“课程”三个实体，教师的基本信息包括：工号、姓名、职称、工资，课程的基本信息包括：课程号、课程名、学分数，学生的基本信息包括：学号、姓名、性别、年龄。系统必须满足以下要求：

(1) 一门课程只能有一个教师任课，一个教师可以上多门课程；

(2) 一个学生可以选修多门课程，一门课程可以由多个学生来选修，记录不同学生选
修不同课程的成绩；

(3) 设置一个管理员，用于维护（添加、删除和修改等基本任务）学生基本信息、教师基本信息和教师所授课程等工作，此外，管理员添加学生时，为其设置初始密码；当学生选修了某门课程，课程成绩由管理员录入；

(4) 学生可以利用学号和密码登录系统，登陆系统后，可以进行选课、修改密码和个人基本信息、查询自己的选课及总学分等操作；

(5) 能够统计不同职称的教师的数量、不同职称的教师的平均工资，可以统计每门课程的平均成绩、最高分、最低分，统计每个学生选修课程的总学分；
## 使用方法
### 建表（mysql为例）
在你的数据库上建表
```sql
CREATE TABLE `student` (
  `pwd` varchar(20) NOT NULL,
  `sno` varchar(10) NOT NULL,
  `sname` varchar(20) NOT NULL,
  `ssex` char(3) DEFAULT NULL,
  `sage` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `course` (
  `cno` varchar(4) NOT NULL,
  `cname` varchar(40) NOT NULL,
  `ccredit` smallint(6) NOT NULL,
  `tno` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sc` (
  `sno` varchar(10) NOT NULL,
  `cno` varchar(4) NOT NULL,
  `grade` smallint(6) NOT NULL,
  `tno` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `teacher` (
  `tno` varchar(7) NOT NULL,
  `tname` varchar(20) NOT NULL,
  `tposition` varchar(20) NOT NULL,
  `tsalary` smallint(6) NOT NULL,
  `pwd` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `admin` (
  `ano` varchar(10) NOT NULL,
  `pwd` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
### 安装依赖
```shell
pip install flask
pip install flask_SQLAlchemy
```
**可能有遗漏，可以根据报错进行pip安装**
### 修改连接地址
```python
app.config['SQLALCHEMY_DATABASE_URI'] = "你的数据库url"
```
### 运行
```shell
flask run
```
## 作者想说
这玩意是我一天半写出来的，大二下学期太累了，赶完好几个ddl才轮到数据库的ddl，这个程序做得非常草率，甚至没有登录鉴权机制，纯靠跳转实现，拿来交作业可以，别深究
