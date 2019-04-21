from app import limiter
from flask_user import roles_required
from flask import Flask, render_template, flash, redirect, url_for, request, session, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import app, db, secrets  # , mysql
from app.auth.forms import LoginForm, RegistrationForm, RecoverForm
from app.forms import LanguageForm, LoginForm, GetLanguage
from app.ticket.forms import TicketForm, ViewForm, ResolveForm
from app.models import User, Tickets, UserRoles, Messages
from app import secrets
import requests
import uuid
from datetime import datetime
from io import BytesIO
from base64 import b64encode
bearer_token = secrets.bearer_token


# sanitize form inputs
# flask-user implementation


def getRole():
    user = User.query.filter_by(username=current_user.username).first().id
    role = UserRoles.query.filter_by(user_id=user).first()
    if role:
        roleid = int(role.role_id)
    else:
        roleid = 0
    return roleid


def getNotif():
    tickets = Tickets.query.filter_by(status="New").all()
    return len(tickets)

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        roleid = getRole()
        notif = getNotif()
        return render_template('index.html', title='Home', user=roleid, notif=notif)
    else:
        return render_template('index.html', title='Home')


@app.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    form = TicketForm()
    roleid = getRole()
    if request.method == 'POST':
        if form.validate_on_submit():
            options = form.options.data
            details = form.details.data
            title = form.title.data
            uid = uuid.uuid1()
            user = current_user.username
            email = current_user.email
            status = "New"
            isdelete = 0
            date = datetime.today()
            if form.file.data:
                file = form.file.data.read()
                ticket = Tickets(id=uid, name=user, options=options, title=title,
                                 details=details, status=status, isdelete=isdelete, upload=file, date=date)
            else:
                ticket = Tickets(id=uid, name=user, options=options, title=title,
                                 details=details, status=status, isdelete=isdelete, date=date)
            emailsending(uid, user, email)
            db.session.add(ticket)
            db.session.commit()
            flash('Your ticket has been successfully submitted.')
            return redirect(url_for('index'))
        else:
            flash('Error: File must be jpg or png')
    return render_template('ticket.html', title='Ticket', form=form, user=roleid)


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("40 per minute", methods=['POST'], error_message='Too Many Requests!')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ticket'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', user_data=current_user)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were successfully logged out.")
    return redirect("/login")


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


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = RecoverForm()
    print('recover password')
    if form.validate_on_submit():
        if form.email.data:
            print(form.email.data)
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                recoverPasswordEmail(user.username, form.email.data)
    return render_template('forgot.html', title='Recover Password', form=form)


@app.route('/profile')
@login_required
def profile():
    roleid = getRole()
    user = current_user.username
    tickets = Tickets.query.filter_by(name=user).all()
    # print(tickets)
    return render_template('profile.html', title='Profile', tickets=tickets, user=roleid)


@app.route('/archiving/<id>', methods=(['GET', 'POST']))
@roles_required('admin')
def archivingTicket(id):
    tickets = Tickets.query.get(id)
    if tickets.status != "New":
        tickets.isdelete = 1
        db.session.commit()
        return 'success'
    else:
        flash("Issue is not resolved, unable to archive")
        return 'fail'


@app.route('/deleting/<id>', methods=(['GET', 'POST']))
@roles_required('admin')
def deletingTicket(id):
    tickets = Tickets.query.get(id)
    db.session.delete(tickets)
    db.session.commit()
    return 'success'


@app.route('/submissions/<id>', methods=(['GET', 'POST']))
@login_required
# @roles_required('admin')
def submission(id):
    roleid = getRole()
    notif = getNotif()
    tickets = Tickets.query.get(id)
    if(roleid == 1 or current_user.username == tickets.name):
        form = ViewForm()
        form2 = ResolveForm()
        form3 = ResolveForm()
        user = current_user
        tickets = Tickets.query.get(id)
        allMsg = Messages.query.filter_by(ticket_id=id).all()
        print(allMsg)
        if form.validate_on_submit():
            emailstring = form.replytext.data
            ticket = Tickets.query.filter_by(id=id).first()
            user = User.query.filter_by(username=ticket.name).first()
            emailreply(emailstring, id, ticket.name, user.email)
            ticket.status = 'Pending'
            db.session.commit()
            return redirect('/submissions')
        elif form2.validate_on_submit():
            ticket = Tickets.query.filter_by(id=id).first()
            ticket.status = 'Resolved'
            db.session.commit()
            return redirect('/submissions')
        elif form3.validate_on_submit():
            return redirect('/submissions/<id>')
        return render_template('submissionById.html', title='Submission', tickets=tickets, form=form, form2=form2,
                               form3=form3, messages=allMsg, user=roleid, notif=notif)
    else:
        return render_template('errorhandlers/401.html'), 401


