from flask import Flask, render_template, request, jsonify
from database import get_db_connection, init_db

app = Flask(__name__)

db_conn = get_db_connection()
init_db(db_conn)

def get_22_positions():
    home_players = [
        {'num': '1', 'pos': 'GK', 'x': 50, 'y': 92, 'type': 'gk'},
        {'num': '2', 'pos': 'RB', 'x': 15, 'y': 80, 'type': 'home-team'},
        {'num': '4', 'pos': 'CB', 'x': 38, 'y': 82, 'type': 'home-team'},
        {'num': '5', 'pos': 'CB', 'x': 62, 'y': 82, 'type': 'home-team'},
        {'num': '3', 'pos': 'LB', 'x': 85, 'y': 80, 'type': 'home-team'},
        {'num': '6', 'pos': 'CDM', 'x': 50, 'y': 68, 'type': 'home-team'},
        {'num': '8', 'pos': 'CM', 'x': 30, 'y': 60, 'type': 'home-team'},
        {'num': '10', 'pos': 'CAM', 'x': 70, 'y': 60, 'type': 'home-team'},
        {'num': '7', 'pos': 'RW', 'x': 18, 'y': 48, 'type': 'home-team'},
        {'num': '9', 'pos': 'ST', 'x': 50, 'y': 45, 'type': 'home-team'},
        {'num': '11', 'pos': 'LW', 'x': 82, 'y': 48, 'type': 'home-team'},
    ]
    away_players = [
        {'num': '1', 'pos': 'GK', 'x': 50, 'y': 8, 'type': 'gk'},
        {'num': '2', 'pos': 'RB', 'x': 85, 'y': 20, 'type': 'away-team'},
        {'num': '4', 'pos': 'CB', 'x': 62, 'y': 18, 'type': 'away-team'},
        {'num': '5', 'pos': 'CB', 'x': 38, 'y': 18, 'type': 'away-team'},
        {'num': '3', 'pos': 'LB', 'x': 15, 'y': 20, 'type': 'away-team'},
        {'num': '6', 'pos': 'CDM', 'x': 50, 'y': 32, 'type': 'away-team'},
        {'num': '8', 'pos': 'CM', 'x': 70, 'y': 40, 'type': 'away-team'},
        {'num': '10', 'pos': 'CAM', 'x': 30, 'y': 40, 'type': 'away-team'},
        {'num': '7', 'pos': 'RW', 'x': 82, 'y': 52, 'type': 'away-team'},
        {'num': '9', 'pos': 'ST', 'x': 50, 'y': 55, 'type': 'away-team'},
        {'num': '11', 'pos': 'LW', 'x': 18, 'y': 52, 'type': 'away-team'},
    ]
    return home_players + away_players

@app.route('/')
def match_center():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM teams ORDER BY name ASC")
    teams = cursor.fetchall()
    pitch_players = get_22_positions()
    return render_template('index.html', teams=teams, pitch_players=pitch_players, active_page='match')

@app.route('/api/team-roster/<int:team_id>')
def get_team_roster(team_id):
    cursor = db_conn.cursor()
    cursor.execute("SELECT shirt_number, name, position, role_type FROM players WHERE team_id=? ORDER BY shirt_number ASC", (team_id,))
    roster = cursor.fetchall()
    return jsonify([dict(r) for r in roster])

@app.route('/worldcup')
def world_cup_page():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE type='National' ORDER BY name ASC")
    teams = cursor.fetchall()
    return render_template('worldcup.html', teams=teams, active_page='worldcup')

@app.route('/bracket')
def bracket_page():
    return render_template('bracket.html', active_page='bracket')

@app.route('/history')
def history_page():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM trophies_history ORDER BY year DESC, id DESC")
    trophies = cursor.fetchall()
    return render_template('history.html', trophies=trophies, active_page='history')

@app.route('/api/record-match', methods=['POST'])
def record_match():
    data = request.json
    return jsonify({
        'status': 'success',
        'message': f"บันทึกผลการแข่งขันเรียบร้อยแล้ว!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
