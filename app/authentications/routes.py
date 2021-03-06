from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from . import authentications
from . forms import LoginForm
from .. models import User

@authentications.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Name = form.name.data).first()
        if user is not None and user.verifyPassword(form.password.data) and user.Enabled:
            login_user(user, form.rememberMe.data)
            return redirect(request.args.get("next") or url_for("main.index"))

        flash("Invalid username and/or password or disabled user.", "alert alert-danger")

    return render_template("authentications/login.html", form = form)

@authentications.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "alert alert-success")
    return redirect(url_for("main.index"))
