from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import app, db, login_manager
from app.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User, Team, Tag

@app.route("/")
def index():
    return redirect(url_for("user_list"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("user_list"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("user_list"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/teams")
def team_list():
    teams = Team.query.order_by(Team.created_at.desc()).all()
    return render_template("team_list.html", teams=teams)

@app.route("/teams/create", methods=["GET", "POST"])
def create_team():
    if request.method == "POST":
        team = Team(name=request.form["name"])
        db.session.add(team)
        db.session.commit()
        return redirect(url_for("team_list"))
    return render_template("create_team.html")

@app.route("/users")
def user_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("user_list.html", users=users)

@app.route("/users/<int:user_id>")
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.profile = form.profile.data
        current_user.team_id = form.team_id.data
        db.session.commit()
        return redirect(url_for("user_list"))
    return render_template("profile.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)