from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user

from database import *
from forms import RegisterForm, LoginForm, NewCafeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'duyasvfxjhcryt52sx3xqscytxx1ex'

Bootstrap(app)

db.init_app(app)
app.app_context().push()
# db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


# login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def user_logged_in():
    return dict(logged_in=current_user.is_authenticated)


@app.context_processor
def is_admin():
    if not current_user.is_anonymous and current_user.id == 1:
        return dict(is_admin=True)
    else:
        return dict(is_admin=False)


# web route
@app.route("/")
def home():
    cafe_table = db.session.query(Cafe).all()
    return render_template('index.html', table_a=cafe_table)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = read_user(email)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Wrong password. Please Try again.")
        else:
            flash("That email does not exist. Please Try again.")
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if read_user(request.form["email"]):
            flash("That email already exists. Please log in.")
            return redirect(url_for("login"))
        else:
            hash_ = generate_password_hash(password=request.form["password"], method="pbkdf2:sha256", salt_length=8)
            new_user = User(name=request.form["name"],
                            email=request.form["email"],
                            password=hash_)
            create_record(new_user)
            login_user(new_user)
            return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/add-new-cafe", methods=["GET", "POST"])
def add_new_cafe():
    form = NewCafeForm()
    if request.method == 'POST' and form.validate_on_submit():
        if read_cafe(request.form["name"]):
            flash("That Cafe already exists.")
            return redirect(url_for("add_new_cafe"))
        else:
            new_cafe = Cafe(name=request.form["name"],
                            map_url=request.form["map_url"],
                            img_url=request.form["img_url"],
                            location=request.form["location"],
                            has_sockets=(True if request.form["has_sockets"] == "y" else False),
                            has_toilet=(True if request.form["has_toilet"] == "y" else False),
                            has_wifi=(True if request.form["has_wifi"] == "y" else False),
                            can_take_calls=(True if request.form["can_take_calls"] == "y" else False),
                            seats=request.form["seats"],
                            coffee_price=request.form["coffee_price"], )
            create_record(new_cafe)
            return redirect(url_for("home"))
    return render_template("new_cafe.html", form=form)


@app.route("/delete")
def delete():
    cafe_id = request.args.get('id')

    # DELETE A RECORD BY ID
    entry_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)