# @app.route('/archive/<id>', methods=(['GET', 'POST', 'DELETE']))
# @login_required
# @roles_required('admin')
# def archivedTicket(id):
#     notif = getNotif()
#     roleid = getRole()
#     if request.method == 'DELETE':
#         tickets = Tickets.query.get(id)
#         db.session.delete(tickets)
#         db.session.commit()
#         return 'success'
#     else:
#         form = ViewForm()
#         form2 = ResolveForm()
#         form3 = ResolveForm()

#         tickets = Tickets.query.get(id)
#         if form.validate_on_submit():
#             emailstring = form.replytext.data
#             ticket = Tickets.query.filter_by(id=id).first()
#             user = User.query.filter_by(username=ticket.name).first()
#             emailreply(emailstring, id, ticket.name, user.email)
#             ticket.status = 'Pending'
#             db.session.commit()
#             return redirect('/archive')
#         elif form2.validate_on_submit():
#             ticket = Tickets.query.filter_by(id=id).first()
#             ticket.status = 'Resolved'
#             db.session.commit()
#             return redirect('/archive')
#         elif form3.validate_on_submit():
#             return redirect('/archive')
#         return render_template('archiveById.html', title='Archive', tickets=tickets, form=form, form2=form2, form3=form3, user=roleid, notif=notif)


@app.route('/submissions/attachment/<id>')
@login_required
def attachment(id):
    roleid = getRole()
    notif = getNotif()
    ticket = Tickets.query.get(id)
    if roleid == 1 or current_user.username == ticket.name:
        img = BytesIO(ticket.upload)
        img64 = b64encode(img.read())
        return render_template('attachment.html', image=img64.decode('utf8'), user=roleid, notif=notif)
    else:
        return render_template('errorhandlers/401.html'), 401


@app.route('/submissions')
@login_required
@roles_required('admin')
def submissions():
    roleid = getRole()
    notif = getNotif()
    tickets = Tickets.query.filter_by(isdelete=0).all()
    # print(tickets)
    return render_template('submissions.html', title='Submissions', tickets=tickets, user=roleid, notif=notif)


@app.route('/archive')
@login_required
@roles_required('admin')
def archive():
    roleid = getRole()
    notif = getNotif()
    tickets = Tickets.query.filter_by(isdelete=1).all()
    # print(tickets)
    return render_template('archive.html', title='Archive', tickets=tickets, user=roleid, notif=notif)


@app.route('/api/')
def apipage():
    clusterForm = LanguageForm()
    getLangForm = GetLanguage()
    return render_template("apicall.html", get_language="", text_cluster="", getlangform=getLangForm,
                           clusterform=clusterForm)


bearer_token = secrets.bearer_token

value = ""
text_cluster = ""


@app.route('/api/languagecheck', methods=["GET", "POST"])
def getLanguage():
    url = "https://ug-api.acnapiv3.io/swivel/language-identification/lang-2.0?of=json&txt="
    clusterForm = LanguageForm()
    getLangForm = GetLanguage()

    text = getLangForm.text2.data
    print(text)
    url = url + text

    headers = {"Server-Token": bearer_token}

    response = requests.get(url, headers=headers)
    try:
        print(response.json())
    except:
        pass
    get_language = str(response.json()['language_list'][0])
    return render_template("apicall.html", get_language=get_language, getlangform=getLangForm,
                           clusterform=clusterForm)


