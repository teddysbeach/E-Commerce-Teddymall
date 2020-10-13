from app import app, db
from flask import request, url_for, render_template, redirect, session, g, flash
from app.models import User, Comment, Product, Transaction

@app.before_request
def loadSession():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        g.user = User.query.filter_by(username=username).first()

@app.route('/')
def index():
    new = Product.query.all()
    products = Product.query.all()
    return render_template('index.html', products=products, newProducts=new)

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if('username' in session):
        return redirect(url_for('index'))
    if(request.method == 'POST'):
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(username=name).first()
        if(user):
            if(user.tryLogin(password)):
                session['username'] = user.username
                if(user.privilege == 1):
                    session['admin'] = True
                return redirect(url_for('index'))
            else:
                flash('비밀번호가 틀립니다.')
                return render_template('login.html')
        else:
            flash('해당하는 아이디가 존재하지 않습니다.')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if('username' in session):
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/me')
def me():
    if('username' in session):
        user = getUser(session['username'])
        return render_template('me.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if(request.method == 'POST'):
        username = request.form['name']
        nickname = request.form['nickname']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        
        user = User(username, nickname, password, 0, email, address)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as E:
            flash(E.__str__())
            return render_template('register.html')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/post', methods=['POST', 'GET'])
def post():
    if(request.method == 'POST'):
        productTitle = request.form['name']
        productImg = request.form['img']
        productPrice = request.form['price']
        productDesc = request.form['description']
        productAuthor = request.form['userId']
        productType = request.form['pType']
        product = Product(productTitle, productImg, productPrice, productDesc, productAuthor, productType)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('upload.html', user=g.user)


def getUser(username):
    return User.query.filter_by(username=username).first()
