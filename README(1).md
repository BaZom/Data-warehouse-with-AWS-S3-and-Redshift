Useful Queries:

For Stating tables:
SELECT page, * FROM "dev"."public"."staging_events" where page = 'NextSong';
SELECT * FROM "dev"."public"."staging_songs";
SELECT count(*) FROM "dev"."public"."staging_events" where page = 'NextSong';
SELECT count(*) FROM "dev"."public"."staging_songs";

For star schema:
SELECT * FROM "dev"."public"."songplays";

Why user_id as distkey:
SELECT song_id, count(*) as county FROM "dev"."public"."songplays"group by song_id order by county DESC;
SELECT user_id, count(*) as county FROM "dev"."public"."songplays"group by user_id order by county DESC;

affectes of not working primary key
SELECT song_id, count(*) as county  FROM "dev"."public"."songs" group by song_id order by county DESC;
SELECT artist_id, count(*) as county FROM "dev"."public"."artists" group by artist_id order by county DESC;
SELECT * FROM "dev"."public"."artists" where artist_id = 'ARTE9CG1187B99B1AF';

some data are weird
SELECT * FROM "dev"."public"."users" where user_id = '';


SELECT * FROM "dev"."public"."time";

Other queries:
SELECT st_events.song, st_songs.title, st_events.artist, st_songs.artist_name
                                                From staging_events st_events, staging_songs st_songs
                                                WHERE st_events.song = st_songs.title
                                                AND st_events.artist = st_songs.artist_name
                                                AND st_events.page = 'NextSong';

SELECT distinct artist_id,* FROM staging_songs where artist_id = 'ARTE9CG1187B99B1AF'; # Primary key does not work in redshift

select * from stl_load_errors;