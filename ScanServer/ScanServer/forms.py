from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Required

class NameForm(FlaskForm):
    # text = StringField( "网卡名",validators= [DataRequired()])
    netname = SelectField('网卡名', coerce=str)
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

