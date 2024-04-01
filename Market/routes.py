from Market import app
from flask import render_template, url_for, redirect, flash, request
from Market.models import Itemdb1, Userdb, db
from Market.forms import RegisterForm, LoginForm, PurchaseItem, SellItem
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/market", methods=['GET', 'POST'])
@login_required  # It will not let user directly enter to market without login or registration
def market():
    purchaseform = PurchaseItem()
    sellform = SellItem()
    if request.method == "POST":
        purchasedItem = request.form.get('purchase')
        sellItem = request.form.get('sold')
        s_item_object = Itemdb1.query.filter_by(name=sellItem).first()
        p_item_object = Itemdb1.query.filter_by(name=purchasedItem).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                # p_item_object.owner_id = current_user.id
                # current_user.budget -= p_item_object.price
                # db.session.commit()
                flash(f"Purchased {p_item_object.name} successfully!", category='success')
            else:
                flash("Not Enough Budget to purchase this Item!", category='danger')
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Sold {s_item_object.name} to MarketPlace successfully!", category='success')
            else:
                flash("Something went wrong, Try Again!", category='danger')
        return redirect(url_for('market'))
    if request.method == 'GET':   # by this that resubmission popup will not occur anymore
        items = Itemdb1.query.filter_by(owner_id=None)
        owned_items = Itemdb1.query.filter_by(owner_id=current_user.id)
        return render_template("market.html", item=items, purchaseform=purchaseform, sellform=sellform, owned_items=owned_items)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_add = Userdb(uname=form.uname.data,
                             email=form.email.data,
                             password_hash=form.pass1.data)
        db.session.add(user_to_add)
        db.session.commit()
        login_user(user_to_add)
        flash(f"Account Created Successfully as  {user_to_add.uname}", category='success')
        return redirect(url_for("market"))
    if form.errors != {}:
        for i in form.errors.values():
            flash(i, category='danger')
    return render_template("registration.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Userdb.query.filter_by(uname=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            print(attempted_user)
            login_user(attempted_user)
            flash(f"Login Successfully as {attempted_user.uname}", category='success')
            return redirect(url_for('market'))
        else:
            flash('Invalid Credentials', category='danger')

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logout Successfully!", category='info')
    return redirect(url_for('index'))
