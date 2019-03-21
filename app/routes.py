from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.auth.forms import LoginForm, RegistrationForm
from app.forms import LanguageForm, LoginForm, GetLanguage
from app.ticket.forms import TicketForm
from app.models import User
import requests


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    form = TicketForm()
    if form.validate_on_submit():
        #create db for ticket submission
        #commit to db
        flash('Your ticket has been submitted.')
        return redirect(url_for('ticket'))
    return render_template('ticket.html', title = 'Ticket', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
  
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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


bearer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlF6Y3hRVEl5UkRVeU1qYzNSakEzTnpKQ01qVTROVVJFUlVZelF6VT" \
               "RPRUV6T0RreE1UVTVPQSJ9.eyJpc3MiOiJodHRwczovL2FjbmFwaS1wcm9kLmF1dGgwLmNvbS8iLCJzdWIiOiJpNzlBOVJReHF" \
               "lMWZQMmlPb0dlTHE0aERGYzNyaUNQckBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9wbGFjZWhvbGRlci5jb20vcGxhY2UiLCJpY" \
               "XQiOjE1NDk5NTI3MDMsImV4cCI6MTU1MjU0NDcwMywiYXpwIjoiaTc5QTlSUXhxZTFmUDJpT29HZUxxNGhERmMzcmlDUHIiLCJ" \
               "ndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.P1zV9IRXUZttmdetxvhYEI9wcbr8ZsznxtRV5S9XLSRXFMqDOz8D5wPdkFu6mS" \
               "0FCsGQ2eeMPIi1jTNDLzH6CsgJLlAH8A_47BS1DswYcn--bORVQA0as-TZqkMsq97X67Y0P2GX_CE_K-4jtqd_jKWD74WqPkeD" \
               "4z2JFRV0DS3FQ56aKuJOPWK4WriCniRPLJYulTp8IJeQ8X3wzDlwbJXYjGtMYB1DKMT21lorY5bHF3Daghfqe08m5tqUAU7Erf" \
               "WTx2zp6pRTzy67acJja-9O4D3DPCwiRkC-EOUa_gOdTzxeZ-sCugVW15e_XXqVHctADp5Zr7bjHGn-RcOVkQ"


@app.route('/api/')
def apipage():
    clusterForm = LanguageForm()
    getLangForm = GetLanguage()
    return render_template("apicall.html", get_language="", text_cluster="", getlangform=getLangForm,
                           clusterform=clusterForm)


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
            data["text" + f'{enum+1:02}'] = i
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

