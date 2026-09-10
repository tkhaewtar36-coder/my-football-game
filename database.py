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
            name TEXT NOT NULL,
            position TEXT NOT NULL,
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

    # Seed Managers & Players
    cursor.execute("SELECT id, name, rating FROM teams")
    all_teams = cursor.fetchall()
    positions_list = ['GK', 'RB', 'CB', 'CB', 'LB', 'CDM', 'CM', 'CAM', 'RW', 'ST', 'LW', 'SUB-GK', 'SUB-DEF', 'SUB-MID', 'SUB-FWD']

    for team in all_teams:
        t_id, t_name, t_rating = team['id'], team['name'], team['rating']
        
        # Add Manager
        m_info = REAL_MANAGERS.get(t_name, (f"Manager {t_name}", "Balanced"))
        cursor.execute("INSERT INTO managers (name, tactical_style, in_game_reading, team_id) VALUES (?, ?, ?, ?)",
                       (m_info[0], m_info[1], random.randint(78, 96), t_id))

        # Add Players
        existing_stars = STAR_PLAYERS.get(t_name, [])
        for s_name, s_pos in existing_stars:
            cursor.execute('''
                INSERT INTO players (name, position, age, pace, finishing, vision, stamina, team_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (s_name, s_pos, random.randint(20, 33), min(t_rating+3, 99), min(t_rating+3, 99), min(t_rating+3, 99), 100, t_id))

        needed_count = 15 - len(existing_stars)
        for i in range(needed_count):
            pos = positions_list[i % len(positions_list)]
            p_name = f"{t_name} Player {i+1}"
            cursor.execute('''
                INSERT INTO players (name, position, age, pace, finishing, vision, stamina, team_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (p_name, pos, random.randint(18, 34), max(50, min(99, t_rating + random.randint(-6, 4))),
                  max(50, min(99, t_rating + random.randint(-6, 4))), max(50, min(99, t_rating + random.randint(-6, 4))), 100, t_id))

    # Seed Trophies
    cursor.executemany('''
        INSERT INTO trophies_history (tournament_name, year, champion_team, runner_up, score)
        VALUES (?, ?, ?, ?, ?)
    ''', TROPHIES_HISTORY_SAMPLES)

    conn.commit()
