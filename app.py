from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

auction_data = {
    "player_name": "New Player",
    "base_price": 100,
    "current_bid": 100,
    "highest_bidder": "None",
    "league_name": "Uncha Premiere League"
}

@app.route('/')
def home():
    return render_template('index.html', data=auction_data)

@app.route('/admin')
def admin():
    return render_template('admin.html', data=auction_data)

@app.route('/update_player', methods=['POST'])
def update_player():
    auction_data['player_name'] = request.form.get('player_name')
    auction_data['base_price'] = int(request.form.get('base_price'))
    auction_data['current_bid'] = int(request.form.get('base_price'))
    auction_data['highest_bidder'] = "None"
    return jsonify({"success": True})

@app.route('/place_bid', methods=['POST'])
def place_bid():
    new_bid = int(request.form.get('bid_amount'))
    bidder_name = request.form.get('bidder_name')
    if new_bid > auction_data['current_bid']:
        auction_data['current_bid'] = new_bid
        auction_data['highest_bidder'] = bidder_name
        return jsonify({"success": True, "new_bid": new_bid, "bidder": bidder_name})
    return jsonify({"success": False, "message": "Boli kam hai!"})

if __name__ == '__main__':
    app.run(debug=True)
