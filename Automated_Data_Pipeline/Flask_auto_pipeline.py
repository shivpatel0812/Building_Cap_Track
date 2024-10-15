# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
socketio = SocketIO(app, cors_allowed_origins="*") 


MONGO_URI = "your_mongo_uri"  
DB_NAME = "capacity_db"
COLLECTION_NAME = "counts"


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def background_thread():
    """Background thread to emit data to clients."""
    pipeline = [{'$match': {'operationType': 'insert'}}]
    with collection.watch(pipeline) as stream:
        for change in stream:
            full_document = change['fullDocument']
            data = {
                'location': full_document.get('location', 'Unknown'),
                'occupancy': full_document.get('occupancy', 0),
                'enter_count': full_document.get('enter_count', 0),
                'exit_count': full_document.get('exit_count', 0),
                'timestamp': full_document.get('timestamp')
            }
            socketio.emit('update_counts', data)
            print(f"Emitted data: {data}")


@socketio.on('connect')
def handle_connect():
    global thread
    if not thread.is_alive():
        print("Starting background thread")
        thread.start()

@app.route('/')
def index():
    return "Socket.IO server running."

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    socketio.run(app, debug=True)
