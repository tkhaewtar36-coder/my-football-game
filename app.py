from flask import Flask, render_template_string, request, jsonify
import sqlite3
import random
import time

app = Flask(__name__)

# --- DATABASE SETUP ---
DB_NAME = "football_sim.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Teams Table (National & Club)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- 'National' or 'Club'
            country TEXT,
            confederation TEXT, -- 'AFC', 'UEFA', 'CONMEBOL', etc.
            rating INTEGER DEFAULT 70,
            fifa_ranking INTEGER DEFAULT 100,
            trophies TEXT DEFAULT ''
        )
    ''')

    # 2. Managers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tactical_style TEXT DEFAULT 'Balanced',
            in_game_reading INTEGER DEFAULT 75, -- ความสามารถในการอ่านเกม
            adaptability INTEGER DEFAULT 70,     -- การปรับแผนหน้างาน
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    ''')

    # 3. Players Table & History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            age INTEGER,
            pace INTEGER DEFAULT 70,
            finishing INTEGER DEFAULT 70,
            vision INTEGER DEFAULT 70,
            stamina INTEGER DEFAULT 100,
            team_id INTEGER,
            national_team_id INTEGER,
            career_goals INTEGER DEFAULT 0,
            career_assists INTEGER DEFAULT 0,
            career_apps INTEGER DEFAULT 0,
            history_log TEXT DEFAULT '', -- บันทึกประวัติสโมสร/ทีมชาติ
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    ''')

    # 4. Tournaments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, -- 'World Cup Qualifiers', 'UEFA Euro', 'Thai League', etc.
            category TEXT NOT NULL, -- 'National' or 'Club'
            region TEXT NOT NULL -- 'Global', 'Asia', 'Europe', 'Thailand', 'Japan', 'England', 'Spain'
        )
    ''')

    conn.commit()
    conn.close()

# Initialize DB structure on launch
init_db()

