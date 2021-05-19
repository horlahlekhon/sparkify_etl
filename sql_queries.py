# DROP TABLES

songplay_table_drop = """DROP TABLE IF EXISTS songplays"""
user_table_drop = """DROP TABLE IF EXISTS users"""
song_table_drop = """DROP TABLE IF EXISTS songs"""
artist_table_drop = """DROP TABLE IF EXISTS artists"""
time_table_drop = """DROP TABLE IF EXISTS time"""

# CREATE TABLES

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY ,
                                    first_name VARCHAR, 
                                        last_name VARCHAR, gender VARCHAR,
                                         level VARCHAR)
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR PRIMARY KEY , name VARCHAR, location VARCHAR,
                                        latitude DOUBLE PRECISION, longitude DOUBLE PRECISION
                                         )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (song_id SERIAL PRIMARY KEY ,
                                    title VARCHAR, artist_id VARCHAR, year INTEGER, duration DOUBLE PRECISION,
                                    CONSTRAINT fk_artist_id
                                        FOREIGN KEY(artist_id) REFERENCES artists(artist_id) ON DELETE SET NULL
                                        )
""")

time_table_create = ("""
        CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP WITHOUT TIME ZONE, hour INTEGER,
         day INTEGER, week INTEGER, month INTEGER, year INTEGER, weekday INTEGER)
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING 
""")

user_table_insert = ("""
    INSERT INTO users(user_id, first_name, last_name, gender, level)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING 
""")

song_table_insert = ("""
        INSERT INTO songs(title, artist_id, duration, year)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING 
""")

artist_table_insert = ("""
        INSERT INTO artists(artist_id, name, location, latitude, longitude) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING 
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING 
""")

# FIND SONGS

song_select = ("""
        SELECT a.artist_id, songs.song_id FROM songs 
        JOIN artists a ON songs.artist_id = a.artist_id 
            WHERE songs.title = %s AND  a.name = %s AND songs.duration = %s
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY , 
                                            start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL, user_id INTEGER NOT NULL ,
                                            level VARCHAR, song_id INTEGER DEFAULT NULL, artist_id VARCHAR DEFAULT NULL,
                                            session_id INTEGER, location VARCHAR, user_agent VARCHAR,
                                            CONSTRAINT fk_song_id
                                                FOREIGN KEY(song_id) REFERENCES songs(song_id) ON DELETE SET NULL,
                                            CONSTRAINT fk_artist_id
                                                FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE SET NULL 
                                            )
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, time_table_create, song_table_create,
                        songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
