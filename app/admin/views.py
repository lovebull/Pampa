from flask import  (
    Blueprint ,render_template,
    flash,redirect,url_for,request)
from werkzeug.security import generate_password_hash
from app.auth.views.auth import login_required
from app.blog.models import Category,Post,Tag
from .forms import CategoryForm ,PostForm,TagForm,CreateUserForm,SettingForm
from RealProject import db
from app.auth.models import User
from .models import Banner,Setting
from  flask_sqlalchemy import  Pagination
bp=Blueprint('admin',__name__,url_prefix='/admin',template_folder='templates',static_folder='static')
PER_PAGE=20

@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/category')
@login_required
def category():

    page=request.args.get('page',1,type=int)
    pagination=Category.query.order_by(-Category.add_date).paginate(page,per_page=PER_PAGE,error_out=False)
    category_list=pagination.items
    return  render_template(
        'admin/category.html',
        category_list=category_list,
        pagination=pagination
    )


@bp.route('/category/add',methods=['GET','POST'])
@login_required
def category_add():
    form=CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, icon=form.icon.data)
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}--分类添加成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)

@bp.route('/category/edit/<int:cate_id>',methods=['GET','POST'])
@login_required
def category_edit(cate_id):
    cate=Category.query.get(cate_id)
    form=CategoryForm(name=cate.name,icon=cate.icon)
    if form.validate_on_submit():
        cate.name=form.name.data
        cate.icon=form.icon.data
        db.session.add(cate)
        db.session.commit()
        flash(f'{form.name.data}--分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html',form=form)


@bp.route('/category/delete/<int:cate_id>',methods=['GET','POST'])
@login_required
def category_delete(cate_id):
    cate = Category.query.get(cate_id)
    if cate:
        Post.query.filter(Post.category_id==cate.id).delete()#2022.9.18 级联删除
        db.session.delete(cate)
        db.session.commit()
        flash(f'{cate.name}--分类删除成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category')


@bp.route('/article')
@login_required
def article():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page, per_page=PER_PAGE, error_out=False)
    post_list = pagination.items
    return render_template('admin/article.html', post_list=post_list, pagination=pagination)

@bp.route('/article/add',methods=['GET','POST'])
@login_required
def article_add():
    form=PostForm()
    form.category_id.choices=[(v.id ,v.name )for v in Category.query.all()]
    form.tags.choices=[(v.id,v.name) for v in Tag.query.all()]
    if form.validate_on_submit():
        post=Post(
            title=form.title.data,
            desc=form.desc.data,
            has_type=form.has_type.data,
            category_id=int(form.category_id.data),#一对多
            content=form.content.data
                  )
        post.tags=[Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}--文章保存成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html',form=form)


@bp.route('/article/edit/<int:post_id>',methods=['GET','POST'])
@login_required
def article_edit(post_id):
    post=Post.query.get(post_id)
    tags=[tag.id for tag in post.tags]
    form=PostForm(
        title=post.title,
        desc=post.desc,
        has_type=post.has_type.value,
        category_id=int(post.category.id),
        content=post.content,
        tags=tags,
        add_date=post.add_date,


    )
    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id = int(form.category_id.data) 
        post.content = form.content.data
        post.tags=[Tag.query.get(tag_id) for tag_id in form.tags.data]
        post.pub_date=request.form['pub_date']
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}--文章修改成功')
        return redirect(url_for('admin.article'))

    return render_template('admin/article_form.html',form=form,post=post)



@bp.route('/article/delete/<int:post_id>',methods=['GET','POST'])
@login_required
def article_delete(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}--文章删除成功')
        return redirect(url_for('admin.article'))


@bp.route('/tag')
@login_required
def tag():
    page=request.args.get('page',1,type=int)
    pagination = Tag.query.order_by(-Tag.add_date).paginate(page, per_page=PER_PAGE, error_out=False)
    tag_list = pagination.items
    return render_template('admin/tag.html', tag_list=tag_list, pagination=pagination)


