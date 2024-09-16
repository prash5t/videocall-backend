from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store user sessions
users = {}


@socketio.on('connect')
def handle_connect():
    email = request.args.get('email')
    if email:
        users[email] = request.sid
        join_room(email)
        print(f"User {email} connected")


@socketio.on('disconnect')
def handle_disconnect():
    for email, sid in users.items():
        if sid == request.sid:
            del users[email]
            leave_room(email)
            print(f"User {email} disconnected")
            break


@socketio.on('call_request')
def handle_call_request(data):
    caller_email = data['caller_email']
    callee_email = data['callee_email']

    if callee_email in users:
        emit('incoming_call', {
            'caller_email': caller_email,
            'call_id': str(uuid.uuid4())
        }, room=callee_email)
    else:
        emit('user_unavailable', {
             'callee_email': callee_email}, room=caller_email)


@socketio.on('call_response')
def handle_call_response(data):
    call_id = data['call_id']
    response = data['response']
    caller_email = data['caller_email']
    callee_email = data['callee_email']

    if response == 'accept':
        emit('call_accepted', {'call_id': call_id,
             'callee_email': callee_email}, room=caller_email)
    else:
        emit('call_rejected', {'call_id': call_id,
             'callee_email': callee_email}, room=caller_email)


@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    target_email = data['target_email']
    if target_email in users:
        emit('ice_candidate', data, room=target_email)


@socketio.on('offer')
def handle_offer(data):
    target_email = data['target_email']
    if target_email in users:
        emit('offer', data, room=target_email)


@socketio.on('answer')
def handle_answer(data):
    target_email = data['target_email']
    if target_email in users:
        emit('answer', data, room=target_email)


@socketio.on('end_call')
def handle_end_call(data):
    target_email = data['target_email']
    if target_email in users:
        emit('call_ended', {
             'caller_email': data['caller_email']}, room=target_email)


if __name__ == '__main__':
    socketio.run(app, debug=True)
