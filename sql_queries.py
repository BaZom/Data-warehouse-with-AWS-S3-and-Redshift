import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events CASCADE"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs CASCADE"
songplay_table_drop = "DROP TABLE IF EXISTS songplays CASCADE"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE"
time_table_drop = "DROP TABLE IF EXISTS time CASCADE"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (\
                                Staging_event_id INT IDENTITY(0,1),\
                                artist VARCHAR,\
                                auth VARCHAR,\
                                firstName VARCHAR,\
                                gender CHAR,\
                                itemInSession INT,\
                                lastName VARCHAR,\
                                length DOUBLE PRECISION,\
                                level VARCHAR,\
                                location VARCHAR(500),\
                                method VARCHAR,\
                                page VARCHAR,\
                                registration DOUBLE PRECISION,\
                                sessionId INT,\
                                song VARCHAR,\
                                status INT,\
                                ts bigint,\
                                userAgent VARCHAR,\
                                userId VARCHAR,\
                                PRIMARY KEY (stating_event_id));""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (\
                                Staging_song_id INT IDENTITY(0,1),\
                                artist_id VARCHAR,\
                                artist_latitude VARCHAR,\
                                artist_location VARCHAR(500),\
                                artist_longitude VARCHAR,\
                                artist_name VARCHAR,\
                                duration NUMERIC,\
                                num_songs INT,\
                                song_id VARCHAR,                            
                                title VARCHAR,\
                                year INT,\
                                PRIMARY KEY (stating_song_id));""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (\
                            songplay_id INT IDENTITY(0,1),\
                            start_time TIMESTAMP not null,\
                            user_id VARCHAR NOT NULL distkey,\
                            user_level VARCHAR,\
                            song_id VARCHAR NOT NULL,\
                            artist_id VARCHAR NOT NULL,\
                            session_id INT NOT NULL,\
                            location VARCHAR(500),\
                            user_agent TEXT,\
                            PRIMARY KEY (songplay_id),
                            FOREIGN KEY(user_id) REFERENCES users(user_id),\
                            FOREIGN KEY(song_id) REFERENCES songs(song_id),\
                            FOREIGN KEY(artist_id) REFERENCES artists(artist_id),\
                            FOREIGN KEY(start_time) REFERENCES time(start_time));""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (\
                        user_id VARCHAR sortkey,\
                        user_first_name VARCHAR,\
                        user_last_name VARCHAR,\
                        user_gender CHAR,\
                        user_level VARCHAR,\
                        PRIMARY KEY (user_id));""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (\
                        song_id VARCHAR sortkey,\
                        song_title VARCHAR NOT NULL,\
                        artist_id VARCHAR NOT NULL,\
                        year INT NOT NULL,\
                        duration numeric NOT NULL,\
                        PRIMARY KEY (song_id));""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (\
                        artist_id VARCHAR sortkey,\
                        name VARCHAR,\
                        location VARCHAR(500),\
                        artist_latitude VARCHAR,\
                        artist_longitude VARCHAR,\
                        PRIMARY KEY (artist_id));""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(\
                        start_time TIMESTAMP sortkey,\
                        hour INT,\
                        day INT,\
                        week INT,\
                        month INT,\
                        year INT,\
                        weekday INT,\
                        PRIMARY KEY (start_time));""")

# STAGING TABLES


staging_events_copy = ("""copy staging_events 
                          from {}
                          iam_role {}
                          json {}
                          timeformat as 'auto';
                       """).format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs 
                          from {} 
                          iam_role {}
                          json 'auto'
                          compupdate off
                          region 'us-west-2';
                      """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, user_level, song_id, artist_id, session_id, location, user_agent)\
                                                SELECT\
                                                TIMESTAMP 'epoch' + (st_events.ts/1000 * INTERVAL '1 second') as start_time,\
                                                st_events.userId,\
                                                st_events.level,\
                                                st_songs.song_id,\
                                                st_events.artist,\
                                                st_events.sessionId,\
                                                st_events.location,\
                                                st_events.userAgent\
                                                From staging_events st_events, staging_songs st_songs\
                                                WHERE st_events.song = st_songs.title\
                                                AND st_events.artist = st_songs.artist_name
                                                AND st_events.page = 'NextSong'""")

user_table_insert = ("""INSERT INTO users (user_id, user_first_name, user_last_name, user_gender, user_level)\
                                        SELECT distinct userId,\
                                        firstName,\
                                        lastName,\
                                        gender,\
                                        level\
                                        FROM staging_events""")

song_table_insert = ("""INSERT INTO songs (song_id, song_title, artist_id, year, duration)\
                                        SELECT distinct song_id,\
                                        title,\
                                        artist_id,\
                                        year,\
                                        duration\
                                        FROM staging_songs""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, artist_latitude, artist_longitude)\
                                            SELECT distinct artist_id,\
                                            artist_name,\
                                            artist_location,\
                                            artist_latitude,\
                                            artist_longitude\
                                            FROM staging_songs""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)\
        WITH temp_time AS (SELECT TIMESTAMP 'epoch' + (ts/1000 * INTERVAL '1 second') as ts FROM staging_events)
        SELECT DISTINCT
        ts,
        extract(hour from ts),
        extract(day from ts),
        extract(week from ts),
        extract(month from ts),
        extract(year from ts),
        extract(weekday from ts)
        FROM temp_time
                                        """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
