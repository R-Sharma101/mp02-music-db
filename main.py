import sqlite3
# from schema_data import build_database, seed_database
# from queries import get_playlist_tracks, get_tracks_on_no_playlist
# from queries import get_most_added_track, get_playlist_durations

def main():
    # TODO: startup sequence (check if music.db exists)
    
    while True:
        print("\n=== Pop Music Playlist Manager ===")
    print("1. View tracks on a playlist")
    print("2. View tracks not on any playlist")
    print("3. Most added track")
    print("4. Playlist durations")
    print("5. Delete an artist")
    print("0. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "0":
            break
        # TODO: handle other options

if __name__ == "__main__":
    main()