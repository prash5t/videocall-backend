from flask import Flask, render_template
from flask_socketio import SocketIO
from database import init_db, get_call_logs
from events import register_events
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()
register_events(socketio)


@app.route('/admin-dashboard')
def admin_dashboard():
    logs = get_call_logs()
    return render_template('admin_dashboard.html', logs=logs)


if __name__ == '__main__':
    socketio.run(app, debug=app.config['DEBUG'],
                 host=app.config['HOST'], port=app.config['PORT'])
