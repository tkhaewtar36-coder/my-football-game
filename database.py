import sqlite3
import random
from data_seeding import NATIONAL_TEAMS, CLUB_TEAMS, REAL_MANAGERS, STAR_PLAYERS, TROPHIES_HISTORY_SAMPLES

def get_db_connection():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn):
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
            league TEXT DEFAULT ''
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tactical_style TEXT DEFAULT 'Balanced',
            in_game_reading INTEGER DEFAULT 75,
            team_id INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shirt_number INTEGER NOT NULL,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            role_type TEXT DEFAULT 'STARTER',
            age INTEGER,
            pace INTEGER DEFAULT 70,
            finishing INTEGER DEFAULT 70,
            vision INTEGER DEFAULT 70,
            stamina INTEGER DEFAULT 100,
            team_id INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trophies_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            champion_team TEXT NOT NULL,
            runner_up TEXT NOT NULL,
            score TEXT NOT NULL
        )
    ''')

    # Seed Teams
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', NATIONAL_TEAMS + CLUB_TEAMS)

    cursor.execute("SELECT id, name, rating FROM teams")
    all_teams = cursor.fetchall()
    
    # Standard 23-Man Squad Positions (1-11 Starters, 12-23 Subs)
    squad_23_positions = [
        ('GK', 'STARTER'), ('RB', 'STARTER'), ('CB', 'STARTER'), ('CB', 'STARTER'), ('LB', 'STARTER'),
        ('CDM', 'STARTER'), ('CM', 'STARTER'), ('CAM', 'STARTER'), ('RW', 'STARTER'), ('ST', 'STARTER'), ('LW', 'STARTER'),
        ('GK', 'SUB'), ('RB', 'SUB'), ('LB', 'SUB'), ('CB', 'SUB'), ('CDM', 'SUB'), ('CM', 'SUB'),
        ('CAM', 'SUB'), ('RW', 'SUB'), ('LW', 'SUB'), ('ST', 'SUB'), ('ST', 'SUB'), ('GK', 'SUB')
    ]

    for team in all_teams:
        t_id, t_name, t_rating = team['id'], team['name'], team['rating']
        
        # Add Manager
        m_info = REAL_MANAGERS.get(t_name, (f"Manager {t_name}", "Balanced"))
        cursor.execute("INSERT INTO managers (name, tactical_style, in_game_reading, team_id) VALUES (?, ?, ?, ?)",
                       (m_info[0], m_info[1], random.randint(78, 96), t_id))

        # Add 23 Squad Players numbered 1 to 23
        existing_stars = STAR_PLAYERS.get(t_name, [])
        star_idx = 0

        for number in range(1, 24):
            pos, role = squad_23_positions[number - 1]
            
            # Use star player if available for matching position/slot
            if star_idx < len(existing_stars):
                p_name = existing_stars[star_idx][0]
                pos = existing_stars[star_idx][1]
                star_idx += 1
            else:
                p_name = f"Player #{number} ({pos})"

            cursor.execute('''
                INSERT INTO players (shirt_number, name, position, role_type, age, pace, finishing, vision, stamina, team_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (number, p_name, pos, role, random.randint(18, 34),
                  max(50, min(99, t_rating + random.randint(-5, 5))),
                  max(50, min(99, t_rating + random.randint(-5, 5))),
                  max(50, min(99, t_rating + random.randint(-5, 5))), 100, t_id))

    cursor.executemany('''
        INSERT INTO trophies_history (tournament_name, year, champion_team, runner_up, score)
        VALUES (?, ?, ?, ?, ?)
    ''', TROPHIES_HISTORY_SAMPLES)

    conn.commit()

# =========================================================================
# 🚀 เพิ่มส่วนต่อขยาย: ฟังก์ชันสุ่มจับฉลากรอบคัดเลือกทวีป & รอบสุดท้าย 32 ทีม
# =========================================================================

def generate_qualifiers_and_draw(conn):
    """
    1. ดึงทีมชาติทั้งหมดแยกตามทวีป (Confederation)
    2. สุ่มจับฉลากรอบคัดเลือกในทวีปตัวเอง
    3. สิมูเลตหาผู้ผ่านเข้ารอบตามโควตาจริงเพื่อไปจับฉลากฟุตบอลโลกรอบสุดท้าย (A-H)
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name, confederation, rating, fifa_ranking FROM teams WHERE type = 'National'")
    national_teams = cursor.fetchall()

    # แยกทีมตามทวีป
    confeds = {}
    for t in national_teams:
        c = t['confederation'] or 'AFC'
        if c not in confeds:
            confeds[c] = []
        confeds[c].append(dict(t))

    # 1. จับฉลากแบ่งกลุ่มรอบคัดเลือกแยกตามทวีป
    qualifier_groups = {}
    for c_name, t_list in confeds.items():
        random.shuffle(t_list)
        # ถ้าทีมเยอะ ให้แบ่งเป็น 2 กลุ่ม (เช่น Group A, Group B ของทวีปนั้น)
        num_groups = 2 if len(t_list) >= 8 else 1
        qualifier_groups[c_name] = {f'Group {chr(65+i)}': [] for i in range(num_groups)}
        
        for idx, team in enumerate(t_list):
            g_key = f'Group {chr(65 + (idx % num_groups))}'
            qualifier_groups[c_name][g_key].append(team)

    # 2. จำลองทีมผู้ชนะผ่านเข้ารอบสุดท้าย 32 ทีม (อิงตามโควตาจริง)
    # โควตา: UEFA 13, CONMEBOL 5, AFC 6, CAF 4, CONCACAF 3, OFC 1
    quotas = {'UEFA': 13, 'CONMEBOL': 5, 'AFC': 6, 'CAF': 4, 'CONCACAF': 3, 'OFC': 1}
    qualified_finalists = []

    for c_name, quota in quotas.items():
        teams_in_c = confeds.get(c_name, [])
        # คำนวณความสามารถ + ค่าสุ่มเพื่อหาทีมที่ผ่านรอบคัดเลือก
        sorted_teams = sorted(teams_in_c, key=lambda x: x['rating'] + random.randint(-6, 6), reverse=True)
        qualified_finalists.extend(sorted_teams[:quota])

    # 3. จับฉลากฟุตบอลโลกรอบสุดท้าย (World Cup Groups A - H)
    random.shuffle(qualified_finalists)
    world_cup_groups = {f'Group {chr(65+i)}': [] for i in range(8)}
    
    for idx, team in enumerate(qualified_finalists):
        group_key = f'Group {chr(65 + (idx % 8))}'
        world_cup_groups[group_key].append(team)

    return {
        'qualifiers': qualifier_groups,
        'world_cup_groups': world_cup_groups
    }
