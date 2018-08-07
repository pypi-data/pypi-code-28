from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, \
    current_user

from app.auth.forms import RegistrationForm
from app.auth.models import CommonUserInfo
from . import auth
from .. import db



#
# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         if not current_user.confirmed \
#                 and request.endpoint \
#                 and request.endpoint[:5] != 'auth.' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('auth.unconfirmed'))

@auth.before_app_request
def before_request():
    pass
    current_app.logger.warning(current_user)
    # if not current_user.is_authenticated:
    #     flash('用户名或密码错误，请重新登录！', 'danger')
    #     return redirect(url_for('auth.login'))
#
#
# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')
#

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
       登录方法
       :return:
       """
    if request.method == 'POST':

        user = CommonUserInfo.query.filter_by(login_account=request.form['login_account']).first()

        current_app.logger.warning("===登录日志===")

        if user is not None and user.verify_password(request.form['password']):
            login_user(user, True)
            return redirect(url_for('main.index'))

        else:
            flash('用户名或密码错误，请重新登录！', 'warning')

            return redirect(request.args.get('next') or url_for('auth.login'))

    #
    #
    #
    # if user is not None and user.verify_password(request.form['password']):
    #     login_user(user, True)
    #     return redirect(request.args.get('next') or url_for('main.index'))
    #     flash('Invalid username or password.')
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('系统注销成功！','success')
    return redirect(url_for('auth.login'))




@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = CommonUserInfo(email=form.email.data,
                    login_account=form.login_account.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        flash('注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)








@auth.route('/ytxtest', methods=['GET', 'POST'])
def ytxtest():
    error = None

    
    print("order_code:%s" % (request.form['order_code']))
    print("FKEY:"+request.form['FKEY'])
    print("=====")
    print("imageFile:"+request.form['imageFile'][0:100])

    return "{'flag':'true',msg:'测试图片上传成功'}"

#
#
# @auth.route('/confirm/<token>')
# @login_required
# def confirm(token):
#     if current_user.confirmed:
#         return redirect(url_for('main.index'))
#     if current_user.confirm(token):
#         flash('You have confirmed your account. Thanks!')
#     else:
#         flash('The confirmation link is invalid or has expired.')
#     return redirect(url_for('main.index'))
#
#
# @auth.route('/confirm')
# @login_required
# def resend_confirmation():
#     token = current_user.generate_confirmation_token()
#     send_email(current_user.email, 'Confirm Your Account',
#                'auth/email/confirm', user=current_user, token=token)
#     flash('A new confirmation email has been sent to you by email.')
#     return redirect(url_for('main.index'))
#
#
# @auth.route('/change-password', methods=['GET', 'POST'])
# @login_required
# def change_password():
#     form = ChangePasswordForm()
#     if form.validate_on_submit():
#         if current_user.verify_password(form.old_password.data):
#             current_user.password = form.password.data
#             db.session.add(current_user)
#             flash('Your password has been updated.')
#             return redirect(url_for('main.index'))
#         else:
#             flash('Invalid password.')
#     return render_template("auth/change_password.html", form=form)
#
#
# @auth.route('/reset', methods=['GET', 'POST'])
# def password_reset_request():
#     if not current_user.is_anonymous:
#         return redirect(url_for('main.index'))
#     form = PasswordResetRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             token = user.generate_reset_token()
#             send_email(user.email, 'Reset Your Password',
#                        'auth/email/reset_password',
#                        user=user, token=token,
#                        next=request.args.get('next'))
#         flash('An email with instructions to reset your password has been '
#               'sent to you.')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html', form=form)
#
#
# @auth.route('/reset/<token>', methods=['GET', 'POST'])
# def password_reset(token):
#     if not current_user.is_anonymous:
#         return redirect(url_for('main.index'))
#     form = PasswordResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None:
#             return redirect(url_for('main.index'))
#         if user.reset_password(token, form.password.data):
#             flash('Your password has been updated.')
#             return redirect(url_for('auth.login'))
#         else:
#             return redirect(url_for('main.index'))
#     return render_template('auth/reset_password.html', form=form)
#
#
# @auth.route('/change-email', methods=['GET', 'POST'])
# @login_required
# def change_email_request():
#     form = ChangeEmailForm()
#     if form.validate_on_submit():
#         if current_user.verify_password(form.password.data):
#             new_email = form.email.data
#             token = current_user.generate_email_change_token(new_email)
#             send_email(new_email, 'Confirm your email address',
#                        'auth/email/change_email',
#                        user=current_user, token=token)
#             flash('An email with instructions to confirm your new email '
#                   'address has been sent to you.')
#             return redirect(url_for('main.index'))
#         else:
#             flash('Invalid email or password.')
#     return render_template("auth/change_email.html", form=form)
#
#
# @auth.route('/change-email/<token>')
# @login_required
# def change_email(token):
#     if current_user.change_email(token):
#         flash('Your email address has been updated.')
#     else:
#         flash('Invalid request.')
#     return redirect(url_for('main.index'))

@auth.route('/secret')
def secret():
    return 'Only authenticated users are allowed!'