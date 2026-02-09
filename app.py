from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ipl_secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Shuruati data
auction_data = {
    "player_name": "MS Dhoni",
    "current_bid": 200,
    "current_team": "None",
    "status": "In Progress"
}

@app.route('/')
def index():
    return render_template('index.html', data=auction_data)

@app.route('/admin')
def admin():
    return render_template('admin.html', data=auction_data)

@socketio.on('place_bid')
def handle_bid(data):
    global auction_data
    auction_data['current_bid'] = data['bid_amount']
    auction_data['current_team'] = data['team_name']
    # Sabhi users ko live update bhejna
    emit('bid_update', auction_data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
