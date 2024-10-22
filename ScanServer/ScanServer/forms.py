from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Required, Email, Optional, URL, InputRequired

class NameForm(FlaskForm):
    # text = StringField( "网卡名",validators= [DataRequired()])
    netname = StringField('网卡名', validators=[DataRequired()])
    needpcap = StringField('抓包个数', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField( "提交")

class ScipyForm(FlaskForm):
    scipy = SubmitField("开启抓包")
    spider = SubmitField("开启扫描")
    repeter = SubmitField("重发数据包")

class PrintLogForm(FlaskForm):
    scipylog = TextAreaField("数据包抓取记录",validators=[Required()])
    spiderlog = TextAreaField("爬虫记录",validators=[Required()])
    repeterlog = TextAreaField("重发器记录",validators=[Required()])

class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired('请输入用户名'), Length(1, 20)])
    # email = StringField('Email', validators=[DataRequired('请输入邮箱'), Email('邮箱格式不正确')])
    username_or_email = StringField('Username / Email', validators=[DataRequired('请输入用户名/邮箱')])
    password = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired('请输入邮箱'), Email('邮箱格式不正确')])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    password1 = PasswordField('Re Password', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Register')


class InitForm(FlaskForm):
    website = StringField('网页', validators=[DataRequired('请输入网址'), Optional(), URL(), Length(0, 255)])
    runway = SelectField('身份验证方式', coerce=str)
    submit = SubmitField( "提交")

class CookieForm(FlaskForm):
    usercookie1 = StringField('TestCookie1', validators=[DataRequired('请输入有效Cookie')])
    usercookie2 = StringField('TestCookie2', validators=[DataRequired('请输入有效Cookie')])
    spider = SubmitField("开启扫描网页敏感数据")
    repeter = SubmitField("重发数据包")



class AimUserForm(FlaskForm):
    username_or_email1 = StringField('Username / Email / Phone', validators=[DataRequired('请输入账号')])
    password1 = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(1, 128)])
    username_or_email2 = StringField('Username / Email / Phone', validators=[DataRequired('请输入账号')])
    password2 = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(1, 128)])
    submit = SubmitField('开始用户登入')
