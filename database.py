import sqlite3

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

    # 2. Trophies History Table (ตารางบันทึกประวัติแชมป์)
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
    national_teams = [
        ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'FIFA World Cup'),
        ('France', 'National', 'France', 'UEFA', 91, 2, 'FIFA World Cup / UEFA Euro'),
        ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'FIFA World Cup / UEFA Euro'),
        ('England', 'National', 'England', 'UEFA', 89, 4, 'FIFA World Cup / UEFA Euro'),
        ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'FIFA World Cup / AFC Asian Cup'),
        ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'FIFA World Cup / AFC Asian Cup')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', national_teams)

    club_teams = [
        ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1'),
        ('Kawasaki Frontale', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League'),
        ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', club_teams)

    # Seed Sample Champions History Logs (ข้อมูลประวัติแชมป์ตั้งต้น)
    sample_history = [
        ('FIFA World Cup', 2022, 'Argentina', 'France', '3 - 3 (p 4-2)'),
        ('UEFA Euro', 2024, 'Spain', 'England', '2 - 1'),
        ('AFC Asian Cup', 2023, 'Qatar', 'Jordan', '3 - 1'),
        ('Premier League', 2024, 'Manchester City', 'Arsenal', '91 Pts'),
        ('La Liga', 2024, 'Real Madrid', 'FC Barcelona', '95 Pts'),
        ('Thai League 1', 2024, 'Buriram United', 'Bangkok United', '69 Pts'),
        ('J1 League', 2023, 'Vissel Kobe', 'Yokohama F. Marinos', '71 Pts')
    ]
    cursor.executemany('''
        INSERT INTO trophies_history (tournament_name, year, champion_team, runner_up, score)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_history)

    conn.commit()
