from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Auction State
auction_state = {
    "player_name": "Virat Kohli",
    "current_bid": 200,
    "current_team": "None",
    "history": [] # Sabhi actions yahan save honge
}

@app.route('/')
def index():
    return render_template('index.html', data=auction_state)

@app.route('/admin')
def admin():
    return render_template('admin.html', data=auction_state)

@socketio.on('action')
def handle_action(data):
    global auction_state
    action_type = data['type'] # 'bid' ya 'pass'
    team = data['team_name']
    
    if action_type == 'bid':
        amount = data['amount']
        auction_state['current_bid'] = amount
        auction_state['current_team'] = team
        log_entry = f"🏏 {team} ne {amount} Lakh ki Bid lagai!"
    else:
        log_entry = f"❌ {team} ne Pass kar diya."

    # History mein top par naya action add karna
    auction_state['history'].insert(0, log_entry)
    
    # Sirf last 10 actions dikhane ke liye
    auction_state['history'] = auction_state['history'][:10]
    
    emit('update_all', auction_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
