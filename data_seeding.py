# data_seeding.py - Full Global Teams, Current Managers & Squad Data

NATIONAL_TEAMS = [
    # CONMEBOL
    ('Argentina', 'National', 'Argentina', 'CONMEBOL', 92, 1, 'FIFA World Cup'),
    ('Brazil', 'National', 'Brazil', 'CONMEBOL', 90, 5, 'FIFA World Cup'),
    ('Colombia', 'National', 'Colombia', 'CONMEBOL', 86, 9, 'FIFA World Cup'),
    ('Uruguay', 'National', 'Uruguay', 'CONMEBOL', 85, 11, 'FIFA World Cup'),
    # UEFA
    ('France', 'National', 'France', 'UEFA', 91, 2, 'FIFA World Cup / UEFA Euro'),
    ('Spain', 'National', 'Spain', 'UEFA', 90, 3, 'FIFA World Cup / UEFA Euro'),
    ('England', 'National', 'England', 'UEFA', 89, 4, 'FIFA World Cup / UEFA Euro'),
    ('Belgium', 'National', 'Belgium', 'UEFA', 86, 6, 'FIFA World Cup / UEFA Euro'),
    ('Netherlands', 'National', 'Netherlands', 'UEFA', 87, 7, 'FIFA World Cup / UEFA Euro'),
    ('Portugal', 'National', 'Portugal', 'UEFA', 88, 8, 'FIFA World Cup / UEFA Euro'),
    ('Italy', 'National', 'Italy', 'UEFA', 86, 10, 'FIFA World Cup / UEFA Euro'),
    ('Germany', 'National', 'Germany', 'UEFA', 88, 12, 'FIFA World Cup / UEFA Euro'),
    # AFC
    ('Japan', 'National', 'Japan', 'AFC', 85, 18, 'FIFA World Cup / AFC Asian Cup'),
    ('Iran', 'National', 'Iran', 'AFC', 81, 20, 'FIFA World Cup / AFC Asian Cup'),
    ('South Korea', 'National', 'South Korea', 'AFC', 83, 23, 'FIFA World Cup / AFC Asian Cup'),
    ('Australia', 'National', 'Australia', 'AFC', 80, 24, 'FIFA World Cup / AFC Asian Cup'),
    ('Saudi Arabia', 'National', 'Saudi Arabia', 'AFC', 78, 56, 'FIFA World Cup / AFC Asian Cup'),
    ('Thailand', 'National', 'Thailand', 'AFC', 73, 101, 'FIFA World Cup / AFC Asian Cup'),
    ('Vietnam', 'National', 'Vietnam', 'AFC', 69, 115, 'FIFA World Cup / AFC Asian Cup'),
    ('Indonesia', 'National', 'Indonesia', 'AFC', 68, 133, 'FIFA World Cup / AFC Asian Cup'),
    # CAF & CONCACAF
    ('Morocco', 'National', 'Morocco', 'CAF', 84, 14, 'FIFA World Cup'),
    ('Senegal', 'National', 'Senegal', 'CAF', 83, 19, 'FIFA World Cup'),
    ('USA', 'National', 'USA', 'CONCACAF', 81, 16, 'FIFA World Cup'),
    ('Mexico', 'National', 'Mexico', 'CONCACAF', 82, 17, 'FIFA World Cup')
]

