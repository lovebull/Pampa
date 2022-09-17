import json
from  flask import  Blueprint ,render_template,send_from_directory,current_app,request
import os
from app.blog.models import Post,Category,Tag
bp=Blueprint('blog',__name__,url_prefix='/',template_folder='templates',static_url_path='/statics',static_folder='static')
PER_PAGE=10
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page, per_page=PER_PAGE, error_out=False)
    post_list = pagination.items
    import random
    imgs = ['图一url', '图二url', '图三url']
    for post in post_list:
        post.img = random.sample(imgs, 1)[0]
    return render_template('index.html', post_list=post_list, pagination=pagination)

@bp.route('/category/<int:cate_id>')
def cate(cate_id):
    cate=Category.query.get(cate_id)
    page=request.args.get('page',default=1,type=int)
    pagination=Post.query.filter(Post.category_id==cate_id).paginate(page,per_page=PER_PAGE,error_out=False)
    post_list=pagination.items
    return render_template('category.html',post_list=post_list,cate=cate,cate_id=cate_id,pagination=pagination)

@bp.route('/category/<int:cate_id>/<int:post_id>')
def detail(cate_id,post_id):
    cate=Category.query.get(cate_id)
    post=Post.query.get_or_404(post_id)
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()
    return render_template('detail.html',cate=cate,post=post, prev_post=prev_post, next_post=next_post)
@bp.context_processor
def inject_archive():
    posts = Post.query.order_by(-Post.pub_date)
    dates = set([post.pub_date.strftime("%Y年%m月") for post in posts])
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['bg-primary', 'bg-secondary', 'bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'bg-light', 'bg-dark']
    new_posts = posts.limit(6)
    cates=Category.query.all()
    for ca in cates:
        ca.num = Post.query.filter(Post.category_id ==ca.id).count()
    return dict(dates=dates, tags=tags, new_posts=new_posts,cates=cates)

@bp.route('/category/<string:date>')
def archive(date):
    import re
    regex = re.compile(r'\d{4}|\d{2}')
    dates = regex.findall(date)
    from sqlalchemy import extract, and_, or_
    page = request.args.get('page', 1, type=int)
    archive_posts = Post.query.filter(and_(extract('year', Post.pub_date) == int(dates[0]), extract('month', Post.pub_date) == int(dates[1])))
    pagination = archive_posts.paginate(page, per_page=PER_PAGE, error_out=False)
    return render_template('archive.html', post_list=pagination.items,  pagination=pagination, date=date)

@bp.route('/tags/<int:tag_id>')
def tags(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)


@bp.route('/search')
def search():
    words = request.args.get('words', '', type=str)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.title.like("%"+words+"%")).paginate(page, per_page=PER_PAGE, error_out=False)
    post_list = pagination.items
    return render_template('search.html', post_list=post_list, words=words, pagination=pagination)
@bp.route('/uploads/<path:filename>')
def uploads(filename):
    return  send_from_directory(current_app.config['PAMPA_UPLOAD_PATH'],filename)