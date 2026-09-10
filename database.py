import sqlite3
import random

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

    # National Teams with Tournaments
    national_teams = [
        ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'FIFA World Cup'),
        ('France', 'National', 'France', 'UEFA', 91, 2, 'FIFA World Cup / UEFA Euro'),
        ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'FIFA World Cup / UEFA Euro'),
        ('England', 'National', 'England', 'UEFA', 89, 4, 'FIFA World Cup / UEFA Euro'),
        ('Brazil', 'National', 'Brazil', 'CONMEBOL', 90, 5, 'FIFA World Cup'),
        ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'FIFA World Cup / AFC Asian Cup'),
        ('South Korea', 'National', 'South Korea', 'AFC', 83, 22, 'FIFA World Cup / AFC Asian Cup'),
        ('Australia', 'National', 'Australia', 'AFC', 80, 24, 'FIFA World Cup / AFC Asian Cup'),
        ('Saudi Arabia', 'National', 'Saudi Arabia', 'AFC', 78, 56, 'FIFA World Cup / AFC Asian Cup'),
        ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'FIFA World Cup / AFC Asian Cup'),
        ('Vietnam', 'National', 'Vietnam', 'AFC', 69, 115, 'FIFA World Cup / AFC Asian Cup'),
        ('Indonesia', 'National', 'Indonesia', 'AFC', 68, 133, 'FIFA World Cup / AFC Asian Cup')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', national_teams)

    # Club Teams with Domestic Leagues
    club_teams = [
        # Thai League 1
        ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1'),
        ('BG Pathum United', 'Club', 'Thailand', 'AFC', 73, 0, 'Thai League 1'),
        ('Port FC', 'Club', 'Thailand', 'AFC', 72, 0, 'Thai League 1'),
        ('Bangkok United', 'Club', 'Thailand', 'AFC', 74, 0, 'Thai League 1'),
        
        # J1 League
        ('Kawasaki Frontale', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Yokohama F. Marinos', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Vissel Kobe', 'Club', 'Japan', 'AFC', 79, 0, 'J1 League'),
        
        # Premier League
        ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League'),
        ('Arsenal', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        ('Liverpool', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        
        # La Liga
        ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga'),
        ('FC Barcelona', 'Club', 'Spain', 'UEFA', 89, 0, 'La Liga'),
        ('Atletico Madrid', 'Club', 'Spain', 'UEFA', 86, 0, 'La Liga')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', club_teams)

    conn.commit()
