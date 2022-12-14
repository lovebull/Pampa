from flask_wtf import  FlaskForm
from wtforms import  StringField,RadioField,SelectField,TextAreaField,SelectMultipleField,PasswordField,BooleanField,URLField
from wtforms.validators import DataRequired,Length,URL
from app.blog.models import PostPublishType
from flask_wtf.file import FileField, FileSize, FileAllowed

class CategoryForm (FlaskForm):
    name = StringField('分类名称', validators=[
        DataRequired(message="不能为空"),
        Length(max=20,min=2, message="用户名必须在8到20位之间")
    ])
    icon = StringField('分类图标', validators=[
        Length(max=256, message="不符合字数要求！")
    ])


class PostForm(FlaskForm):
    title = StringField('标题', validators=[
        DataRequired(message="[标题]不能为空"),
        Length(max=128, message="不符合字数要求！")
    ])
    desc = TextAreaField('描述')
    has_type = RadioField('发布状态',
        choices=(PostPublishType.draft.name, PostPublishType.show.name),
        default=PostPublishType.show.name)

    category_id = SelectField(
        '分类',
        choices=None,
        coerce=int,
        validators=[
            DataRequired(message="[分类]不能为空"),
        ]
    )
    content = TextAreaField('文章内容',
        validators=[DataRequired(message="[文章内容]不能为空")]
    )
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)

class TagForm(FlaskForm):
    name=StringField('标签',validators=[
        DataRequired(message='Tag[标签]不能为空'),
        Length(min=2,max=128,message="标签数字在2到128")

         ])



class CreateUserForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
    ])
    password = PasswordField('password', validators=[
        Length(max=32, message="不符合字数要求！")
    ], description="修改用户信息时，留空则代表不修改！")

    avatar = FileField(u"avatar", validators=[
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=2048000, message="不能大于2M")],
                       description="大小不超过2M，仅支持jpg/png/gif格式，不选择则代表不修改")

    is_super_user = BooleanField("是否为管理员")
    is_active = BooleanField("是否活跃", default=True)
    is_staff = BooleanField("是否锁定")


class BannerForm(FlaskForm):
    img=FileField("Banner图",validators=[
        FileAllowed(['jpg','png','gif'],message="仅支持jpg/png/gif格式"),
        FileSize(max_size=3*1024*1000,message="不能大于3M")],
        description="大小不超过3M，仅支持jpg/png/gif格式，不选择则代表不修改")
    desc=StringField("描述",validators=[
        Length(max=20,message="不符合字数要求")
    ])

    url=URLField("URL",validators=[
        URL(require_tld=False,message="请输入正确URL"),
        Length(max=30,message="不符合字数要求")]
      )


class SettingForm(FlaskForm):

    pampa_domain = StringField('网站域名', default='www.h3blog.com', validators=[DataRequired()])
    pampa_title = StringField('网站名称', default='何三笔记', validators=[DataRequired()])
    pampa_keywords = StringField('关键字', default='python blog')
    pampa_description = TextAreaField('网站描述')
    pampa_tongji_script = TextAreaField('网站统计代码', default='')
    pampa_extend_meta = TextAreaField('网站META', default='')
    pampa_record_no = StringField('备案号', default='冀ICP备16000781号-3')
    pampa_start_time = StringField('网站开始时间', default='2020-02-20')
    pampa_comment = BooleanField(label='开启评论', default=False)
    pampa_register_invitecode = BooleanField(label='开启邀请注册', default=False)
    pampa_blog_copyright=TextAreaField('版权说明', default='Copyright Your WebSite.Some Rights Reserved.')

    def to_dict(self):
        '''转换成map'''
        ret = {}
        for name in self._fields:
            if name in ['csrf_token', 'submit']:
                continue
            ret[name] = self._fields[name].data
        return ret
