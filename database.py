import sqlite3
import random

def get_db_connection():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn):
    cursor = conn.cursor()
    
    # 1. Teams Table
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

    # 2. Managers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tactical_style TEXT DEFAULT 'Balanced',
            in_game_reading INTEGER DEFAULT 75,
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
            team_id INTEGER
        )
    ''')

    # Seed National Teams (Complete Confederations)
    national_teams = [
        ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'World Cup Qualifiers'),
        ('France', 'National', 'France', 'UEFA', 91, 2, 'UEFA Euro'),
        ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'UEFA Euro'),
        ('England', 'National', 'England', 'UEFA', 89, 4, 'UEFA Euro'),
        ('Brazil', 'National', 'Brazil', 'CONMEBOL', 90, 5, 'World Cup Qualifiers'),
        ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'AFC Asian Cup'),
        ('South Korea', 'National', 'South Korea', 'AFC', 83, 22, 'AFC Asian Cup'),
        ('Australia', 'National', 'Australia', 'AFC', 80, 24, 'AFC Asian Cup'),
        ('Saudi Arabia', 'National', 'Saudi Arabia', 'AFC', 78, 56, 'AFC Asian Cup'),
        ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'AFC Asian Cup'),
        ('Vietnam', 'National', 'Vietnam', 'AFC', 69, 115, 'AFC Asian Cup'),
        ('Indonesia', 'National', 'Indonesia', 'AFC', 68, 133, 'AFC Asian Cup')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', national_teams)

    # Seed Club Teams
    club_teams = [
        ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1'),
        ('BG Pathum United', 'Club', 'Thailand', 'AFC', 73, 0, 'Thai League 1'),
        ('Kawasaki Frontale', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Yokohama F. Marinos', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League'),
        ('Arsenal', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga'),
        ('FC Barcelona', 'Club', 'Spain', 'UEFA', 89, 0, 'La Liga')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', club_teams)

    # Auto-generate Managers & Players for each team
    cursor.execute("SELECT id, name, rating FROM teams")
    teams = cursor.fetchall()
    positions = ['GK', 'RB', 'CB', 'CB', 'LB', 'CDM', 'CM', 'CAM', 'RW', 'ST', 'LW']

    for team in teams:
        t_id, t_name, t_rating = team['id'], team['name'], team['rating']
        
        # Add Manager
        cursor.execute("INSERT INTO managers (name, tactical_style, in_game_reading, team_id) VALUES (?, ?, ?, ?)",
                       (f"Manager {t_name}", "Balanced", random.randint(75, 95), t_id))
        
        # Add Squad
        for pos in positions:
            p_name = f"{t_name} {pos}"
            if t_name == 'Thailand' and pos == 'CAM': p_name = 'Chanathip Songkrasin'
            elif t_name == 'Thailand' and pos == 'ST': p_name = 'Supachai Chaided'
            elif t_name == 'Real Madrid' and pos == 'CAM': p_name = 'Jude Bellingham'
            elif t_name == 'Manchester City' and pos == 'ST': p_name = 'Erling Haaland'

            cursor.execute('''
                INSERT INTO players (name, position, age, pace, finishing, vision, stamina, team_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (p_name, pos, random.randint(19, 32), t_rating, t_rating, t_rating, 100, t_id))

    conn.commit()
