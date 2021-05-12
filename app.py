from flask import *
from flask_socketio import *

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
    print('received message: ' + data)
    return 'one'
    
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    
if __name__ == '__main__':
    socketio.run(app)