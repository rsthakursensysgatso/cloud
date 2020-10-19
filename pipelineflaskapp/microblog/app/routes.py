from app import app, images, mail
from flask import render_template, make_response
from app.forms import LoginForm
from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, PartsSelectForm, HomeAddressForm, ChangePass, ForgetPass, NewPassord, SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.forms import EditProfileForm, PostForm
from app.models import Post, Cart, subs, Order, User
import sqlite3
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os
import random, string
from itsdangerous import URLSafeSerializer
from flask import Flask
from flask_mail import Mail, Message
import urllib.parse
from functools import wraps
from flask import g

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

# https://navaspot.wordpress.com/2014/06/25/how-to-implement-forgot-password-feature-in-flask/
@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPass()
    if form.validate_on_submit():
        auth_s = URLSafeSerializer("secret key", "auth")
        token = auth_s.dumps({"email": form.email_addr.data, "auth_token": randomString(100)})
        email = form.email_addr.data
        user_tuple = (token, email)
        conntdb = sqlite3.connect('app.db')
        cur = conntdb.cursor()
        sqlite_insert_with_param = """UPDATE user  set  token = ?  where email = ?;"""
        cur.execute(sqlite_insert_with_param, user_tuple)
        cur.close()
        conntdb.commit()
        conntdb.close()
        msg = Message('Hello', sender='rsthakur83@gmail.com', recipients=['rsthakur83@yahoo.com'])
        #msg.body = "Hello Shalllu Ravinder App message sent from Flask-Mail"
        q= {'token': token}
        msg.body =  "http://192.168.56.107:31017/new_password?{}".format(urllib.parse.urlencode(q))
        mail.send(msg)
    return render_template("forget_password.html", title='Forget Password', form=form)


def access_reset_password_page(func):
    def wrapper():
        token_from_url = request.args.get('token')
    #Users.query.filter_by(public_id=data['public_id']).first()
    #if User.query.filter(user.token=token_from_url).first():
    #if User.query.filter(token=token_from_url).first():
        func()
    #else:
     # return "you need to be admin", 401
    return wrapper


@access_reset_password_page
def check_access():
    form = NewPassord()
    return render_template("new_password.html", form=form)


