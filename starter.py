from amanigo import app
from flask_socketio import SocketIO

if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    socketio = SocketIO(app)
    socketio.run(app, debug=True, port=6500, use_reloader=True)
