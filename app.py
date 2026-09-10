from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GBA Football Tactics Simulator</title>
    <style>
        body { background-color: #1a1a1a; color: #fff; font-family: monospace; text-align: center; }
        .pitch { width: 300px; height: 400px; background-color: #2e8b57; margin: 20px auto; border: 4px solid #fff; position: relative; }
        .line { position: absolute; top: 50%; width: 100%; height: 2px; background: #fff; }
        .btn { background: #ff4500; color: white; padding: 10px 20px; border: none; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <h1>GBA Football Simulator</h1>
    <form method="POST">
        <label>เลือกแผนการเล่น (Home): </label>
        <select name="formation">
            <option value="4-3-3">4-3-3</option>
            <option value="4-4-2">4-4-2</option>
            <option value="3-5-2">3-5-2</option>
        </select>
        <button type="submit" class="btn">จำลองการแข่งขัน</button>
    </form>

    <div class="pitch">
        <div class="line"></div>
        <p style="padding-top: 20px;">[ สนามแข่ง พิกเซล ]</p>
    </div>

    {% if result %}
        <h2>ผลการแข่งขัน: {{ result }}</h2>
        <p>{{ details }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    details = ""
    if request.method == 'POST':
        formation = request.form.get('formation')
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 3)
        result = f"ทีมคุณ ({formation}) {home_score} - {away_score} ทีมคู่แข่ง"
        details = "ระบบประมวลผลตามแผนการเล่นและสุ่มผลการแข่งเรียบร้อยแล้ว!"
    return render_template_string(HTML_TEMPLATE, result=result, details=details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GBA Football Tactics Simulator</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; padding: 20px; }
        h1 { margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px #000; }
        
        .controls { margin-bottom: 20px; background: #1e1e1e; display: inline-block; padding: 15px 25px; border-radius: 8px; border: 1px solid #333; }
        select { padding: 8px 12px; background: #2b2b2b; color: white; border: 1px solid #444; border-radius: 4px; font-size: 14px; }
        .btn { background: #ff4500; color: white; padding: 9px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; margin-left: 10px; transition: 0.2s; }
        .btn:hover { background: #ff5722; }

        /* Tactical Pitch Design */
        .pitch { 
            width: 320px; 
            height: 460px; 
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
        .goal-area-top { position: absolute; top: 0; left: 50%; width: 70px; height: 25px; border: 2px solid rgba(255,255,255,0.8); border-top: none; transform: translateX(-50%); }
        
        .penalty-area-bottom { position: absolute; bottom: 0; left: 50%; width: 150px; height: 65px; border: 2px solid rgba(255,255,255,0.8); border-bottom: none; transform: translateX(-50%); }
        .goal-area-bottom { position: absolute; bottom: 0; left: 50%; width: 70px; height: 25px; border: 2px solid rgba(255,255,255,0.8); border-bottom: none; transform: translateX(-50%); }

        /* Player Pin / Icon */
        .player {
            position: absolute;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
            transform: translate(-50%, -50%);
            border: 2px solid #fff;
        }
        .home-team { background-color: #d32f2f; } /* Red Kit */
        .away-team { background-color: #1976d2; } /* Blue Kit */
        .gk { background-color: #fbc02d; color: black; } /* Yellow GK */

        .result-box { margin-top: 25px; background: #1e1e1e; display: inline-block; padding: 15px 30px; border-radius: 8px; border: 1px solid #333; }
    </style>
</head>
<body>
    <h1>GBA Tactical Board</h1>
    <div class="controls">
        <form method="POST">
            <label>เลือกแผนการเล่น: </label>
            <select name="formation">
                <option value="4-3-3" {% if formation == '4-3-3' %}selected{% endif %}>4-3-3</option>
                <option value="4-4-2" {% if formation == '4-4-2' %}selected{% endif %}>4-4-2</option>
                <option value="3-5-2" {% if formation == '3-5-2' %}selected{% endif %}>3-5-2</option>
            </select>
            <button type="submit" class="btn">จัดแผน / จำลองการแข่ง</button>
        </form>
    </div>

    <div class="pitch">
        <!-- Lines -->
        <div class="halfway-line"></div>
        <div class="center-circle"></div>
        <div class="center-dot"></div>
        <div class="penalty-area-top"></div>
        <div class="goal-area-top"></div>
        <div class="penalty-area-bottom"></div>
        <div class="goal-area-bottom"></div>

        <!-- Players Position (Dynamic) -->
        {% for p in players %}
            <div class="player {{ p.type }}" style="left: {{ p.x }}%; top: {{ p.y }}%;">{{ p.num }}</div>
        {% endfor %}
    </div>

    {% if result %}
        <div class="result-box">
            <h2>{{ result }}</h2>
            <p style="color: #aaa;">{{ details }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

def get_positions(formation):
    # Default 4-3-3 Home (Red) vs Away (Blue)
    players = [
        # Home GK & Defenders (Bottom)
        {'num': 'GK', 'x': 50, 'y': 92, 'type': 'gk'},
        {'num': '4', 'x': 20, 'y': 78, 'type': 'home-team'},
        {'num': '5', 'x': 40, 'y': 80, 'type': 'home-team'},
        {'num': '3', 'x': 60, 'y': 80, 'type': 'home-team'},
        {'num': '2', 'x': 80, 'y': 78, 'type': 'home-team'},
        # Midfielders
        {'num': '8', 'x': 30, 'y': 62, 'type': 'home-team'},
        {'num': '6', 'x': 50, 'y': 65, 'type': 'home-team'},
        {'num': '10', 'x': 70, 'y': 62, 'type': 'home-team'},
        # Forwards
        {'num': '7', 'x': 20, 'y': 48, 'type': 'home-team'},
        {'num': '9', 'x': 50, 'y': 45, 'type': 'home-team'},
        {'num': '11', 'x': 80, 'y': 48, 'type': 'home-team'},

        # Away Opponent Pins (Top)
        {'num': 'GK', 'x': 50, 'y': 8, 'type': 'gk'},
        {'num': '4', 'x': 30, 'y': 20, 'type': 'away-team'},
        {'num': '5', 'x': 70, 'y': 20, 'type': 'away-team'},
        {'num': '8', 'x': 40, 'y': 35, 'type': 'away-team'},
        {'num': '10', 'x': 60, 'y': 35, 'type': 'away-team'}
    ]
    return players

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    details = ""
    formation = "4-3-3"
    
    if request.method == 'POST':
        formation = request.form.get('formation', '4-3-3')
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 3)
        result = f"ทีมคุณ ({formation}) {home_score} - {away_score} ทีมคู่แข่ง"
        details = "จำลองการบุกและยิงประตูสำเร็จ!"

    players = get_positions(formation)
    return render_template_string(HTML_TEMPLATE, result=result, details=details, players=players, formation=formation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