@app.route('/new_password', methods=['GET', 'POST'])
def new_password():
    form = NewPassord()
    global token_from_url
    if request.method == 'GET':
        token_from_url = request.args.get('token')
        if User.query.filter(User.token==token_from_url).first():
            x=User.query.filter(User.token==token_from_url).first()
            return render_template("new_password.html", title='New Password', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user_iid = User.query.filter(User.token==token_from_url).first()
            password = generate_password_hash(form.password.data)
            user_tuple = (password, user_iid.email)
            conntdb = sqlite3.connect('app.db')
            cur = conntdb.cursor()
            sqlite_insert_with_param = """UPDATE user  set  password_hash=?  where email = ?;"""
            print(sqlite_insert_with_param)
            print(sqlite_insert_with_param)
            cur.execute(sqlite_insert_with_param, user_tuple)
            cur.close()
            conntdb.commit()
            conntdb.close()
    return redirect(url_for('index'))


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


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = form.search.data
        item_list = Cart.query.filter(Cart.part_name.like(f'%{query}%'))
        it_list=[]
        for i in item_list:
            print(i.part_name)
            it_list.append(i)
        return render_template('search_results.html', all_items=it_list)  # or what you want
    return render_template('search.html', form=form)


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


def session_data():
    user_iid = current_user.id
    user_tuple = (user_iid)
    conntdb = sqlite3.connect('app.db')
    cur = conntdb.cursor()
    sql_select_query_cart = """select prod_id from  subs where id=?"""
    cur.execute(sql_select_query_cart, [user_tuple])
    print(sql_select_query_cart)
    results = cur.fetchall()
    out = [item for t in results for item in t]
    cur.close()
    conntdb.close()
    #print(out)
    final_data = {}
    for r in out:
        #print(r)
        conntdb = sqlite3.connect('app.db')
        user_iid = current_user.id
        u_table = (user_iid, r)
        cart_count = """select cart_count from subs where id=?  and prod_id=?"""
        x = conntdb.execute(cart_count, u_table)
        item_count_total = x.fetchall()
        out = [item for t in item_count_total for item in t]
        final_o = (out[0])
        conntdb.close()
        final_data[r] = final_o
    return final_data
    #print(final_data)
    session['my_session_id'] = session_data()


@app.route('/delivery_address', methods=['GET', 'POST'])
@login_required
def delivery_address():
    form = HomeAddressForm()
    if request.method == 'POST':
        if not Order.query.get(1):
            if form.validate_on_submit():
                session['address'] = form.order_user_address.data
                all_addr_item = []
                # for key, value in session['my_session_id'].items():
                #     print(key)
                add_addr = Order(order_user_address=session['address'], order_item_detail=session['my_session_id'], order_user_id=current_user.id)
                db.session.add(add_addr)
                db.session.commit()
        else:
            print('Updating')
            q=Order.query.get(1)
            q.order_item_detail = session_data()
            print(q.order_item_detail)
            db.session.add(q)
            db.session.commit()
    d = []
    q=Order.query.filter(Order.order_user_id==current_user.id).all()
    def myval():
        for i in q:
            for k,v in i.order_item_detail.items():
                #print(k)
                c = Cart.query.filter(Cart.prod_id==k)
                #print(c.prod_id)
                d.append(c)
        return d
    # print(type(d))
    # print(d)
    #x = myval()
    my_purchase_list=[]
    for o in myval():
        for t in o:
            print(type(t))
            my_purchase_list.append(t)
    print(my_purchase_list)
    # print(myval())
    # print(myval())
    # print(myval())
    return render_template('delivery_address.html', title='Delivery address', form=form , order_list=q, item=my_purchase_list)


@app.route('/change_pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    form = ChangePass()
    if form.validate_on_submit():
        user_iid = current_user.id
        password = generate_password_hash(form.password.data)
        user_tuple = (password, user_iid)
        conntdb = sqlite3.connect('app.db')
        cur = conntdb.cursor()
        sqlite_insert_with_param = """UPDATE user  set  password_hash=?  where id = ?;"""
        cur.execute(sqlite_insert_with_param, user_tuple)
        cur.close()
        conntdb.commit()
        conntdb.close()
    return render_template('change_pass.html', title='Change Password', form=form)



@app.route('/total_item', methods=['GET'])
@login_required
def total_item():
    u = User.query.get(current_user.id)
    all_items = u.cart_item.all()
    print(u)
    print(all_items)
    # if not request.cookies.get('foo'):
    my_total_item_list = Cart.query.paginate(per_page=1, page=1, error_out=True )
    res = make_response(render_template('total_item.html', title='Total Items', all_items=all_items, my_total_item_list=my_total_item_list))
    res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2, domain='devops.com',  httponly=True)
    res.set_cookie('all_items', 'all_items', max_age=60 * 60 * 24 * 365 * 2, domain='devops.com', httponly=True )
    res.set_cookie('all_items', 'all_items', max_age=60 * 60 * 24 * 365 * 2, domain='devops.com', httponly=True)
    # else:
    #     res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    #     print("Value of cookie foo is {}".format(request.cookies.get('foo')))

    return res


@app.route('/paginator/<int:page_num>')
@login_required
def paginator(page_num):
    u = User.query.get(current_user.id)
    all_items = u.cart_item.all()
    my_total_item_list = Cart.query.paginate(per_page=2, page=page_num, error_out=True)
    return render_template('paginator.html', title='Total Items', all_items=all_items, my_total_item_list=my_total_item_list)





@app.route('/about_item/<int:id>', methods=['GET'])
@login_required
def about_item(id):
    carts = Cart.query.filter_by(prod_id=id).first_or_404()
    print(type(carts.prod_id))
    print(type(carts))
    print(carts)
    my_cart_list = []
    # res = make_response(render_template('about_item.html', title='About Items', all_items=carts))
    # res.set_cookie("item", str(carts), max_age=60 * 60 * 24 * 365 * 2,  httponly=True)
    # res.set_cookie("item_id", json.dumps(carts.prod_id), max_age=60 * 60 * 24 * 365 * 2, httponly=True)
    # print(request.cookies.get('session').split(".")[0])
    # print(request.cookies.get('session'))
    # res.headers['X-Parachutes'] = 'parachutes are cool'
    # res.headers['X-Content-Type-Options'] = 'nosniff'
    # print(request.cookies.get('item'))
    # for key in store.keys():
    #     print(key)
############################
#    if request.method = 'GET':
    user_iid = current_user.id
    user_tuple = (user_iid)
    conntdb = sqlite3.connect('app.db')
    cur = conntdb.cursor()
    sql_select_query_cart = """select prod_id from  subs where id=?"""
    cur.execute(sql_select_query_cart, [user_tuple])
    print(sql_select_query_cart)
    results = cur.fetchall()
    out = [item for t in results for item in t]
    cur.close()
    conntdb.close()
    print(out)
    final_data = {}
    for r in out:
        # print(r)
        conntdb = sqlite3.connect('app.db')
        user_iid = current_user.id
        u_table = (user_iid, r)
        cart_count = """select cart_count from subs where id=?  and prod_id=?"""
        x = conntdb.execute(cart_count, u_table)
        item_count_total = x.fetchall()
        out = [item for t in item_count_total for item in t]
        final_o = (out[0])
        conntdb.close()
        final_data[r] = final_o
        print(type(final_data))
        print(final_data)
        print(final_data)
        print(final_data)
        print(final_data)
    return render_template('about_item.html', title='Total Items', all_items=carts, all_items_data=final_data)
    ###################################
     #print(request.cookies.get(int(carts.prod_id)))
    #return  res
    #res.set_cookie('all_items', 'all_items', max_age=60 * 60 * 24 * 365 * 2, domain='devops.com', httponly=True )

#
# @app.route('/my_liked_item', method=['GET'])
# @login_required
# def my_liked_item():
#     if request.cookies.get()

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
            conn.close()

#    if request.method == 'GET':
    user_iid = current_user.id
    user_tuple = (user_iid)
    conntdb = sqlite3.connect('app.db')
    cur = conntdb.cursor()
    sql_select_query_cart = """select prod_id from  subs where id=?"""
    cur.execute(sql_select_query_cart, [user_tuple])
    print(sql_select_query_cart)
    results = cur.fetchall()
    out = [item for t in results for item in t]
    cur.close()
    conntdb.close()
    #print(out)
    final_data = {}
    for r in out:
        #print(r)
        conntdb = sqlite3.connect('app.db')
        user_iid = current_user.id
        u_table = (user_iid, r)
        cart_count = """select cart_count from subs where id=?  and prod_id=?"""
        x = conntdb.execute(cart_count, u_table)
        item_count_total = x.fetchall()
        out = [item for t in item_count_total for item in t]
        final_o = (out[0])
        conntdb.close()
        final_data[r] = final_o
    print(final_data)
    session['my_session_id'] = final_data
    my_all_items = Cart.query.all()

    flash('Add Item to cart, Now Count is {}, !'.format(carts.part_name))
    #return render_template('cart_added_item.html', title='Cart Items', all_items=final_data, my_all_items=my_all_items)
    #return render_template('all_added_item.html', title='Cart Items', all_items=final_data, my_all_items=my_all_items)
    return render_template('about_item.html', title='Total Items', all_items=carts, all_items_data=final_data)


@app.route('/get_all_from_cart')
@login_required
def get_all_from_cart():
    user_iid = current_user.id
    user_tuple = (user_iid)
    conntdb = sqlite3.connect('app.db')
    cur = conntdb.cursor()
    sql_select_query_cart = """select prod_id from  subs where id=?"""
    cur.execute(sql_select_query_cart, [user_tuple])
    print(sql_select_query_cart)
    results = cur.fetchall()
    print(results)
    out = [item for t in results for item in t]
    cur.close()
    conntdb.close()
    # print(out)
    final_data = {}
    for r in out:
        # print(r)
        conntdb = sqlite3.connect('app.db')
        user_iid = current_user.id
        u_table = (user_iid, r)
        cart_count = """select cart_count from subs where id=?  and prod_id=?"""
        x = conntdb.execute(cart_count, u_table)
        item_count_total = x.fetchall()
        out = [item for t in item_count_total for item in t]
        final_o = (out[0])
        print(final_o)
        conntdb.close()
        if not final_o == 0:
            final_data[r] = final_o
    print(type(final_data))
    print(type(final_data))
    print(final_data)
    # carts = Cart.query.all()
    my_all_items = Cart.query.all()

    return render_template('get_all_from_cart.html', title='Total Items', all_items=final_data, my_all_items=my_all_items)


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

        user_iid = current_user.id
        user_tuple = (user_iid)
        conntdb = sqlite3.connect('app.db')
        cur = conntdb.cursor()
        sql_select_query_cart = """select prod_id from  subs where id=?"""
        cur.execute(sql_select_query_cart, [user_tuple])
        print(sql_select_query_cart)
        results = cur.fetchall()
        out = [item for t in results for item in t]
        cur.close()
        conntdb.close()
        # print(out)
        final_data = {}
        for r in out:
            # print(r)
            conntdb = sqlite3.connect('app.db')
            user_iid = current_user.id
            u_table = (user_iid, r)
            cart_count = """select cart_count from subs where id=?  and prod_id=?"""
            x = conntdb.execute(cart_count, u_table)
            item_count_total = x.fetchall()
            out = [item for t in item_count_total for item in t]
            final_o = (out[0])
            print(final_o)
            print(final_o)
            print(final_o)
            conntdb.close()

            if (final_o == 0):
                conntdb = sqlite3.connect('app.db')
                cur = conntdb.cursor()
                count_iid = 0
                u_table = (count_iid)
                sql_select_query_cart = """delete FROM subs WHERE cart_count=?;"""
                cur.execute(sql_select_query_cart, [u_table])
                print('Operation done successfully')
                cur.close()
                conntdb.commit()
                conntdb.close()
            else:
                print('adding more dataaaaaaaaaaaaaaaaaaaaaaaa')
                final_data[r] = final_o
            final_data[r] = final_o
        print(type(final_data))
        #carts = Cart.query.all()
        my_all_items = Cart.query.all()


        #flash('Add Item to cart, Now Count is {}, !'.format(carts.part_name))
    return render_template('about_item.html', title='Total Items', all_items=carts, all_items_data=final_data)
    #return render_template('cart_added_item.html', title='Total Items', all_items=final_data, my_all_items=my_all_items)


# @login_required
# @app.context_processor
# def context_process():
from flask import  session
from datetime import timedelta
import time


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=50000)
    print(app.permanent_session_lifetime)
    print(timedelta(minutes=5))


# @login_required
# @app.before_request
# def counter_clock():
#     for mycurrent_time in reversed(range(0, 10)):
#         time.sleep(1)
#         #print("%s\r" % i)
#         return print(mycurrent_time)

