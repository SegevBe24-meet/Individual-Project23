from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

const = {
  "apiKey": "AIzaSyCrgR6v7P4jgSkAQSLlg9ox5yAqwN_fJHw",
  "authDomain": "segev-s-recpies.firebaseapp.com",
  "projectId": "segev-s-recpies",
  "storageBucket": "segev-s-recpies.appspot.com",
  "messagingSenderId": "333657138952",
  "appId": "1:333657138952:web:726d6048b3a8e74ba2eebd",
  "measurementId": "G-WCRYWQDBQ4",
  "databaseURL" :"https://segev-s-recpies-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(const)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            login_session['user'] = auth.login_user(username,password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("login.html")
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        age = request.form['age']        
        email = request.form['email']
        password = request.form['password']        
        try:
            login_session['index'] = auth.create_user(email, password)
            uid = login_session['index']['localId']
            user_info = {"fname":fname,"lname":lname,"username":username,"age":age,"email":email,"password":password}
            info = db.child("index").child(uid).set(user_info)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)