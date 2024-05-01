from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, WorkOrder
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    work_orders = WorkOrder.query.all()
    return render_template("home.html", user=current_user, work_orders=work_orders)


@views.route("/create-workorder", methods=['GET', 'POST'])
@login_required
def create_workorder():
    if request.method == "POST":
        equipment = request.form.get('equipment')
        department = request.form.get('department')
        work = request.form.get('work')

        if not (equipment and department and work):
            flash('Workorder cannot be empty', category='error')
        else:
            work_order = WorkOrder(equipment_name=equipment, department=department, work_requested=work, user_id=current_user.id)
            db.session.add(work_order)
            db.session.commit()
            flash('Workorder created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_workorder.html', user=current_user)

@views.route("/delete-workorder/<id>")
@login_required
def delete_workorder(id):
    workorder = WorkOrder.query.filter_by(id=id).first()

    if not workorder:
        flash("Workorder does not exist.", category='error')
    elif current_user.id != workorder.user_id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(workorder)
        db.session.commit()
        flash('Workorder deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/workorders/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    workorders = user.work_orders
    return render_template("workorders.html", user=current_user, work_orders=workorders, username=username)