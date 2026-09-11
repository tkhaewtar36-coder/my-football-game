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
