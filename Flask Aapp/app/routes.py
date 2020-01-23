from app import app, images
from flask import render_template
from app.forms import LoginForm
from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, PartsSelectForm
from datetime import datetime
from app.forms import EditProfileForm, PostForm
from app.models import Post, Cart, subs
import sqlite3
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os


@app.route('/')
@app.route('/index')
@login_required
def index():
    users = User.query.all()
    for i in users:
        if i.username == current_user.username:
            print('ID of logged in user is {}'.format(i.id))
            # get_user_logged_in_uid = i.id
            u = User.query.get(i.id)
            # print(u)
            posts = u.posts.all()
            # print(type(posts))
            # global body
            # for p in posts:
            #     body = p.body
            # mypost = {'user_post': posts}
    # get_user_logged_in_uid = User.query.filter_by(username=form.username.data).first()
    # post = form.username.data.posts.all()
    # print(current_user.username)
    # print(dir(current_user.username))
    # posts = Post.query.all()
    # return render_template("index.html", title='Home Page', mypost=mypost)
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # print(next_page)
        # print(request.args.get('next'))
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        u = User.query.get(current_user.id)
        print('Logged in as user {}'.format(u))
        post_user = Post(body=post_form.post_detail.data, author=current_user)
        db.session.add(post_user)
        db.session.commit()
        flash('Congratulations, you are have added post!')
        return redirect(url_for('login'))
    return render_template('add_post.html', title='POST', post_form=post_form)


@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    # qry = Post.query(Album).filter(Album.id==id)
    # qry = db.session.query(Post).get(id)
    post = Post.query.filter_by(id=id).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.post_detail.data
        db.session.add(post)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index', id=post.id))
    form.post_detail.data = post.body
    return render_template('edit_post.html', title='Edit POSt', form=form)


@app.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    print(post.id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Delete ')
    return redirect(url_for('index'))
    return render_template("index.html", title='Home Page')


@app.route('/delete_item/<int:id>', methods=['POST'])
@login_required
def delete_item(id):
    cart_del = Cart.query.filter_by(prod_id=id).first_or_404()
    print(cart_del)
    db.session.delete(cart_del)
    db.session.commit()
    flash('Post Delete ')
    return redirect(url_for('total_item'))
#    return render_template("index.html", title='Home Page')



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    form = PartsSelectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            my_cart_prod = Cart.query.filter_by(part_name=form.part_name.data).first()
            if my_cart_prod is None:
                filename = images.save(request.files['part_image'])
                url = images.url(filename)
                print('URL of new item is {}'.format(url))
                new_item = Cart(part_name=form.part_name.data, part_cost=form.part_cost.data, part_desc=form.part_desc.data, u_cart_id=current_user.id, image_filename=filename, image_url=url)
                print(my_cart_prod)
                db.session.add(new_item)
                db.session.commit()
                flash('New recipe, {}, added!'.format(new_item.part_name), 'success')
                #   return render_template('cart.html', new_item=new_item)
            else:
                flash('ERROR! PRODUCT {} ALREADY EXIST So Updating'.format(form.part_name.data))
                filename = images.save(request.files['part_image'])
                my_cart_prod.image_filename = filename
                my_cart_prod.part_cost = form.part_cost.data
                my_cart_prod.part_desc = form.part_desc.data
                url = images.url(filename)
                my_cart_prod.image_url = url
                db.session.commit()
        else:
            flash('ERROR! PRODUCT not added.', 'error')

    return render_template('cart.html', title='PRODUCTS ITEMS', form=form)


@app.route('/total_item', methods=['GET'])
@login_required
def total_item():
    u = User.query.get(current_user.id)
    all_items = u.cart_item.all()
    print(u)
    return render_template('total_item.html', title='Total Items', all_items=all_items)


@app.route('/about_item/<int:id>', methods=['GET'])
@login_required
def about_item(id):
    carts = Cart.query.filter_by(prod_id=id).first_or_404()
    return render_template('about_item.html', title='Total Items', all_items=carts)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    # print(dir(user))
    return render_template('user.html', user=user, posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/brands', methods=['GET'])
@login_required
def brands():
    u = User.query.get(current_user.id)
    all_brand_item = u.brand_item.all()
    return render_template('brand.html', title='All Brands', all_brand_item=all_brand_item)

##################
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html")


@app.route('/add_to_cart/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    if request.method == 'POST':
        u = User.query.filter_by(id=current_user.id).first_or_404()
        user_iid = current_user.id
        carts = Cart.query.filter_by(prod_id=id).first_or_404()
        cartt_id = carts.prod_id
        if db.session.query(subs).filter_by(prod_id=cartt_id).first() is None:
            carts.cart_items.append(u)
            db.session.commit()
        else:
            conn = sqlite3.connect('app.db')
            table_tuple = (user_iid, cartt_id)
            sqlite_insert_with_param = """UPDATE subs SET cart_count=cart_count+1 WHERE id=? and prod_id=?;"""
            conn.execute(sqlite_insert_with_param, table_tuple)
            conn.commit()

        flash('Add Item to cart, Now Count is {}, !'.format(carts.part_name))
    return render_template('about_item.html', title='Total Items', all_items=carts)


@app.route('/remove_from_cart/<int:id>', methods=['POST'])
@login_required
def remove_from_cart(id):
    if request.method == 'POST':
        u = User.query.filter_by(id=current_user.id).first_or_404()
        user_iid = current_user.id
        carts = Cart.query.filter_by(prod_id=id).first_or_404()
        cartt_id = carts.prod_id
        if db.session.query(subs).filter_by(prod_id=cartt_id).first() is None:
            carts.cart_items.append(u)
            db.session.commit()
        else:
            conn = sqlite3.connect('app.db')
            table_tuple = (user_iid, cartt_id)
            sqlite_insert_with_param = """UPDATE subs SET cart_count=cart_count-1 WHERE id=? and prod_id=? and cart_count >0;"""
            conn.execute(sqlite_insert_with_param, table_tuple)
            conn.commit()

        flash('Add Item to cart, Now Count is {}, !'.format(carts.part_name))
    return render_template('about_item.html', title='Total Items', all_items=carts)