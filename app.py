from mylib import dodajNaKraj
from flask import *
from flask_socketio import *
from json import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def home():
  return render_template("index.html")

@app.route('/chat')
def chat():
  return render_template("chat.html")

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