CLUB_TEAMS = [
    # Thai League 1
    ('Buriram United', 'Club', 'Thailand', 'AFC', 75, 0, 'Thai League 1'),
    ('BG Pathum United', 'Club', 'Thailand', 'AFC', 73, 0, 'Thai League 1'),
    ('Port FC', 'Club', 'Thailand', 'AFC', 72, 0, 'Thai League 1'),
    ('Bangkok United', 'Club', 'Thailand', 'AFC', 74, 0, 'Thai League 1'),
    # J1 League
    ('Kawasaki Frontale', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
    ('Yokohama F. Marinos', 'Club', 'Japan', 'AFC', 78, 0, 'J1 League'),
    ('Vissel Kobe', 'Club', 'Japan', 'AFC', 79, 0, 'J1 League'),
    # European Leagues
    ('Manchester City', 'Club', 'England', 'UEFA', 92, 0, 'Premier League'),
    ('Arsenal', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
    ('Liverpool', 'Club', 'England', 'UEFA', 89, 0, 'Premier League'),
    ('Real Madrid', 'Club', 'Spain', 'UEFA', 93, 0, 'La Liga'),
    ('FC Barcelona', 'Club', 'Spain', 'UEFA', 89, 0, 'La Liga')
]

REAL_MANAGERS = {
    'Thailand': ('Masatada Ishii', 'Balanced'),
    'Japan': ('Hajime Moriyasu', 'Counter'),
    'South Korea': ('Hong Myung-bo', 'Possession'),
    'England': ('Thomas Tuchel', 'Attacking'),
    'Spain': ('Luis de la Fuente', 'Positional'),
    'Argentina': ('Lionel Scaloni', 'Adaptive'),
    'France': ('Didier Deschamps', 'Defensive'),
    'Brazil': ('Dorival Junior', 'Attacking'),
    'Germany': ('Julian Nagelsmann', 'Gegenpress'),
    'Manchester City': ('Pep Guardiola', 'Positional'),
    'Arsenal': ('Mikel Arteta', 'Possession'),
    'Real Madrid': ('Carlo Ancelotti', 'Adaptive'),
    'Buriram United': ('Osmar Loss', 'Balanced')
}

STAR_PLAYERS = {
    'Thailand': [('Chanathip Songkrasin', 'CAM'), ('Supachai Chaided', 'ST'), ('Supachok Sarachat', 'LW'), ('Patiwat Khammai', 'GK'), ('Theerathon Bunmathan', 'LB')],
    'Japan': [('Kaoru Mitoma', 'LW'), ('Takefusa Kubo', 'RW'), ('Wataru Endo', 'CDM'), ('Takumi Minamino', 'CAM'), ('Zion Suzuki', 'GK')],
    'England': [('Harry Kane', 'ST'), ('Jude Bellingham', 'CAM'), ('Bukayo Saka', 'RW'), ('Declan Rice', 'CDM'), ('Jordan Pickford', 'GK')],
    'France': [('Kylian Mbappe', 'ST'), ('Antoine Griezmann', 'CAM'), ('Ousmane Dembele', 'RW'), ('Aurelien Tchouameni', 'CDM'), ('Mike Maignan', 'GK')],
    'Argentina': [('Lionel Messi', 'RW'), ('Julian Alvarez', 'ST'), ('Alexis Mac Allister', 'CM'), ('Rodrigo De Paul', 'CM'), ('Emiliano Martinez', 'GK')],
    'Spain': [('Lamine Yamal', 'RW'), ('Nico Williams', 'LW'), ('Rodri', 'CDM'), ('Pedri', 'CM'), ('Unai Simon', 'GK')],
    'Brazil': [('Vinicius Jr', 'LW'), ('Rodrygo', 'RW'), ('Endrick', 'ST'), ('Bruno Guimaraes', 'CM'), ('Alisson Becker', 'GK')],
    'Manchester City': [('Erling Haaland', 'ST'), ('Kevin De Bruyne', 'CAM'), ('Phil Foden', 'RW'), ('Rodri', 'CDM'), ('Ederson', 'GK')],
    'Real Madrid': [('Kylian Mbappe', 'ST'), ('Vinicius Jr', 'LW'), ('Jude Bellingham', 'CAM'), ('Federico Valverde', 'CM'), ('Thibaut Courtois', 'GK')],
    'Buriram United': [('Guilherme Bissoli', 'ST'), ('Lucas Crispim', 'CAM'), ('Goran Causic', 'CM'), ('Curtis Good', 'CB'), ('Siwarak Tedsungnoen', 'GK')]
}

TROPHIES_HISTORY_SAMPLES = [
    ('FIFA World Cup', 2022, 'Argentina', 'France', '3 - 3 (p 4-2)'),
    ('UEFA Euro', 2024, 'Spain', 'England', '2 - 1'),
    ('AFC Asian Cup', 2023, 'Qatar', 'Jordan', '3 - 1'),
    ('Premier League', 2024, 'Manchester City', 'Arsenal', '91 Pts'),
    ('La Liga', 2024, 'Real Madrid', 'FC Barcelona', '95 Pts'),
    ('Thai League 1', 2024, 'Buriram United', 'Bangkok United', '69 Pts')
]