@bp.route('/tag/add',methods=['GET','POST'])
@login_required
def tag_add():
    form=TagForm()
    if form.validate_on_submit():
        tag=Tag(
            name=form.name.data
        )
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}--Tag[标签]保存成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html',form=form)

@bp.route('/tag/edit/<int:tag_id>',methods=['GET','POST'])
@login_required
def tag_edit(tag_id):
    tag=Tag.query.get(tag_id)
    form=TagForm(name=tag.name)
    if form.validate_on_submit():
        tag.name=form.name.data
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}--Tag[标签]修改成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html',form=form)


@bp.route('/tag/delete/<int:tag_id>',methods=['GET','POST'])
@login_required
def tag_delete(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash(f'{tag.name}--Tag[标签]删除成功')
        return redirect(url_for('admin.tag'))


@bp.route('/user')
@login_required
def user():
    page=request.args.get('page',1,type=int)
    pagination = User.query.order_by(-User.add_date).paginate(page, per_page=PER_PAGE, error_out=False)
    user_list = pagination.items
    return render_template('admin/user.html', user_list=user_list, pagination=pagination)


@bp.route('/user/add', methods=['GET','POST'])
@login_required
def user_add():
    form=CreateUserForm()
    if form.validate_on_submit():
        from app.util import upload_file_path
        f=form.avatar.data
        avatar_path ,filename= upload_file_path('avatar', f)
        print('avatar_path===',avatar_path)
        print(filename)
        f.save(avatar_path)
        user=User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            avatar=f'avatar/{filename}',
            is_super_user=form.is_super_user.data,
            is_active=form.is_active.data,
            is_staff=form.is_staff.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}--用户信息【添加成功】')
        return redirect(url_for('admin.user'))
    return  render_template('admin/user_form.html',form=form)


@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    user=User.query.get(user_id)
    form=CreateUserForm(
        username=user.username,
        password=user.password,
        avatar=user.avatar,
        is_super_user=user.is_super_user,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
   
    if form.validate_on_submit():
        user.username = form.username.data
        if not form.password.data:
            user.password = user.password
        else:
            user.password = generate_password_hash(form.password.data)
        f = form.avatar.data
        if user.avatar == f:
            user.avatar = user.avatar
        else:
            from app.util import upload_file_path
            avatar_path, filename = upload_file_path('avatar', f)
            f.save(avatar_path)
            user.avatar = f'avatar/{filename}'
        user.is_super_user = form.is_super_user.data
        user.is_active = form.is_active.data
        user.is_staff = form.is_staff.data
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}--用户信息【修改成功】')
        return redirect(url_for('admin.user'))

    return  render_template('admin/user_form.html',form=form,user=user)

