from flask import Flask
from flask_socketio import SocketIO
from database import init_db
from events import register_events
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()
register_events(socketio)

if __name__ == '__main__':
    socketio.run(app, debug=app.config['DEBUG'])