# --- SIMULATION ENGINE CONFIG (25 MINUTES MATCH CLOCK) ---
MATCH_DURATION_MINUTES = 25  # Real-time length: 25 minutes
TOTAL_GAME_MINUTES = 90      # Standard football match duration

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GBA Full-Scale Football Management Simulator</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; margin: 0; padding: 20px; }
        h1 { margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px #000; }
        .subtitle { color: #888; font-size: 14px; margin-bottom: 20px; }
        
        .dashboard { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }
        .card { background: #1e1e1e; padding: 15px 25px; border-radius: 8px; border: 1px solid #333; min-width: 200px; text-align: left; }
        .card h3 { margin-top: 0; color: #ff4500; font-size: 16px; border-bottom: 1px solid #333; padding-bottom: 5px; }

        /* Tactical Pitch Design */
        .pitch { 
            width: 340px; 
            height: 480px; 
            background: repeating-linear-gradient(0deg, #2e8b57, #2e8b57 40px, #27794c 40px, #27794c 80px); 
            margin: 0 auto; 
            border: 4px solid #fff; 
            position: relative; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
            border-radius: 4px;
            overflow: hidden;
        }

        /* Pitch Markings */
        .halfway-line { position: absolute; top: 50%; width: 100%; height: 2px; background: rgba(255,255,255,0.8); }
        .center-circle { position: absolute; top: 50%; left: 50%; width: 70px; height: 70px; border: 2px solid rgba(255,255,255,0.8); border-radius: 50%; transform: translate(-50%, -50%); }
        .center-dot { position: absolute; top: 50%; left: 50%; width: 6px; height: 6px; background: white; border-radius: 50%; transform: translate(-50%, -50%); }
        .penalty-area-top { position: absolute; top: 0; left: 50%; width: 150px; height: 65px; border: 2px solid rgba(255,255,255,0.8); border-top: none; transform: translateX(-50%); }
        .penalty-area-bottom { position: absolute; bottom: 0; left: 50%; width: 150px; height: 65px; border: 2px solid rgba(255,255,255,0.8); border-bottom: none; transform: translateX(-50%); }

        /* Player Pins & Ball */
        .player {
            position: absolute;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            font-weight: bold;
            color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
            transform: translate(-50%, -50%);
            border: 2px solid #fff;
            transition: all 1.5s ease-in-out;
        }
        .home-team { background-color: #d32f2f; }
        .away-team { background-color: #1976d2; }
        .gk { background-color: #fbc02d; color: black; }
        
        .ball {
            position: absolute;
            width: 10px;
            height: 10px;
            background-color: #fff;
            border-radius: 50%;
            box-shadow: 0 0 6px #fff;
            transform: translate(-50%, -50%);
            transition: all 0.8s ease-out;
            z-index: 10;
        }

        .match-clock { font-size: 24px; font-weight: bold; color: #ff4500; margin-bottom: 10px; }
        .btn { background: #ff4500; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; }
        .btn:hover { background: #ff5722; }
    </style>
</head>
<body>
    <h1>GBA Football Simulator</h1>
    <div class="subtitle">Full-Scale Management & Tournament Engine (25-Min Real-Time Match)</div>

    <div class="dashboard">
        <div class="card">
            <h3>🏆 Tournaments Included</h3>
            <p>• FIFA World Cup & Qualifiers</p>
            <p>• UEFA Euro & AFC Asian Cup</p>
            <p>• Leagues: Thai, J-League, EPL, La Liga</p>
        </div>
        <div class="card">
            <h3>👔 Manager AI & Stats</h3>
            <p>• In-Game Reading & Tactical Shifts</p>
            <p>• Player Stamina & Career Logs</p>
            <p>• Global FIFA & Club Rankings</p>
        </div>
    </div>

    <div class="match-clock" id="clock">00:00 (In-Game: 0')</div>

    <div class="pitch">
        <div class="halfway-line"></div>
        <div class="center-circle"></div>
        <div class="center-dot"></div>
        <div class="penalty-area-top"></div>
        <div class="penalty-area-bottom"></div>

        <!-- Ball -->
        <div class="ball" id="ball" style="left: 50%; top: 50%;"></div>

        <!-- 22 Players Position -->
        {% for p in players %}
            <div class="player {{ p.type }}" id="p-{{ loop.index }}" style="left: {{ p.x }}%; top: {{ p.y }}%;">{{ p.num }}</div>
        {% endfor %}
    </div>

    <br>
    <button class="btn" onclick="startMatch()">เริ่มแข่งขัน 25 นาที (Real-Time)</button>

    <script>
        let matchInterval = null;
        let realSeconds = 0;
        const TOTAL_REAL_SECONDS = 25 * 60; // 25 minutes = 1500 seconds

        function startMatch() {
            if (matchInterval) clearInterval(matchInterval);
            realSeconds = 0;

            matchInterval = setInterval(() => {
                realSeconds++;
                let min = Math.floor(realSeconds / 60);
                let sec = realSeconds % 60;
                
                // Map 25 real minutes to 90 game minutes
                let gameMinute = Math.floor((realSeconds / TOTAL_REAL_SECONDS) * 90);

                document.getElementById('clock').innerText = 
                    `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')} (In-Game: ${gameMinute}')`;

                // Ball & Player Movement
                moveBallAndPlayers();

                if (realSeconds >= TOTAL_REAL_SECONDS) {
                    clearInterval(matchInterval);
                    alert("จบการแข่งขัน 90 นาที (เวลาจริง 25 นาที)!");
                }
            }, 1000);
        }

        function moveBallAndPlayers() {
            // Ball Random Pass
            let ball = document.getElementById('ball');
            let ballX = Math.min(Math.max(Math.random() * 80 + 10, 10), 90);
            let ballY = Math.min(Math.max(Math.random() * 80 + 10, 10), 90);
            ball.style.left = ballX + '%';
            ball.style.top = ballY + '%';

            // Players Movement Towards Ball Area
            const players = document.querySelectorAll('.player');
            players.forEach(p => {
                if (p.innerText === 'GK') return;
                let currentX = parseFloat(p.style.left);
                let currentY = parseFloat(p.style.top);
                let moveX = (Math.random() * 8 - 4);
                let moveY = (Math.random() * 8 - 4);
                p.style.left = Math.min(Math.max(currentX + moveX, 8), 92) + '%';
                p.style.top = Math.min(Math.max(currentY + moveY, 8), 92) + '%';
            });
        }
    </script>
</body>
</html>
"""

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

@app.route('/', methods=['GET'])
def home():
    players = get_22_positions()
    return render_template_string(HTML_TEMPLATE, players=players)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