@bp.route('/user/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_delete(user_id):
    user = User.query.get(user_id)
    if tag:
        db.session.delete(user)
        db.session.commit()
        flash(f'{user.username}--删除成功')
        return redirect(url_for('admin.user'))
@bp.route('/upload',methods=["GET","POST"])
@login_required
def upload():
    if request.method=='POST':
        f=request.files["avatar"]
        print('dddddddd=',f)
    return render_template('admin/upload.html')
@bp.route('/tinymceupload',methods=["GET","POST"])
@login_required
def tinymce_upload():
    from app.util import upload_file_path
    if request.method == 'POST':
        f = request.files.get('file')
        file_size = len(f.read())
        f.seek(0)  
        if file_size > 2048000:  
            return {
                'code': 'err',
                'message': '文件超过限制2048000字节',
            }
        upload_path, filename = upload_file_path('article', f)
        f.save(upload_path)
        return {
            'code': '200',
            'location': f'/uploads/article/{filename}'
        }



@bp.route('/banner')
@login_required
def banner():
    banners=Banner.query.all()
    return render_template('admin/banner.html',banners=banners)

@bp.route('/banner/add',methods=["GET","POST"])
@login_required
def banner_add():
    from .forms import BannerForm
    from app.util import upload_file_path
    form=BannerForm()
    if form.validate_on_submit():
        f=form.img.data
        print(f)
        img_path,filename=upload_file_path('banner',f)
        f.save(img_path)
        banner=Banner(
            img=f'banner/{filename}',
            desc=form.desc.data,
            url=form.url.data
        )
        db.session.add(banner)
        db.session.commit()
        return  redirect(url_for('admin.banner'))
        flash(f'Banner数据新增成功')
    return render_template('admin/banner_form.html',form=form)
@bp.route('/banner/edit/<int:banner_id>',methods=["GET","POST"])
@login_required
def banner_edit(banner_id):
    from .forms import BannerForm
    banner=Banner.query.get(banner_id)
    form=BannerForm(img=banner.img,desc=banner.desc,url=banner.url)
    if form.validate_on_submit():
        f=form.img.data
        if banner.img==f:
            banner.img=banner.img
        else:
            from app.util import upload_file_path
            img_path,filename=upload_file_path('banner',f)
            f.save(img_path)
            banner.img=f'banner/{filename}'
        banner.desc=form.desc.data
        banner.url=form.url.data
        return redirect(url_for('admin.banner'))
    return render_template('admin/banner_form.html',form=form,banner=banner)

@bp.route('/banner/del/<int:banner_id>',methods=["GET","POST"])
@login_required
def banner_del(banner_id):
    import os
    from flask import  current_app
    banner=Banner.query.get(banner_id)
    if banner:
        file_path = current_app.config['PAMPA_UPLOAD_PATH'] + '/' + banner.img
        os.remove(file_path)
        db.session.delete(banner)
        db.session.commit()
        flash(f'{banner.img}--删除成功')
        return redirect(url_for('admin.banner'))

@bp.route('/comment')
def comment():
    return render_template('admin/comment.html')
@bp.route('/setting',methods=["GET","POST"])
@login_required
def setting():
    form = SettingForm()
    settings = Setting.query.all()
    setting_dict = {}
    for s in settings:
        setting_dict[s.skey] = s
    if request.method == 'POST' and form.validate_on_submit:
        form_dict = form.to_dict()
        print('form_dict---',form_dict)
        for name in form_dict:
            print('name--',name)
            s = setting_dict.get(name, None)
            print('s===',s)
            if s:
                s.svalue = form_dict.get(name)
                print(s.svalue)
            else:
                s = Setting(
                    skey=name,
                    svalue=form_dict.get(name)
                )
                print("添加--",s)
                db.session.add(s)

            db.session.commit()
        flash('【网站配置信息修改成功】')
    for name in form._fields:
        s = setting_dict.get(name, None)
        if s :
            if name in ['pampa_comment','pampa_register_invitecode']:
                form._fields[name].data = True if s.svalue == '1' else False
            else:
                form._fields[name].data = s.svalue

    return render_template('admin/setting.html',form = form)
@bp.route('/setting/preferences',methods=["GET"])
@login_required
def settingpreferences():
    form = SettingForm()
    settings = Setting.query.all()
    setting_dict = {}
    for s in settings:
        setting_dict[s.skey] = s
    for name in form._fields:
        s = setting_dict.get(name, None)
        if s :
            if name in ['pampa_comment','pampa_register_invitecode']:
                form._fields[name].data = True if s.svalue == '1' else False
            else:
                form._fields[name].data = s.svalue
    return render_template('admin/setting/preferences.html',form = form)
@bp.route('/setting/tab1',methods=["GET","POST"])
@login_required
def setting_tab1():
    return render_template('admin/setting/quansetting.html')
@bp.route('/setting/tab2',methods=["GET","POST"])
@login_required
def setting_tab2():
    return render_template('admin/setting/pagesetting.html')
