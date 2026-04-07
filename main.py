import sqlite3
import os
from schema_data import build_database, seed_database
from queries import get_playlist_tracks, get_tracks_on_no_playlist
from queries import get_most_added_track, get_playlist_durations

def format_duration(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

def delete_artist(conn):
    artist_id = input("Enter artist ID to delete: ")
    try:
        conn.execute("""
            DELETE FROM PlaylistTrack
            WHERE track_id IN (
                SELECT track_id FROM Track WHERE artist_id = ?
            )""", (artist_id,))
        conn.execute("DELETE FROM Track WHERE artist_id = ?", (artist_id,))
        conn.execute("DELETE FROM Artist WHERE artist_id = ?", (artist_id,))
        conn.commit()
        print(f"Artist {artist_id} and all dependent records removed.")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"Deletion failed: {e}")

def main():
    if os.path.exists("music.db"):
        conn = sqlite3.connect("music.db")
        print("Re-opening existing music.db...")
    else:
        print("First run — building database...")
        conn = sqlite3.connect(":memory:")
        build_database(conn)
        seed_database(conn)
        target = sqlite3.connect("music.db")
        conn.backup(target)
        target.close()
        conn = sqlite3.connect("music.db")
        print("Database built and saved to music.db.")

    while True:
        print("\n=== Pop Music Playlist Manager ===")
        print("1. View tracks on a playlist")
        print("2. View tracks not on any playlist")
        print("3. Most added track")
        print("4. Playlist durations")
        print("5. Delete an artist")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter playlist name: ")
            rows = get_playlist_tracks(conn, name)
            if not rows:
                print("No tracks found.")
            else:
                print(f"\n{'Pos':<5}{'Title':<30}{'Artist':<25}{'Duration'}")
                print("-" * 65)
                for title, artist, duration, pos in rows:
                    print(f"{pos:<5}{title:<30}{artist:<25}{format_duration(duration)}")

        elif choice == "2":
            rows = get_tracks_on_no_playlist(conn)
            if not rows:
                print("All tracks are on at least one playlist.")
            else:
                print(f"\n{'Title':<30}{'Artist'}")
                print("-" * 50)
                for track_id, title, artist in rows:
                    print(f"{title:<30}{artist}")

        elif choice == "3":
            row = get_most_added_track(conn)
            if row:
                title, artist, count = row
                print(f"\nMost added track: {title} by {artist} ({count} playlists)")

        elif choice == "4":
            rows = get_playlist_durations(conn)
            print(f"\n{'Playlist':<25}{'Total Duration'}")
            print("-" * 40)
            for name, minutes in rows:
                total_seconds = int(minutes * 60)
                print(f"{name:<25}{format_duration(total_seconds)}")

        elif choice == "5":
            delete_artist(conn)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

    conn.close()

if __name__ == "__main__":
    main()