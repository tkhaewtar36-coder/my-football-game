from flask import Flask, render_template_string, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# --- DATABASE SETUP & SEEDING ---
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            country TEXT,
            confederation TEXT,
            rating INTEGER DEFAULT 70,
            fifa_ranking INTEGER DEFAULT 100,
            league TEXT DEFAULT '',
            points INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tactical_style TEXT DEFAULT 'Balanced',
            in_game_reading INTEGER DEFAULT 75,
            adaptability INTEGER DEFAULT 70,
            team_id INTEGER
        )
    ''')

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
            career_goals INTEGER DEFAULT 0,
            career_apps INTEGER DEFAULT 0
        )
    ''')

    # Seed Teams
    national_teams = [
        ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'World Cup Qualifiers', 0),
        ('France', 'National', 'France', 'UEFA', 91, 2, 'UEFA Euro', 0),
        ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'UEFA Euro', 0),
        ('England', 'National', 'England', 'UEFA', 89, 4, 'UEFA Euro', 0),
        ('Brazil', 'National', 'Brazil', 'CONMEBOL', 90, 5, 'World Cup Qualifiers', 0),
        ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'AFC Asian Cup', 0),
        ('South Korea', 'National', 'South Korea', 'AFC', 83, 22, 'AFC Asian Cup', 0),
        ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'AFC Asian Cup', 0)
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league, points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', national_teams)

    club_teams = [
        ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga', 0),
        ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League', 0),
        ('Arsenal', 'Club', 'England', 'UEFA', 89, 0, 'Premier League', 0),
        ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1', 0),
        ('BG Pathum United', 'Club', 'Thailand', 'AFC', 73, 0, 'Thai League 1', 0)
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league, points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', club_teams)

    # Seed Players
    players = [
        ('Chanathip Songkrasin', 'CAM', 31, 78, 72, 86, 80, 8, 12, 65),
        ('Supachai Chaided', 'ST', 27, 75, 78, 68, 82, 8, 15, 42),
        ('Kaoru Mitoma', 'LW', 29, 90, 79, 82, 85, 6, 8, 34),
        ('Erling Haaland', 'ST', 26, 89, 94, 65, 88, 10, 38, 45),
        ('Jude Bellingham', 'CAM', 23, 82, 86, 89, 92, 9, 22, 50)
    ]
    cursor.executemany('''
        INSERT INTO players (name, position, age, pace, finishing, vision, stamina, team_id, career_goals, career_apps)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', players)

    conn.commit()
    return conn

db_conn = init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GBA Football Simulator - Step 3 Full Match Engine</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; margin: 0; padding: 20px; }
        h1 { margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px #000; }
        .subtitle { color: #888; font-size: 14px; margin-bottom: 20px; }
        
        .setup-box { background: #1e1e1e; padding: 15px 25px; border-radius: 8px; border: 1px solid #333; display: inline-block; margin-bottom: 20px; }
        select { padding: 8px 12px; background: #2b2b2b; color: white; border: 1px solid #444; border-radius: 4px; font-size: 14px; margin: 0 10px; }
        
        .match-score { font-size: 28px; font-weight: bold; color: #ff4500; margin-bottom: 5px; }
        .match-clock { font-size: 18px; color: #aaa; margin-bottom: 15px; }

        .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; }
        .box { background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; width: 350px; text-align: left; }
        .box h3 { margin-top: 0; color: #ff4500; border-bottom: 1px solid #444; padding-bottom: 8px; font-size: 16px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #2a2a2a; }
        th { color: #ff4500; }

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

        .halfway-line { position: absolute; top: 50%; width: 100%; height: 2px; background: rgba(255,255,255,0.8); }
        .center-circle { position: absolute; top: 50%; left: 50%; width: 70px; height: 70px; border: 2px solid rgba(255,255,255,0.8); border-radius: 50%; transform: translate(-50%, -50%); }
        .penalty-area-top { position: absolute; top: 0; left: 50%; width: 150px; height: 65px; border: 2px solid rgba(255,255,255,0.8); border-top: none; transform: translateX(-50%); }
        .penalty-area-bottom { position: absolute; bottom: 0; left: 50%; width: 150px; height: 65px; border: 2px solid rgba(255,255,255,0.8); border-bottom: none; transform: translateX(-50%); }

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

        .btn { background: #ff4500; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; }
        .btn:hover { background: #ff5722; }
        
        .event-log { height: 180px; overflow-y: auto; background: #141414; padding: 10px; border-radius: 4px; border: 1px solid #333; font-family: monospace; font-size: 12px; color: #00ffcc; text-align: left; }
    </style>
</head>
<body>
    <h1>Step 3: 25-Minute Match Engine</h1>
    <div class="subtitle">Real-Time Simulation, Player Rating Factor & Ranking Updates</div>

    <div class="setup-box">
        <label><b>ทีมเหย้า (Home):</b></label>
        <select id="homeTeam">
            {% for t in teams %}
            <option value="{{ t[0] }}">{{ t[1] }} (Rating: {{ t[5] }})</option>
            {% endfor %}
        </select>

        <label><b>ทีมเยือน (Away):</b></label>
        <select id="awayTeam">
            {% for t in teams %}
            <option value="{{ t[0] }}" {% if loop.index == 2 %}selected{% endif %}>{{ t[1] }} (Rating: {{ t[5] }})</option>
            {% endfor %}
        </select>

        <button class="btn" onclick="start25MinMatch()">เริ่มการแข่งขัน 25 นาที</button>
    </div>

    <div class="match-score" id="scoreBoard">Home 0 - 0 Away</div>
    <div class="match-clock" id="clockBoard">00:00 (In-Game: 0')</div>

    <div class="container">
        <!-- Tactical Pitch -->
        <div class="pitch">
            <div class="halfway-line"></div>
            <div class="center-circle"></div>
            <div class="penalty-area-top"></div>
            <div class="penalty-area-bottom"></div>
            <div class="ball" id="ball" style="left: 50%; top: 50%;"></div>

            {% for p in pitch_players %}
                <div class="player {{ p.type }}" style="left: {{ p.x }}%; top: {{ p.y }}%;">{{ p.num }}</div>
            {% endfor %}
        </div>

        <!-- Real-Time Event Log -->
        <div class="box">
            <h3>Match Events & Commentary</h3>
            <div class="event-log" id="eventLog">
                > เลือกทีมแล้วกดเริ่มแข่งเพื่อจำลองเกม 25 นาที...
            </div>
        </div>
    </div>

    <script>
        let matchInterval = null;
        let realSeconds = 0;
        let homeGoals = 0;
        let awayGoals = 0;
        const TOTAL_REAL_SECONDS = 25 * 60; // 25 Minutes = 1500 Secs

        function start25MinMatch() {
            if (matchInterval) clearInterval(matchInterval);
            realSeconds = 0;
            homeGoals = 0;
            awayGoals = 0;

            const homeName = document.getElementById('homeTeam').options[document.getElementById('homeTeam').selectedIndex].text.split(' (')[0];
            const awayName = document.getElementById('awayTeam').options[document.getElementById('awayTeam').selectedIndex].text.split(' (')[0];

            document.getElementById('scoreBoard').innerText = `${homeName} 0 - 0 ${awayName}`;
            document.getElementById('eventLog').innerHTML = `> เริ่มการแข่งขันระหว่าง ${homeName} พบ ${awayName}<br>`;

            matchInterval = setInterval(() => {
                realSeconds++;
                let min = Math.floor(realSeconds / 60);
                let sec = realSeconds % 60;
                let gameMinute = Math.floor((realSeconds / TOTAL_REAL_SECONDS) * 90);

                document.getElementById('clockBoard').innerText = 
                    `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')} (In-Game: ${gameMinute}')`;

                moveBallAndPlayers();

                // Random Goal Event Chance based on time
                if (Math.random() < 0.003) { // Adjusted for 25-minute timeline
                    if (Math.random() > 0.5) {
                        homeGoals++;
                        logEvent(`[${gameMinute}'] GOAL! ${homeName} ยิงประตูขึ้นนำ/ขยับสกอร์!`);
                    } else {
                        awayGoals++;
                        logEvent(`[${gameMinute}'] GOAL! ${awayName} ได้ประตู!`);
                    }
                    document.getElementById('scoreBoard').innerText = `${homeName} ${homeGoals} - ${awayGoals} ${awayName}`;
                }

                if (realSeconds >= TOTAL_REAL_SECONDS) {
                    clearInterval(matchInterval);
                    logEvent(`> [90'] จบการแข่งขัน! สกอร์รวม: ${homeName} ${homeGoals} - ${awayGoals} ${awayName}`);
                    alert(`จบการแข่งขัน 25 นาที!\nผลการแข่งขัน: ${homeName} ${homeGoals} - ${awayGoals} ${awayName}`);
                }
            }, 1000);
        }

        function logEvent(msg) {
            const logBox = document.getElementById('eventLog');
            logBox.innerHTML += `> ${msg}<br>`;
            logBox.scrollTop = logBox.scrollHeight;
        }

        function moveBallAndPlayers() {
            let ball = document.getElementById('ball');
            let ballX = Math.min(Math.max(Math.random() * 80 + 10, 10), 90);
            let ballY = Math.min(Math.max(Math.random() * 80 + 10, 10), 90);
            ball.style.left = ballX + '%';
            ball.style.top = ballY + '%';

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
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM teams ORDER BY rating DESC")
    teams = cursor.fetchall()

    pitch_players = get_22_positions()

    return render_template_string(
        HTML_TEMPLATE, 
        teams=teams,
        pitch_players=pitch_players
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
