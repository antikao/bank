from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from .models import User, Account, Transaction
from . import db
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    accounts = current_user.accounts
    return render_template('profile.html', name = current_user.name, accounts = accounts) 
 
@main.route('/accounts', methods=["POST"])
@login_required
def create_account():
    new_account = Account(user_id=current_user.id)
    db.session.add(new_account)
    db.session.commit()
    return redirect("/profile")

@main.route('/delete_account/<int:account_id>')
@login_required
def accounts_deletion(account_id):
    deleting_account = Account.query.filter_by(id=account_id).first()
    if deleting_account.balance > 0:
        other_accounts = Account.query.filter(Account.user_id==current_user.id, Account.id != account_id).all()
        return render_template('delete_account.html', name = current_user.name, other_accounts = other_accounts, account = deleting_account)
    else:
       Account.query.filter_by(id=account_id).delete()
       db.session.commit()
       return redirect("/profile")

@main.route('/accounts/<int:account_id>/delete', methods=["POST"])
@login_required
def delete_account(account_id):
    reserve_account_id = request.form["selected_account"]
    deleting_account = Account.query.filter_by(id=account_id).first()
    reserve_account = Account.query.filter_by(id=reserve_account_id).first()
    Account.query.filter_by(id=reserve_account_id).update({"balance":reserve_account.balance+deleting_account.balance})
    Account.query.filter_by(id=deleting_account.id).delete()
    db.session.commit()
    return redirect("/profile")

@main.route('/accounts/<int:account_id>')
@login_required
def account_card(account_id):
    account=Account.query.filter_by(id=account_id).first()
    transactions = Transaction.query.filter(or_(Transaction.sender_account_id == account_id, Transaction.referer_account_id == account_id)).all()
    return render_template("account_card.html", transactions = transactions, account=account)


@main.route('/transactions', methods=["POST"])
@login_required
def create_transaction():
    referer_account_number = request.form["account_number"]
    amount = request.form["amount"]
    sender_account_id = request.form["sender_account_id"]
    sender_account = Account.query.filter_by(id=sender_account_id).first()
    if sender_account.balance < float(amount):
        flash('Недостаточно денег на счету.')
        return redirect(url_for('main.account_card', account_id=sender_account_id))
    referer_account = Account.query.filter_by(number=referer_account_number).first()
    if referer_account is None:
        flash('Указан неверный кошелек получателя')
        return redirect(url_for('main.account_card', account_id=sender_account_id))
    db.session.add(Transaction(amount=amount, sender_user_id=sender_account.user_id, referer_user_id=referer_account.user_id, sender_account_id=sender_account_id, referer_account_id=referer_account.id))
    db.session.commit()
    return redirect(f"/accounts/{sender_account_id}")


        
