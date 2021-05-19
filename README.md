Sparkify Data modeling and ETL

This project performs etl and create data schema for easy querying of song data insights based on logged activities of
users logged in json format. we perform etl pipelines on each logfile extract data and insert into the database in form
of a star schema.

#### Project objective

The company will like to have analysis on the behaviours of the users in relation to songs that they hear on the
streaming application. and while all data are being dumped in log files, that proven difficult. so the purpose of this
project is to create etls and a database that filters and clean the data from the logs as well as a database that put
the data into analytical perspective where business decisions can be easily made, and dashboards generated from
available data which would have proven difficult with log files.

#### The Schema

The Star schema components consists of four dimension tables and a fact table which generate aggregates in relation to
the dimension tables

Dimension tables:

`songs_table`: holds song data gottten from song_data logs which logs all songs that was listened. it is presented as a
json object that incudes fields required to generate enough insight into what music was listed to and by ehat artist and
duration of play

`users`: holds user data which can help when finding which user listens to a particular song.

`artists`: holds data relatting to individual artists that made a music.

`time`: provides a broken down dimension of each timestamp in the logs including hours, days and months

Fact table:

`songplays`: this table draw from each of the dimension tables to generate an insight into what song is being played.
with this table one can easily get aggregates information about the songs, artists, locations e.t.c

this table will allow us to see data about a user,

* songs they listened to
* the location where we have most users are listening to songs
  ```sql
    select location,  count(location) as listened_times from songplays group by user_id, location order by listened_times desc
    ```
  <!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta charset="UTF-8">
  </head>
<body>
<table border="1" style="border-collapse:collapse">
<tr>
  <th>location</th>
  <th>listened_times</th>
</tr>
<tr>
  <td>San Francisco-Oakland-Hayward, CA</td>
  <td>502</td>
</tr>
<tr>
  <td>Portland-South Portland, ME</td>
  <td>485</td>
</tr>
<tr>
  <td>Waterloo-Cedar Falls, IA</td>
  <td>337</td>
</tr>
<tr>
  <td>Chicago-Naperville-Elgin, IL-IN-WI</td>
  <td>331</td>
</tr>
<tr>
  <td>Birmingham-Hoover, AL</td>
  <td>219</td>
</tr>
</table>
</body>
</html>

```shell

```
* what music does paid and/or free users listened to the most and by which artist
  ```sql
    select song_id, artist_id, count(song_id) from songplays where level = 'paid' group by song_id, artist_id
    ```
* where do we have most free and/or paid users.
    ```sql
    select location, count(location) from songplays where level = 'free | paid' group by location 
    ```
  <!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta charset="UTF-8">
  </head>
<body>
<table border="1" style="border-collapse:collapse">
<tr>
  <th>location</th>
  <th>count</th>
</tr>
<tr>
  <td>San Jose-Sunnyvale-Santa Clara, CA</td>
  <td>78</td>
</tr>
<tr>
  <td>Yuba City, CA</td>
  <td>23</td>
</tr>
<tr>
  <td>Saginaw, MI</td>
  <td>3</td>
</tr>
<tr>
  <td>Nashville-Davidson--Murfreesboro--Franklin, TN</td>
  <td>15</td>
</tr>
<tr>
  <td>San Diego-Carlsbad, CA</td>
  <td>4</td>
</tr>
</table>
</body>
</html>

* who listened to music the most over a period of time(`2018-11-01` to `2018-11-23`) based on paid level or free level
  and their location.
    ```sql
        select user_id, location, count(user_id) from songplays where start_time >= '2018-11-01' and start_time <= '2018-11-23' and level = 'free | paid'  group by user_id, location
    ```
  <!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta charset="UTF-8">
  </head>
<body>
<table border="1" style="border-collapse:collapse">
<tr>
  <th>user_id</th>
  <th>location</th>
  <th>count</th>
</tr>
<tr>
  <td>3</td>
  <td>Saginaw, MI</td>
  <td>3</td>
</tr>
<tr>
  <td>6</td>
  <td>Atlanta-Sandy Springs-Roswell, GA</td>
  <td>2</td>
</tr>
<tr>
  <td>8</td>
  <td>Phoenix-Mesa-Scottsdale, AZ</td>
  <td>7</td>
</tr>
<tr>
  <td>10</td>
  <td>Washington-Arlington-Alexandria, DC-VA-MD-WV</td>
  <td>7</td>
</tr>
<tr>
  <td>16</td>
  <td>Birmingham-Hoover, AL</td>
  <td>5</td>
</tr>
</table>
</body>
</html>

