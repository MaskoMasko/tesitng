from mylib import dodajNaKraj
from flask import *
from flask_socketio import *
from json import *
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

onlin = []
@app.route('/')
def home():
  logStatus = request.cookies.get('logStat')
  username = request.cookies.get('User')
  return render_template("main.html",logStatus=logStatus,username=username)

@app.route('/mainTu')
def mainTu():
  return render_template("main2.html")


@app.route('/chat')
def chat():
  logStatus = request.cookies.get('logStat')
  username = request.cookies.get('User')
  print(username)
  if logStatus != "Logged In":
    return redirect("/login")
  else:
    return render_template("chat.html",logStatus=logStatus,username=username)

@app.route('/signup')
def signup():
  return render_template("signup.html")


@app.route('/signout')
def signout():
  resp = make_response(redirect('/login'))
  resp.set_cookie('logStat', 'Signed Out')
  resp.set_cookie('User', "None")
  return resp      

@app.route('/login')
def login():
  logStatus = request.cookies.get('logStat')
  if logStatus == "Logged In":
    return redirect("/chat")
  else:
    return render_template("login.html")

@app.route('/profile')
def profile():
  logStatus = request.cookies.get('logStat')
  if logStatus == "Logged In":
    username = request.cookies.get('User')
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      mycursor.execute(f"SELECT email FROM userssss WHERE username='{username}'")
      myresult = mycursor.fetchall()
      return render_template("profile.html",username=username,email=myresult)
  else:
    return render_template("login.html")

@app.route('/signupTry', methods = ['POST'])  
def signupTry():
  if request.method == 'POST':
    name = request.form.get('name') #dela
    username = request.form.get('username') #dela
    email = request.form.get('email') #dela
    password = request.form.get('password') #dela
    surname = request.form.get('surname') #dela

    val = (username,password,email,name,surname)
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      sql = "INSERT INTO userssss (username,password,email,name,surname) VALUES (%s, %s,%s,%s,%s)"           
      mycursor.execute(f"SELECT email FROM userssss WHERE email='{email}'")
      myresult = mycursor.fetchall()
      duzina = len(myresult)
      mycursor.execute(f"SELECT email FROM userssss WHERE email='{email}'")
      myresult2 = mycursor.fetchall()
      duzina2 = len(myresult2)
      if duzina == 0:     # NEMA VEC U DATABAZI
        mycursor.execute(f"SELECT username FROM userssss WHERE username='{username}'")
        myresult2 = mycursor.fetchall()
        duzina2 = len(myresult2)
        if duzina2 == 0:
          print(myresult)
          mycursor.execute(sql, val)
          print("dodano u databasusu ")
          connection.commit()
          mycursor.close()
          connection.close()
          print("MySQL connection is closed")
          return redirect('/')
        elif duzina2 > 0:
          heresult = myresult2[0][0]
          print(heresult+" already exists")
          connection.commit()
          mycursor.close()
          connection.close()
          print("MySQL connection is closed")
          return render_template("login.html",error = "A user with this username already exists, would you like to log in")

      elif duzina > 0: # VEC IMA U DATABAZI
        myresult = myresult[0][0]
        print(myresult+" already exists")
        connection.commit()
        mycursor.close()
        connection.close()
        print("MySQL connection is closed")
        return render_template("login.html",error = "A user with this email already exists, would you like to log in")

@app.route('/loginTry', methods = ['POST'])  
def loginTry():
  if request.method == 'POST':
    username = request.form.get('name') #dela
    password = request.form.get('password') #dela

    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      mycursor.execute(f"SELECT password FROM userssss WHERE username='{username}'")
      myresult = mycursor.fetchall()
      duzina = len(myresult)
      if duzina == 0:
        print("That username does not exist")
        return render_template("signup.html",error = "A user with that name does not exist, would you like to sign up")
      elif duzina > 0:
        myresult = myresult[0][0]
        if password == myresult:
          resp = make_response(redirect('/'))
          resp.set_cookie('logStat', 'Logged In')
          print(username)
          resp.set_cookie('User', username)
          return resp      
        else:
          flash("Wrong password")
          return redirect('/login')
    print(username, password,myresult)
    return redirect('/')




@socketio.on('message')
def handle_message(data):
  logStatus = request.cookies.get('logStat')
  username = request.cookies.get('User')
  print('received message: ' + data)
  data = data +"///"+ str(username)
  emit('announcements', data,broadcast=True) # OVAKO SALJEMO I DI SALJEMO
  dodajNaKraj("poruke.json",data)

@socketio.on('online')
def online():
  onlin.append(request.cookies.get('User'))

@socketio.on('connect')
def test_connect():
  pass

@socketio.on('disconnect')
def test_disconnect():
  onlin.remove(request.cookies.get('User'))



if __name__ == '__main__':
    
    socketio.run(app)