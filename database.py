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

    # 2. Trophies History Table
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

    # -------------------------------------------------------------
    # EXPANDED FIFA NATIONAL TEAMS FROM ALL CONTINENTS
    # -------------------------------------------------------------
    national_teams = [
        # CONMEBOL (South America)
        ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'FIFA World Cup'),
        ('Brazil', 'National', 'Brazil', 'CONMEBOL', 90, 5, 'FIFA World Cup'),
        ('Colombia', 'National', 'Colombia', 'CONMEBOL', 86, 9, 'FIFA World Cup'),
        ('Uruguay', 'National', 'Uruguay', 'CONMEBOL', 85, 11, 'FIFA World Cup'),
        ('Ecuador', 'National', 'Ecuador', 'CONMEBOL', 80, 27, 'FIFA World Cup'),
        ('Chile', 'National', 'Chile', 'CONMEBOL', 78, 43, 'FIFA World Cup'),
        ('Peru', 'National', 'Peru', 'CONMEBOL', 77, 42, 'FIFA World Cup'),
        ('Venezuela', 'National', 'Venezuela', 'CONMEBOL', 76, 54, 'FIFA World Cup'),
        ('Paraguay', 'National', 'Paraguay', 'CONMEBOL', 75, 62, 'FIFA World Cup'),
        ('Bolivia', 'National', 'Bolivia', 'CONMEBOL', 70, 84, 'FIFA World Cup'),

        # UEFA (Europe)
        ('France', 'National', 'France', 'UEFA', 91, 2, 'FIFA World Cup / UEFA Euro'),
        ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'FIFA World Cup / UEFA Euro'),
        ('England', 'National', 'England', 'UEFA', 89, 4, 'FIFA World Cup / UEFA Euro'),
        ('Belgium', 'National', 'Belgium', 'UEFA', 86, 6, 'FIFA World Cup / UEFA Euro'),
        ('Netherlands', 'National', 'Netherlands', 'UEFA', 87, 7, 'FIFA World Cup / UEFA Euro'),
        ('Portugal', 'National', 'Portugal', 'UEFA', 88, 8, 'FIFA World Cup / UEFA Euro'),
        ('Italy', 'National', 'Italy', 'UEFA', 86, 10, 'FIFA World Cup / UEFA Euro'),
        ('Germany', 'National', 'Germany', 'UEFA', 88, 12, 'FIFA World Cup / UEFA Euro'),
        ('Croatia', 'National', 'Croatia', 'UEFA', 84, 13, 'FIFA World Cup / UEFA Euro'),
        ('Switzerland', 'National', 'Switzerland', 'UEFA', 82, 15, 'FIFA World Cup / UEFA Euro'),
        ('Denmark', 'National', 'Denmark', 'UEFA', 81, 21, 'FIFA World Cup / UEFA Euro'),
        ('Austria', 'National', 'Austria', 'UEFA', 80, 22, 'FIFA World Cup / UEFA Euro'),
        ('Ukraine', 'National', 'Ukraine', 'UEFA', 79, 25, 'FIFA World Cup / UEFA Euro'),
        ('Turkey', 'National', 'Turkey', 'UEFA', 79, 26, 'FIFA World Cup / UEFA Euro'),
        ('Poland', 'National', 'Poland', 'UEFA', 78, 28, 'FIFA World Cup / UEFA Euro'),
        ('Sweden', 'National', 'Sweden', 'UEFA', 78, 29, 'FIFA World Cup / UEFA Euro'),
        ('Wales', 'National', 'Wales', 'UEFA', 76, 30, 'FIFA World Cup / UEFA Euro'),
        ('Hungary', 'National', 'Hungary', 'UEFA', 77, 31, 'FIFA World Cup / UEFA Euro'),
        ('Scotland', 'National', 'Scotland', 'UEFA', 76, 39, 'FIFA World Cup / UEFA Euro'),
        ('Norway', 'National', 'Norway', 'UEFA', 79, 47, 'FIFA World Cup / UEFA Euro'),

        # AFC (Asia)
        ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'FIFA World Cup / AFC Asian Cup'),
        ('Iran', 'National', 'Iran', 'AFC', 81, 20, 'FIFA World Cup / AFC Asian Cup'),
        ('South Korea', 'National', 'South Korea', 'AFC', 83, 23, 'FIFA World Cup / AFC Asian Cup'),
        ('Australia', 'National', 'Australia', 'AFC', 80, 24, 'FIFA World Cup / AFC Asian Cup'),
        ('Qatar', 'National', 'Qatar', 'AFC', 77, 34, 'FIFA World Cup / AFC Asian Cup'),
        ('Saudi Arabia', 'National', 'Saudi Arabia', 'AFC', 78, 56, 'FIFA World Cup / AFC Asian Cup'),
        ('Iraq', 'National', 'Iraq', 'AFC', 75, 58, 'FIFA World Cup / AFC Asian Cup'),
        ('Uzbekistan', 'National', 'Uzbekistan', 'AFC', 74, 60, 'FIFA World Cup / AFC Asian Cup'),
        ('UAE', 'National', 'UAE', 'AFC', 72, 69, 'FIFA World Cup / AFC Asian Cup'),
        ('Jordan', 'National', 'Jordan', 'AFC', 73, 70, 'FIFA World Cup / AFC Asian Cup'),
        ('Oman', 'National', 'Oman', 'AFC', 71, 76, 'FIFA World Cup / AFC Asian Cup'),
        ('Bahrain', 'National', 'Bahrain', 'AFC', 70, 80, 'FIFA World Cup / AFC Asian Cup'),
        ('China', 'National', 'China', 'AFC', 69, 88, 'FIFA World Cup / AFC Asian Cup'),
        ('Syria', 'National', 'Syria', 'AFC', 68, 89, 'FIFA World Cup / AFC Asian Cup'),
        ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'FIFA World Cup / AFC Asian Cup'),
        ('Tajikistan', 'National', 'Tajikistan', 'AFC', 67, 103, 'FIFA World Cup / AFC Asian Cup'),
        ('Kyrgyzstan', 'National', 'Kyrgyzstan', 'AFC', 66, 104, 'FIFA World Cup / AFC Asian Cup'),
        ('Vietnam', 'National', 'Vietnam', 'AFC', 69, 115, 'FIFA World Cup / AFC Asian Cup'),
        ('North Korea', 'National', 'North Korea', 'AFC', 67, 118, 'FIFA World Cup / AFC Asian Cup'),
        ('Indonesia', 'National', 'Indonesia', 'AFC', 68, 133, 'FIFA World Cup / AFC Asian Cup'),
        ('Malaysia', 'National', 'Malaysia', 'AFC', 67, 134, 'FIFA World Cup / AFC Asian Cup'),
        ('Kuwait', 'National', 'Kuwait', 'AFC', 65, 136, 'FIFA World Cup / AFC Asian Cup'),
        ('Philippines', 'National', 'Philippines', 'AFC', 64, 145, 'FIFA World Cup / AFC Asian Cup'),
        ('Singapore', 'National', 'Singapore', 'AFC', 62, 161, 'FIFA World Cup / AFC Asian Cup'),

        # CAF (Africa)
        ('Morocco', 'National', 'Morocco', 'CAF', 84, 14, 'FIFA World Cup'),
        ('Senegal', 'National', 'Senegal', 'CAF', 83, 19, 'FIFA World Cup'),
        ('Egypt', 'National', 'Egypt', 'CAF', 80, 36, 'FIFA World Cup'),
        ('Nigeria', 'National', 'Nigeria', 'CAF', 81, 39, 'FIFA World Cup'),
        ('Algeria', 'National', 'Algeria', 'CAF', 79, 41, 'FIFA World Cup'),
        ('Cameroon', 'National', 'Cameroon', 'CAF', 77, 49, 'FIFA World Cup'),
        ('Ivory Coast', 'National', 'Ivory Coast', 'CAF', 82, 50, 'FIFA World Cup'),
        ('Mali', 'National', 'Mali', 'CAF', 76, 53, 'FIFA World Cup'),
        ('Tunisia', 'National', 'Tunisia', 'CAF', 76, 57, 'FIFA World Cup'),
        ('Ghana', 'National', 'Ghana', 'CAF', 75, 64, 'FIFA World Cup'),

        # CONCACAF (North & Central America)
        ('USA', 'National', 'USA', 'CONCACAF', 81, 16, 'FIFA World Cup'),
        ('Mexico', 'National', 'Mexico', 'CONCACAF', 82, 17, 'FIFA World Cup'),
        ('Canada', 'National', 'Canada', 'CONCACAF', 78, 40, 'FIFA World Cup'),
        ('Panama', 'National', 'Panama', 'CONCACAF', 75, 35, 'FIFA World Cup'),
        ('Costa Rica', 'National', 'Costa Rica', 'CONCACAF', 74, 48, 'FIFA World Cup'),
        ('Jamaica', 'National', 'Jamaica', 'CONCACAF', 72, 61, 'FIFA World Cup'),

        # OFC (Oceania)
        ('New Zealand', 'National', 'New Zealand', 'OFC', 72, 94, 'FIFA World Cup'),
        ('Fiji', 'National', 'Fiji', 'OFC', 58, 166, 'FIFA World Cup')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', national_teams)

    # -------------------------------------------------------------
    # CLUB TEAMS (Thai League, J-League, EPL, La Liga)
    # -------------------------------------------------------------
    club_teams = [
        # Thai League 1
        ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1'),
        ('BG Pathum United', 'Club', 'Thailand', 'AFC', 73, 0, 'Thai League 1'),
        ('Port FC', 'Club', 'Thailand', 'AFC', 72, 0, 'Thai League 1'),
        ('Bangkok United', 'Club', 'Thailand', 'AFC', 74, 0, 'Thai League 1'),
        ('Muangthong United', 'Club', 'Thailand', 'AFC', 71, 0, 'Thai League 1'),

        # J1 League
        ('Kawasaki Frontale', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Yokohama F. Marinos', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
        ('Vissel Kobe', 'Club', 'Japan', 'AFC', 79, 0, 'J1 League'),
        ('Urawa Red Diamonds', 'Club', 'Japan', 'AFC', 77, 0, 'J1 League'),

        # Premier League
        ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League'),
        ('Arsenal', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        ('Liverpool', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
        ('Chelsea', 'Club', 'England', 'UEFA', 84, 0, 'Premier League'),

        # La Liga
        ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga'),
        ('FC Barcelona', 'Club', 'Spain', 'UEFA', 89, 0, 'La Liga'),
        ('Atletico Madrid', 'Club', 'Spain', 'UEFA', 86, 0, 'La Liga')
    ]
    cursor.executemany('''
        INSERT INTO teams (name, type, country, confederation, rating, fifa_ranking, league)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', club_teams)

    # Sample Champions History Logs
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