* what hour of the day do users listened to songs the mostt
    ```sql
    select extract(hour from start_time) as hour, count(start_time) from songplays group by extract(hour from songplays.start_time)
    ```
<!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta charset="UTF-8">
  </head>
<body>
<table border="1" style="border-collapse:collapse">
<tr>
  <th>hour</th>
  <th>count</th>
</tr>
<tr>
  <td>0</td>
  <td>132</td>
</tr>
<tr>
  <td>19</td>
  <td>230</td>
</tr>
<tr>
  <td>8</td>
  <td>128</td>
</tr>
<tr>
  <td>5</td>
  <td>102</td>
</tr>
<tr>
  <td>13</td>
  <td>204</td>
</tr>
</table>
</body>
</html>

#### ETL

##### Song and arists data

Song log files are stored in nested directories that consists of detailed logs about a song listened to, and is
structured in such a way that each file constains a single log line of a song listed to, with
> the artist of the  song,
>
> the duration of the song,
>
> location of the artists in geo points,
>
> the title
>
> of the song and the  year it was made.

##### Users, session  info about who played song and at what time song is being  played

this data is also presented in nested log directories with each file representing logs of events that happened in the
song streaming application. this log can give us
> when the particular song was listed to as well as detail of the song listened to,
>
> details of the logged in user listening  to the song, including location data
>
> user agent of the client connected to the streaming service
>

with this we can do much, butt the data is dirty because its a a kind of http logs of events so it includes details of
the response and what page made the request.

##### The process

With the above data, we create a two functions that takes log file and does etl on the two log files.
`process_song_file` : processes a single song log file
`process_log_file` : processes a single streaming app http log data

At the top level we have a `process_data` function that takes a directory and a function, where the directory is where
logs are stored and function is any function able to process the data in the corresponding directory. we then just glob
through the directory given to flatten the files to a single list of json filepaths and then pass it inn turn to the
processing function.

###### process_song_file

Song files are quite straight forward as hey provide data in this format

```json
{
  "num_songs": 1,
  "artist_id": "ARD7TVE1187B99BFB1",
  "artist_latitude": null,
  "artist_longitude": null,
  "artist_location": "California - LA",
  "artist_name": "Casual",
  "song_id": "SOMZWCG12A8C13C480",
  "title": "I Didn't Mean To",
  "duration": 218.93179,
  "year": 0
}
```

so extracting sonng and artist details was easy and we just insert the data into the database straight away.

###### process_log_file

```json
{
  "artist": "Godsmack",
  "auth": "Logged In",
  "firstName": "Lily",
  "gender": "F",
  "itemInSession": 5,
  "lastName": "Koch",
  "length": 208.24771,
  "level": "paid",
  "location": "Chicago-Naperville-Elgin, IL-IN-WI",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1541048010796.0,
  "sessionId": 172,
  "song": "Greed",
  "status": 200,
  "ts": 1541150355796,
  "userAgent": "\"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Ubuntu Chromium\/36.0.1985.125 Chrome\/36.0.1985.125 Safari\/537.36\"",
  "userId": "15"
}

```

Due to log files being dirty we had to somewhat clean it first by filtering out log lines that doesn't refer to songs,
using the `page` attribute which is used to denote which page the application made the request from, typically we only
want lines that has `page` == `NextSong`. After filtering out the other pages, we extracted the `ts` field which can
give us all the information we need regarding the `time` table; we extract and sort of expand each timestamp to give us
details of the day including hour, weekday, month and year.

In this log file we also get all required data for the users information without hassle and insert them into database.
lastly we needed to insert data about the playing of songs in the songplay table, so we made query on the `artists`
and `songs` table to get song_id and artist_id given the "artist" and "song"
attribute of each log lines to be used to prove integrity of songs being played if it exist on the artists and song
table.



### How to run

##### Create virtual env and install dependencies

```shell
  virtualenv --python python3 venv
  source venv/bin/activate
  pip install psycopg2-binary pandas ipython[all]
```

##### Run
To run the project we will have to run the create tables queries first, which exists in 
`create_tables.py`
```shell
  python create_tables.py
```

after the create table scrip has run successfully, we can then run the `etl.py` to clean the data, create tables and populate tables

```shell
  python etl.py
```

#### Files
`sql_queries.py` : define create table and insert table queries

`create_tables.py`: script for  create tthe database and dropping. it basically connect to the db and run queries specified in `sql_queries.py`

`etl.py`: script for running etl, defines logic for cleaninng  data and inserting cleaned data into database.

`test.ipynb`: Notebook for testing database inserted data

`etl.ipynb`: Notebook for detailing the etl process  step by step



Thanks.


