from flask import Flask, render_template_string, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# --- DATABASE SETUP & EXTENDED DATA SEEDING ---
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    
    # 1. Teams Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL, -- 'National' or 'Club'
            country TEXT,
            confederation TEXT,
            rating INTEGER DEFAULT 70,
            fifa_ranking INTEGER DEFAULT 100,
            league TEXT DEFAULT ''
        )
    ''')

    # 2. Managers Table
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

    # 3. Players Table
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
            career_apps INTEGER DEFAULT 0,
            history_log TEXT DEFAULT ''
        )
    ''')

    # -------------------------------------------------------------
    # SEEDING NATIONAL TEAMS (AFC, UEFA, CONMEBOL, CAF, CONCACAF)
    # -------------------------------------------------------------
    national_teams = [
        # AFC (Asia)
        ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Iran', 'National', 'Iran', 'AFC', 81, 20, 'AFC Asian Cup / World Cup Qualifiers'),
        ('South Korea', 'National', 'South Korea', 'AFC', 83, 22, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Australia', 'National', 'Australia', 'AFC', 80, 24, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Qatar', 'National', 'Qatar', 'AFC', 77, 34, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Saudi Arabia', 'National', 'Saudi Arabia', 'AFC', 78, 56, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Iraq', 'National', 'Iraq', 'AFC', 75, 58, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Uzbekistan', 'National', 'Uzbekistan', 'AFC', 74, 60, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Vietnam', 'National', 'Vietnam', 'AFC', 69, 115, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Indonesia', 'National', 'Indonesia', 'AFC', 68, 133, 'AFC Asian Cup / World Cup Qualifiers'),
        ('Malaysia', 'National', 'Malaysia', 'AFC', 67, 134, 'AFC Asian Cup / World Cup Qualifiers'),

        # UEFA (Europe)
        ('France', 'National', 'France', 'UEFA', 91, 2, 'UEFA Euro / World Cup Qualifiers'),
        ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'UEFA Euro / World Cup Qualifiers'),
        ('England', 'National', 'England', 'UEFA', 89, 4, 'UEFA Euro / World Cup Qualifiers'),
        ('Belgium', 'National', 'Belgium', 'UEFA', 86, 6, 'UEFA Euro / World Cup Qualifiers'),
        ('Netherlands', 'National', 'Netherlands', 'UEFA', 87, 7, 'UEFA Euro / World Cup Qualifiers'),
        ('Portugal', 'National', 'Portugal', 'UEFA', 88, 8, 'UEFA Euro / World Cup Qualifiers'),
        ('Italy', 'National', 'Italy', 'UEFA', 86, 10, 'UEFA Euro / World Cup Qualifiers'),
        ('Germany', 'National', 'Germany', 'UEFA', 88, 12, 'UEFA Euro / World Cup Qualifiers'),

        # CONMEBOL & CAF & CONCACAF (Americas & Africa)
        ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'World Cup Qualifiers'),
        ('Brazil', 'National', 'Brazil', 'CONMEBOL', 90, 5, 'World Cup Qualifiers'),
        ('Uruguay', 'National', 'Uruguay', 'CONMEBOL', 85, 11, 'World Cup Qualifiers'),
        ('Morocco', 'National', 'Morocco', 'CAF', 84, 14, 'World Cup Qualifiers'),
        ('USA', 'National', 'USA', 'CONCACAF', 81, 16, 'World Cup Qualifiers'),
        ('Mexico', 'National', 'Mexico', 'CONCACAF', 82, 17, 'World Cup Qualifiers')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', national_teams)

    # -------------------------------------------------------------
    # SEEDING CLUB TEAMS (Thai League, J-League, EPL, La Liga)
    # -------------------------------------------------------------
    club_teams = [
        # Thai League 1
        ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1'),
        ('BG Pathum United', 'Club', 'Thailand', 'AFC', 73, 0, 'Thai League 1'),
        ('Port FC', 'Club', 'Thailand', 'AFC', 72, 0, 'Thai League 1'),
        ('Bangkok United', 'Club', 'Thailand', 'AFC', 74, 0, 'Thai League 1'),
        ('Muangthong United', 'Club', 'Thailand', 'AFC', 71, 0, 'Thai League 1'),

        # J1 League (Japan)
        ('Vissel Kobe', 'Club', 'Japan', 'AFC', 79, 0, 'J1 League'),
        ('Kawasaki Frontale', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Yokohama F. Marinos', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Urawa Red Diamonds', 'Club', 'Japan', 'AFC', 77, 0, 'J1 League'),
        ('Sanfrecce Hiroshima', 'Club', 'Japan', 'AFC', 77, 0, 'J1 League'),

        # Premier League (England)
        ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League'),
        ('Arsenal', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        ('Liverpool', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        ('Chelsea', 'Club', 'England', 'UEFA', 84, 0, 'Premier League'),
        ('Manchester United', 'Club', 'England', 'UEFA', 83, 0, 'Premier League'),

        # La Liga (Spain)
        ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga'),
        ('FC Barcelona', 'Club', 'Spain', 'UEFA', 89, 0, 'La Liga'),
        ('Atletico Madrid', 'Club', 'Spain', 'UEFA', 86, 0, 'La Liga'),
        
        # Other European Giants
        ('Bayern Munich', 'Club', 'Germany', 'UEFA', 90, 0, 'Bundesliga'),
        ('Paris Saint-Germain', 'Club', 'France', 'UEFA', 88, 0, 'Ligue 1'),
        ('Inter Milan', 'Club', 'Italy', 'UEFA', 87, 0, 'Serie A')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', club_teams)

    # -------------------------------------------------------------
    # SEEDING MANAGERS & PLAYERS
    # -------------------------------------------------------------
    managers = [
        ('Masatada Ishii', 'Balanced', 83, 85, 9),      # Thailand
        ('Hajime Moriyasu', 'Counter', 85, 82, 1),      # Japan
        ('Pep Guardiola', 'Positional', 96, 95, 23),    # Man City
        ('Mikel Arteta', 'Possession', 89, 88, 24),     # Arsenal
        ('Carlo Ancelotti', 'Adaptive', 95, 96, 28)     # Real Madrid
    ]
    cursor.executemany('''
        INSERT INTO managers (name, tactical_style, in_game_reading, adaptability, team_id)
        VALUES (?, ?, ?, ?, ?)
    ''', managers)

    players = [
        ('Chanathip Songkrasin', 'CAM', 31, 78, 72, 86, 80, 9, 12, 65, 'Thailand National Team / BG Pathum'),
        ('Supachai Chaided', 'ST', 27, 75, 78, 68, 82, 9, 15, 42, 'Thailand National Team / Buriram United'),
        ('Kaoru Mitoma', 'LW', 29, 90, 79, 82, 85, 1, 8, 34, 'Japan National Team'),
        ('Takefusa Kubo', 'RW', 25, 86, 77, 85, 82, 1, 6, 29, 'Japan National Team'),
        ('Erling Haaland', 'ST', 26, 89, 94, 65, 88, 23, 38, 45, 'Manchester City'),
        ('Jude Bellingham', 'CAM', 23, 82, 86, 89, 92, 28, 22, 50, 'Real Madrid / England')
    ]
    cursor.executemany('''
        INSERT INTO players (name, position, age, pace, finishing, vision, stamina, team_id, career_goals, career_apps, history_log)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', players)

    conn.commit()
    return conn

db_conn = init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GBA Football Simulator - Step 2 World Rankings</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; margin: 0; padding: 20px; }
        h1 { margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px #000; }
        .subtitle { color: #888; font-size: 14px; margin-bottom: 25px; }
        
        .tab-buttons { margin-bottom: 20px; }
        .tab-btn { background: #222; color: #aaa; border: 1px solid #444; padding: 10px 20px; cursor: pointer; font-weight: bold; border-radius: 4px; margin: 0 5px; }
        .tab-btn.active { background: #ff4500; color: white; border-color: #ff4500; }

        .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; }
        .box { background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; width: 420px; text-align: left; }
        .box h3 { margin-top: 0; color: #ff4500; border-bottom: 1px solid #444; padding-bottom: 8px; font-size: 16px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid #2a2a2a; }
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

        .btn { background: #ff4500; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; margin-top: 15px; }
        .btn:hover { background: #ff5722; }
    </style>
</head>
<body>
    <h1>Step 2: World Teams & Rankings</h1>
    <div class="subtitle">FIFA World Rankings, Club Ratings & Complete Database Infrastructure</div>

    <div class="tab-buttons">
        <button class="tab-btn active" onclick="showSection('fifa')">FIFA World Rankings (National)</button>
        <button class="tab-btn" onclick="showSection('clubs')">Top Clubs & Leagues</button>
        <button class="tab-btn" onclick="showSection('players')">Star Players Database</button>
    </div>

    <div class="container">
        <!-- FIFA World Rankings Table -->
        <div class="box" id="sec-fifa">
            <h3>FIFA World Rankings (National Teams)</h3>
            <table>
                <tr><th>Rank</th><th>Team</th><th>Confederation</th><th>Rating</th></tr>
                {% for team in fifa_teams %}
                <tr>
                    <td><b>#{{ team[6] }}</b></td>
                    <td>{{ team[1] }}</td>
                    <td>{{ team[4] }}</td>
                    <td>{{ team[5] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <!-- Clubs Table -->
        <div class="box" id="sec-clubs" style="display:none;">
            <h3>Top Clubs & League System</h3>
            <table>
                <tr><th>Club</th><th>League</th><th>Country</th><th>Rating</th></tr>
                {% for club in club_teams %}
                <tr>
                    <td><b>{{ club[1] }}</b></td>
                    <td>{{ club[7] }}</td>
                    <td>{{ club[3] }}</td>
                    <td>{{ club[5] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <!-- Players Table -->
        <div class="box" id="sec-players" style="display:none;">
            <h3>Star Players & Career Logs</h3>
            <table>
                <tr><th>Player</th><th>Pos</th><th>Pace</th><th>Finishing</th><th>Goals</th></tr>
                {% for p in players %}
                <tr>
                    <td><b>{{ p[1] }}</b></td>
                    <td>{{ p[2] }}</td>
                    <td>{{ p[4] }}</td>
                    <td>{{ p[5] }}</td>
                    <td>{{ p[8] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <!-- Match Pitch -->
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
    </div>

    <button class="btn" onclick="moveBallAndPlayers()">Simulate Match Movement</button>

    <script>
        function showSection(sectionId) {
            document.getElementById('sec-fifa').style.display = 'none';
            document.getElementById('sec-clubs').style.display = 'none';
            document.getElementById('sec-players').style.display = 'none';

            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(b => b.classList.remove('active'));

            if (sectionId === 'fifa') {
                document.getElementById('sec-fifa').style.display = 'block';
                buttons[0].classList.add('active');
            } else if (sectionId === 'clubs') {
                document.getElementById('sec-clubs').style.display = 'block';
                buttons[1].classList.add('active');
            } else if (sectionId === 'players') {
                document.getElementById('sec-players').style.display = 'block';
                buttons[2].classList.add('active');
            }
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
    
    # Query FIFA National Teams ordered by Rank
    cursor.execute("SELECT * FROM teams WHERE type='National' ORDER BY fifa_ranking ASC")
    fifa_teams = cursor.fetchall()
    
    # Query Clubs ordered by Rating
    cursor.execute("SELECT * FROM teams WHERE type='Club' ORDER BY rating DESC")
    club_teams = cursor.fetchall()

    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()

    pitch_players = get_22_positions()

    return render_template_string(
        HTML_TEMPLATE, 
        fifa_teams=fifa_teams,
        club_teams=club_teams, 
        players=players, 
        pitch_players=pitch_players
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
