from app import app
import requests
from flask import Flask, render_template, request
from app.forms import LanguageForm

@app.route('/')
@app.route('/index')
def index():
    return "Hello friends! :)"



bearer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlF6Y3hRVEl5UkRVeU1qYzNSakEzT"\
                + "npKQ01qVTROVVJFUlVZelF6VTRPRUV6T0RreE1UVTVPQSJ9.eyJpc3MiOiJodHRwczovL2FjbmFwaS1w"\
                + "cm9kLmF1dGgwLmNvbS8iLCJzdWIiOiJpNzlBOVJReHFlMWZQMmlPb0dlTHE0aERGYzNyaUNQckBjbGll"\
                + "bnRzIiwiYXVkIjoiaHR0cHM6Ly9wbGFjZWhvbGRlci5jb20vcGxhY2UiLCJpYXQiOjE1NDk5NTI3MDMs"\
                + "ImV4cCI6MTU1MjU0NDcwMywiYXpwIjoiaTc5QTlSUXhxZTFmUDJpT29HZUxxNGhERmMzcmlDUHIiLCJn"\
                + "dHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.P1zV9IRXUZttmdetxvhYEI9wcbr8ZsznxtRV5S9XLSRXF"\
                + "MqDOz8D5wPdkFu6mS0FCsGQ2eeMPIi1jTNDLzH6CsgJLlAH8A_47BS1DswYcn--bORVQA0as-TZqkMsq"\
                + "97X67Y0P2GX_CE_K-4jtqd_jKWD74WqPkeD4z2JFRV0DS3FQ56aKuJOPWK4WriCniRPLJYulTp8IJeQ8"\
                + "X3wzDlwbJXYjGtMYB1DKMT21lorY5bHF3Daghfqe08m5tqUAU7ErfWTx2zp6pRTzy67acJja-9O4D3DP"\
                + "CwiRkC-EOUa_gOdTzxeZ-sCugVW15e_XXqVHctADp5Zr7bjHGn-RcOVkQ"


@app.route('/api/')
def apipage():
    form = LanguageForm()
    return render_template("apicall.html", get_language="", text_cluster="", form=form)


value = ""
text_cluster = ""


@app.route('/api/languagecheck', methods=["GET", "POST"])
def getLanguage():
    url = "https://ug-api.acnapiv3.io/swivel/language-identification/lang-2.0?of=json&txt="
    text = request.form['getLanguage']
    print(text)
    url = url + text

    headers = {"Server-Token": bearer_token}

    response = requests.get(url, headers=headers)
    try:
        print(response.json())
    except:
        pass
    get_language = str(response.json()['language_list'][0])
    return render_template("apicall.html", get_language=get_language)


@app.route('/api/textclustering', methods=["GET", "POST"])
def textCluster():
    url = "https://ug-api.acnapiv3.io/swivel/text-clustering/clustering-1.1?of=json&txt="
    form = LanguageForm()
    data = {}
    if form.validate():
        text = form.text.data
        textlist = text.split('.')
        textlist = [i for i in textlist if i != ""]
        for enum, i in enumerate(textlist):
            data["text" + f'{enum+1:02}'] = i
        language = '&lang=' + form.language.data
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
        return render_template("apicall.html", text_cluster=text_cluster, form=form)
    else:
        return render_template("apicall.html", text_cluster="Please Enter Text", form=form)