@app.route('/api/textclustering', methods=["GET", "POST"])
def textCluster():
    url = "https://ug-api.acnapiv3.io/swivel/text-clustering/clustering-1.1?of=json&txt="
    getLangForm = GetLanguage()
    clusterForm = LanguageForm()
    data = {}
    if clusterForm.validate():
        text = clusterForm.text.data
        textlist = text.split('.')
        textlist = [i for i in textlist if i != ""]
        for enum, i in enumerate(textlist):
            data["text" + "{enum+1:02}"] = i
        language = '&lang=' + clusterForm.language.data
        for (key, value) in data.items():
            url += '"{}":"{}" \n'.format(key, value)
        url += language
        print(url)
        headers = {"Server-Token": bearer_token}

        response = requests.get(url, headers=headers)
        try:
            print(response.json())
        except:
            pass
        text_cluster = str(response.json()["cluster_list"])
        return render_template("apicall.html", text_cluster=text_cluster, getlangform=getLangForm,
                               clusterform=clusterForm)
    else:
        return render_template("apicall.html", text_cluster="Please Enter Text", getlangform=getLangForm,
                               clusterform=clusterForm)


@app.route('/email', methods=["GET", "POST"])
def emailsending(ticketnumber, name, email):
    user = name
    email = email
    ticketnumber = ticketnumber
    content = "Dear {user}, <br><br>Thank you for contacting accenture!<p>We have received your ticket " \
              "submission #{ticketnumber}, and our development team will be looking into the issue shortly " \
              "and will send you a follow up email once it has been reviewed.</p>You can view your " \
              "existing tickets at accenture.com <br>Thanks and have a great day.<br><br> Best regards, <br>" \
              "Accenture Service Team".format(
                  user=user, ticketnumber=ticketnumber)
    url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
    headers = {"Server-Token": bearer_token}
    body = {"subject": "Accenture: Confirmation of ticket submission",
            "sender": "noreply@accenture.com",
            "recipient": email,
            "html": content
            }
    response = requests.post(url, headers=headers, json=body)
    return redirect(url_for("index"))


def emailreply(emailstring, ticketnumber, name, email):
    user = name
    email = email
    ticketnumber = ticketnumber
    emailstring = emailstring
    email = "remnanto@hotmail.com"
    content = "Dear {user}, <br><br>{text}<br>Thanks and have a great day.<br><br> Best regards, <br>" \
              "Accenture Service Team".format(
                  user=user, text=emailstring, ticketnumber=ticketnumber)
    url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
    headers = {"Server-Token": bearer_token}
    body = {"subject": "Accenture: Confirmation of ticket submission",
            "sender": "supportteam@accenture.com",
            "recipient": email,
            "html": content
            }
    response = requests.post(url, headers=headers, json=body)
    return redirect(url_for("index"))


def recoverPasswordEmail(username, email):
    passwordlink = generatePasswordLink(username)
    emailstring = "To recover your password please visit " + passwordlink
    content = "Dear {user}, <br><br>{text}<br>Thanks and have a great day.<br><br> Best regards, <br>" \
              "Accenture Service Team".format(user=username, text=emailstring)
    url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
    headers = {"Server-Token": bearer_token}
    body = {"subject": "Accenture: Recover Password",
            "sender": "noreply@accenture.com",
            "recipient": email,
            "html": content
            }
    response = requests.post(url, headers=headers, json=body)


def recoverUsername(username, email):

    content = "Dear Member, <br><br>Your username is : {user}<br>Thanks and have a great day.<br><br> Best regards, <br>" \
              "Accenture Service Team".format(user=username)
    url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
    headers = {"Server-Token": bearer_token}
    body = {"subject": "Accenture: Recover Password",
            "sender": "supportteam@accenture.com",
            "recipient": email,
            "html": content
            }
    response = requests.post(url, headers=headers, json=body)


def generatePasswordLink(username):
    return "localhost:5000"


@app.route("/download", methods=['GET', 'POST'])
def download_blob():
    ticket = Tickets.query.get('1ea59f4c-602c-11e9-a5c7-34f39a281f4e')
    image = ticket.upload
    return send_file(BytesIO(image), attachment_filename='flask.jpg', as_attachment=True)
