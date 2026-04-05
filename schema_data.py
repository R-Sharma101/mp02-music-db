import sqlite3


def build_database(conn):
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute('''CREATE TABLE IF NOT EXISTS Artist (
        artist_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        genre TEXT NOT NULL,
        origin_city TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Track (
        track_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        duration_seconds INTEGER NOT NULL,
        artist_id INTEGER NOT NULL
            REFERENCES Artist(artist_id)
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Playlist (
        playlist_id INTEGER PRIMARY KEY,
        playlist_name TEXT NOT NULL,
        owner_name TEXT NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS PlaylistTrack (
        playlist_id INTEGER NOT NULL REFERENCES Playlist(playlist_id),
        track_id INTEGER NOT NULL REFERENCES Track(track_id),
        position INTEGER NOT NULL,
        PRIMARY KEY (playlist_id, track_id)
    )''')
    conn.commit()


def seed_database(conn):
    artists = [
        (1, "Taylor Swift",      "Pop",      "West Reading, Pennsylvania"),
        (2, "Ariana Grande",     "Pop/R&B",  "Boca Raton, Florida"),
        (3, "Billie Eilish",     "Alt Pop",  "Los Angeles, California"),
        (4, "Harry Styles",      "Pop Rock", "Redditch, England"),
        (5, "The Weeknd",        "R&B",      "Toronto, Ontario, Canada"),
        (6, "Sabrina Carpenter", "Pop",      "Quakertown, Pennsylvania"),
    ]
    conn.executemany("INSERT OR IGNORE INTO Artist VALUES (?, ?, ?, ?)", artists)

    tracks = [
        (1,  "Style",                231, 1),
        (2,  "The Fate of Ophelia",  226, 1),
        (3,  "Fortnight",            228, 1),
        (4,  "One Last Time",        197, 2),
        (5,  "Dangerous Woman",      235, 2),
        (6,  "Side To Side",         226, 2),
        (7,  "Lovely",               200, 3),
        (8,  "Ocean Eyes",           200, 3),
        (9,  "TV",                   281, 3),
        (10, "Sign of the Times",    340, 4),
        (11, "American Girls",       213, 4),
        (12, "As It Was",            167, 4),
        (13, "Starboy",              230, 5),
        (14, "Blinding Lights",      200, 5),
        (15, "The Hills",            242, 5),
        (16, "Espresso",             175, 6),
        (17, "Manchild",             213, 6),
        (18, "Please Please Please", 186, 6),
    ]
    conn.executemany("INSERT OR IGNORE INTO Track VALUES (?, ?, ?, ?)", tracks)

    playlists = [
        (1, "Late Night Vibes", "Group2"),
        (2, "Workout Hits",     "Group2"),
        (3, "Chill Pop",        "Group2"),
        (4, "Party Anthems",    "Group2"),
    ]
    conn.executemany("INSERT OR IGNORE INTO Playlist VALUES (?, ?, ?)", playlists)

    playlist_tracks = [
        (1,  1, 1),
        (1,  7, 2),
        (1,  8, 3),
        (1, 13, 4),
        (1, 15, 5),
        (1,  4, 6),
        (2, 14, 1),
        (2, 16, 2),
        (2,  6, 3),
        (2, 12, 4),
        (2,  3, 5),
        (3, 17, 1),
        (3,  9, 2),
        (3,  2, 3),
        (3, 11, 4),
        (3,  5, 5),
        (4, 10, 1),
        (4, 18, 2),
        (4,  1, 3),
        (4, 13, 4),
    ]
    conn.executemany("INSERT OR IGNORE INTO PlaylistTrack VALUES (?, ?, ?)", playlist_tracks)

    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect(':memory:')
    build_database(conn)
    seed_database(conn)

    try:
        conn.execute('INSERT INTO Track VALUES (99, "Ghost Track", 210, 9999)')
    except sqlite3.IntegrityError as e:
        print(f'IntegrityError caught: {e}')

    target = sqlite3.connect('music.db')
    conn.backup(target)
    target.close()
    conn.close()
    print('Database written to music.db')