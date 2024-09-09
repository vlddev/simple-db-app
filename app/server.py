import os
import sys, traceback
from datetime import datetime
from flask import Flask, request, session, render_template, flash, redirect, url_for, jsonify
import requests
import dto
from types import SimpleNamespace
import utils

app = Flask(__name__)
app.secret_key = "==dfgdijertmnwesodi=="

user = os.getenv('DB_USER', 'kic')
pwd = os.getenv('DB_PASSWORD', 'kic#pwd')
dbName = os.getenv('DB_NAME', 'kic')
dbHost = os.getenv('DB_HOST', 'localhost')
dbcon = utils.create_connection(dbName, user, pwd, dbHost, "5432")

def isLoggedIn() -> bool:
    return 'Username' in session;

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        ret_msg = []
        btitle = request.form.get('btitle')
        query_content = f"Title: {btitle}"
        err_msg, resultList = utils.searchBookByTitle(dbcon, btitle)
        if err_msg is not None:
            ret_msg.append(dto.MessageDto(mtype='E', message=err_msg))
        return render_template('index.html',
                            ret_msg=ret_msg,
                            btitle=btitle,
                            query_content=query_content,
                            resultList=resultList,
                            loggedIn=isLoggedIn())

@app.route('/user', methods=['GET', 'POST'])
def userLogin():
    ret_msg = []
    contractList = []
    username = None
    userId = None

    if request.method == 'POST':
        if 'Username' not in session: # login
            username = request.form.get('username')
            userkey = request.form.get('userkey')
            try:
                r = requests.get(utils.WORK_MATCHER_AUTH.format(user=username))
                # process result, feel ret_msg
                results = r.json()
                if results is not None:
                    print(f"results = {results}")
                    if results['userId'] is not None:
                        session['Username'] = username
                        session['userId'] = results['userId']
                        userId = session['userId']
                        print(f"Logged in as {username} (uid = {results['userId']})")
                    else:
                        ret_msg.append(dto.MessageDto(mtype='W', message=f'Login impossible for user: {username}'))
                else:
                    ret_msg.append(dto.MessageDto(mtype='W', message=f'Unknown user: {username}'))
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                ret_msg.append(dto.MessageDto(mtype='E', message=f'Error querying work matcher: {str(exc_value)}'))
        else: 
            # logout
            logout = request.form.get('logout')
            if logout is not None and logout == 'true':
                uname = session['Username']
                session.pop('Username', None)
                session.pop('userId', None)
                print(f"{uname} logged out")
    else: # GET
        if 'Username' in session:
            username = session['Username']
            userId = session['userId']

    if userId is not None:
        try:
            contractList = utils.extendContractsWithRecording(utils.getContracts(userId))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            ret_msg.append(dto.MessageDto(mtype='E', message=f'Error querying work matcher: {str(exc_value)}'))

    return render_template('user.html', user=username, contractList=contractList, ret_msg=ret_msg)


@app.route('/addrecording', methods=['GET', 'POST'])
def addRecording():
    ret_msg = []
    if request.method == 'POST':
        stitle = request.form.get('stitle')
        sartist = request.form.get('sartist')
        try:
            r = requests.post(utils.WORK_MATCHER_ADD_RECORDING, data = {'artist':sartist, 'title':stitle})
            # process result, feel ret_msg
            json_responce = r.json()
            ret_msg = json_responce['messages']
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            ret_msg.append(dto.MessageDto(mtype='E', message=f'Error querying work matcher: {str(exc_value)}'))
        return render_template('addrecording.html', ret_msg=ret_msg)
    else:
        return render_template('addrecording.html')

@app.route('/addartist', methods=['GET', 'POST'])
def addArtist():
    ret_msg = []
    if request.method == 'POST':
        sartist = request.form.get('sartist')
        try:
            r = requests.post(utils.WORK_MATCHER_ADD_ARTIST, data = {'name':sartist})
            # process result, feel err_msg, ret_msg
            json_responce = r.json()
            ret_msg = json_responce['messages']
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            ret_msg.append(dto.MessageDto(mtype='E', message=f'Error querying work matcher: {str(exc_value)}'))
        return render_template('addrecording.html', ret_msg=ret_msg)
    else:
        return render_template('addrecording.html')

if __name__=="__main__":
    app.run("0.0.0.0") #, 5050)
