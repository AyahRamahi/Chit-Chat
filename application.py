import os

from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit,join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

rooms = []
chat = {}

@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html",rooms=rooms,error=False)
    else :
        roomName = request.form['roomName']
        if roomName in rooms :
            return render_template('index.html',rooms=rooms,error=True)
        else :
            rooms.append(roomName)
            return render_template('index.html',rooms=rooms,error=False)

@app.route('/<string:roomName>')
def room(roomName):
    ch = chat.get(roomName)
    return render_template('room.html',room=roomName,chat=ch)

@socketio.on('join')
def join(data):
    join_room(data['room'])

@socketio.on('send_msg')
def send_msg(data):
    room=data['room']
    msg = data['message']
    ch = chat.get(room)
    name = data['username']
    if ch is None :
        ch = []
    ch.append(msg+' by '+name)
    chat[room]=ch
    emit('get_msg',{'message':data['message'],'username':data['username'],'room':room},room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
