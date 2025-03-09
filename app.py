from flask import Flask, render_template, request, jsonify
from ai_dm import AIDungeonMaster  # Import your AI Dungeon Master

app = Flask(__name__)
ai_dm = AIDungeonMaster()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    user_input = request.json.get('user_input')
    response = ai_dm.player_action("Player", user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
