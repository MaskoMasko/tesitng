from mylib import dodajNaKraj
from flask import *
from flask_socketio import *
from json import *
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def home():
  return render_template("index.html")

@app.route('/chat')
def chat():
  return render_template("chat.html")

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/signupTry', methods = ['POST'])  
def signupTry():
  if request.method == 'POST':
    name = request.form.get('name') #dela
    username = request.form.get('username') #dela
    email = request.form.get('email') #dela
    password = request.form.get('password') #dela


    val = (username,password,email,name)
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      sql = "INSERT INTO usersss (username,password,email,name) VALUES (%s, %s,%s,%s)"           
      mycursor.execute(f"SELECT email FROM usersss WHERE email='{email}'")
      myresult = mycursor.fetchall()
      duzina = len(myresult)

      if duzina == 0:     # NEMA VEC U DATABAZI
        print(myresult)
        mycursor.execute(sql, val)
        print("dodano u databasusu ")
        connection.commit()
        mycursor.close()
        connection.close()
        print("MySQL connection is closed")
        return redirect('/')

      elif duzina > 0: # VEC IMA U DATABAZI
        myresult = myresult[0][0]
        print(myresult+" already exists")
        connection.commit()
        mycursor.close()
        connection.close()
        print("MySQL connection is closed")
        return render_template("login.html",error = "A user with this email already exists, would you like to log in")


@socketio.on('message')
def handle_message(data):
  ip_address = request.remote_addr
  print('received message: ' + data)
  data = data +"///"+ str(ip_address)
  emit('announcements', data,broadcast=True) # OVAKO SALJEMO I DI SALJEMO
  dodajNaKraj("poruke.json",data)


@socketio.on('connect')
def test_connect():
  pass

@socketio.on('disconnect')
def test_disconnect():
  print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)