# 系统记录

## 数据库参数介绍
### account
**用户账户数据库，主要是用于快捷登陆查询**
```
account: 用户名，主Key，不允许有重复的用户名
id: 角色的ID，先通过role确定角色，再用ID对应到该用户个人
role: 系统角色，目前分为学生:0，老师:1，校长:2
password: 账户密码
联合主键role_id_key，避免角色相同ID插入失败，主要通过id和role来区分
```

### student
**学生信息表**

```
id: 主键，自增ID，方便程序内部查询
name: 姓名
tel: 可选，学生电话，不一定有
payment: 可选，付费情况
cid: 可选，字符串存储课程id，用","分隔，因为可能有多个课程
sex: 性别
age: 年龄
school: 学校
email: 邮箱
parent_name: 监护人名字
relation: 关系, 0:父亲，1:母亲，其他再定义
parent_tel: 监护人电话，必须要有，并通过这个获取验证码注册
联合主键identity，通过学生姓名，监护人姓名和电话确认唯一学生
```

### teacher
**老师信息表**
```
id: 主键，自增ID，方便程序内部查询
name: 姓名，
tel: 老师电话，
cid: 课程ID，字符串存储，用","分隔，因为可能有多个课程
```

### course
**课程信息表**
```
id: 主键，自增ID，方便程序内部查询
subject: 科目，目前没有定义对应关系，例子：“0:数学, 1:语文，2:英语”
fee: 课程费用
term: 学期
grade: 年级
time: 0:上午，1:下午，2:晚上
date: 字符串保存，每周几上课，可能多天，用","分隔，例子"1,2,3"表示每周1，2，3上课
class: 班次
classroom: 教室
tid: 老师ID，字符串存储，用","分隔，因为可能有多个老师
联合主键identity，通过课程科目，班次，学期和时间确定唯一课程
```

### problem
**题目信息表**
```
id: 主键，自增ID，方便程序内部查询
subject: 科目，目前没有定义对应关系，例子：“0:数学”
type: 题目类型
level: 题目难度
elapsed: 题目耗时
question: 题目问题，目前存的是文本
solution: 题目答案，目前存的是文本
focus: 题目考点
```