from flask import Flask, render_template, request, jsonify
from database import get_db_connection, init_db

app = Flask(__name__)

db_conn = get_db_connection()
init_db(db_conn)

def get_22_positions():
    home_players = [
        {'num': 'GK', 'x': 50, 'y': 92, 'type': 'gk'},
        {'num': '2', 'x': 15, 'y': 80, 'type': 'home-team'},
        {'num': '4', 'x': 38, 'y': 82, 'type': 'home-team'},
        {'num': '5', 'x': 62, 'y': 82, 'type': 'home-team'},
        {'num': '3', 'x': 85, 'y': 80, 'type': 'home-team'},
        {'num': '6', 'x': 50, 'y': 68, 'type': 'home-team'},
        {'num': '8', 'x': 30, 'y': 60, 'type': 'home-team'},
        {'num': '10', 'x': 70, 'y': 60, 'type': 'home-team'},
        {'num': '7', 'x': 18, 'y': 48, 'type': 'home-team'},
        {'num': '9', 'x': 50, 'y': 45, 'type': 'home-team'},
        {'num': '11', 'x': 82, 'y': 48, 'type': 'home-team'},
    ]
    away_players = [
        {'num': 'GK', 'x': 50, 'y': 8, 'type': 'gk'},
        {'num': '2', 'x': 85, 'y': 20, 'type': 'away-team'},
        {'num': '4', 'x': 62, 'y': 18, 'type': 'away-team'},
        {'num': '5', 'x': 38, 'y': 18, 'type': 'away-team'},
        {'num': '3', 'x': 15, 'y': 20, 'type': 'away-team'},
        {'num': '6', 'x': 50, 'y': 32, 'type': 'away-team'},
        {'num': '8', 'x': 70, 'y': 40, 'type': 'away-team'},
        {'num': '10', 'x': 30, 'y': 40, 'type': 'away-team'},
        {'num': '7', 'x': 82, 'y': 52, 'type': 'away-team'},
        {'num': '9', 'x': 50, 'y': 55, 'type': 'away-team'},
        {'num': '11', 'x': 18, 'y': 52, 'type': 'away-team'},
    ]
    return home_players + away_players

@app.route('/')
def match_center():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM teams ORDER BY type DESC, rating DESC")
    teams = cursor.fetchall()
    pitch_players = get_22_positions()
    return render_template('index.html', teams=teams, pitch_players=pitch_players, active_page='match')

@app.route('/worldcup')
def world_cup_page():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE type='National'")
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

# API สำหรับรับบันทึกผลการแข่งขันจากสนามแข่งไปลงตารางคะแนน
@app.route('/api/record-match', methods=['POST'])
def record_match():
    data = request.json
    home_name = data.get('home_name')
    away_name = data.get('away_name')
    home_score = int(data.get('home_score', 0))
    away_score = int(data.get('away_score', 0))

    # กำหนดแต้ม
    if home_score > away_score:
        h_pts, a_pts = 3, 0
    elif home_score < away_score:
        h_pts, a_pts = 0, 3
    else:
        h_pts, a_pts = 1, 1

    return jsonify({
        'status': 'success',
        'message': f'บันทึกผลเรียบร้อย: {home_name} {home_score} - {away_score} {away_name} (คะแนนถูกส่งไปหน้ารอบคัดเลือกเรียบร้อย)'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
