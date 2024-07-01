import flask
# from flask_mail import Mail
from flask import request ,redirect ,url_for
from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
import json

with open('D:/rayhan-drive/flask/flask1/config.json','r', encoding='utf-8')  as c:
    paramiters=json.load(c)["paramiters"]

with open('D:/rayhan-drive/flask/flask1/blogs.json','r', encoding='utf-8')  as s:
    blogs=json.load(s)["blogs"]

local_server=True

panel = Flask(__name__)

if local_server:
    panel.config["SQLALCHEMY_DATABASE_URI"] = paramiters['local_uri']
else:
    panel.config["SQLALCHEMY_DATABASE_URI"] = paramiters['prodaction_uri']

db = SQLAlchemy(panel)


class Sign_in(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False)
    last_name = db.Column(db.String(80), unique=False)
    phone_num = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    birthday = db.Column(db.String(1200), unique=False)
    age = db.Column(db.String(10), unique=False)
    country=db.Column(db.String(40), unique=False)

class Login(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    unameemail = db.Column(db.String(100), unique=False)
    password = db.Column(db.String(100), unique=False)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique=False)
    message = db.Column(db.String(1000), unique=False)

class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(30), unique=False)
    slug = db.Column(db.String(50), unique=True)
    content = db.Column(db.String(1000), unique=False)
    date = db.Column(db.String(10), unique=False)



@panel.route("/", methods=["GET", "POST"])
def first_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        entry = Login(unameemail=username, password=password)
        db.session.add(entry)
        db.session.commit()
        if username == paramiters['admin_name'] and password == paramiters['admin_pass'] or username == paramiters['admin_name1'] and password == paramiters['admin_pass1']:
            return redirect(url_for('home'))
    return render_template("first_login.html")
@panel.route("/home")
def home():
    b=blogs
    return render_template("index.html",b=b)
@panel.route("/post/<string:post_slug>",methods=["GET"])
def postx(post_slug):
    post=Post.query.filter_by(slug=post_slug).first()
    return render_template("post.html",post=post)


@panel.route("/about")
def about():
    p=paramiters
    return render_template("about.html",p=p)

@panel.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name=request.form.get("username")
        emiall=request.form.get("email")
        messagex=request.form.get("message")
        entry=Contact(username=name, email=emiall,message=messagex)
        db.session.add(entry)
        db.session.commit()
        return render_template("scontac.html")
    return render_template("contact.html")
@panel.route("/blog")
def Xblog():
    b=blogs
    return render_template("blog.html",b=b)

@panel.route("/login", methods=["GET", "POST"])
def Xlogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        entry = Login(unameemail=username, password=password)
        db.session.add(entry)
        db.session.commit()
        return render_template("slogin.html")
    return render_template("login.html")
@panel.route("/sign", methods=['GET', 'POST'])
def sign_in():
    if request.method == "POST":
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        number = request.form.get("phone")
        mail = request.form.get("email")
        birthday = request.form.get("birthday")
        age = request.form.get("age")
        country=request.form.get("country")
        entry = Sign_in(first_name=fname, last_name=lname, phone_num=number, email=mail, birthday=birthday, age=age , country=country)
        db.session.add(entry)
        db.session.commit()
        return render_template("ssignin.html")
    return render_template("sign.html")

@panel.route("/ssignin")
def ssignin(): 
    return render_template("ssignin.html")

@panel.route("/first_sign")
def frist_sign(): 
    return render_template("first_sign.html")

@panel.route("/users",methods=["GET"])
def userd(): 
    users=Sign_in.query.all()
    return render_template("users.html",users=users)

@panel.route("/addpost",methods=["GET","POST"])
def addpost(): 
    
    if request.method == "POST":
        titel=request.form.get("title")
        slug=request.form.get("slug")
        content=request.form.get("content")
        date=request.form.get("date")
        entry=Post(titel=titel,slug=slug,content=content,date=date)
        db.session.add(entry)
        db.session.commit()
    return render_template("addpost.html")

@panel.route("/addpostlogin",methods=["GET","POST"])
def addlogin(): 
    user=request.form.get("username")
    password=request.form.get("password")
    if user==paramiters["loguser"] and password==paramiters["logpass"]:
        return redirect(url_for("addpost"))
    return render_template("addpostlogin.html")

panel.run(debug=True)