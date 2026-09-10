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
