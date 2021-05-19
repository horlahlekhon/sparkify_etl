import glob
import logging
import os
from logging import Logger
from pathlib import Path
from typing import Callable, Union

import pandas as pd
import psycopg2
from psycopg2.extensions import connection, cursor

from sql_queries import *


class ETL:

    def __init__(self, connection: connection, data_directory: Path, logger: Logger):
        self._conn: connection = connection
        self._cursor: Union[cursor, None] = None
        self.data_dir = data_directory
        self.log: Logger = logger

    @classmethod
    def _process_song_file(cls, _cursor: cursor, filepath):
        """
            Load a given song json file and insert the data in the  database
        :param filepath: path to the json file
        """
        # open song file
        df = pd.read_json(filepath, lines=True)

        # insert artist record
        artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[
            0]
        _cursor.execute(artist_table_insert, artist_data)

        # insert song record
        song_data = df[["title", "artist_id", "duration", "year"]].values[0]
        _cursor.execute(song_table_insert, song_data)

    @classmethod
    def _process_log_file(cls, _cursor: cursor, filepath):
        """
            Load a given log json file
             filter out logs that doesnt  describe any song. then
              extract data to be used to create user and songplays records
        :param filepath: path to the json file
        """
        # open log file
        df = pd.read_json(filepath, lines=True)

        # filter by NextSong action
        is_next_song = df["page"] == "NextSong"
        df = df[is_next_song]

        # convert timestamp column to datetime
        t = df["ts"].apply(lambda x: pd.Timestamp(x, unit='ms'))

        # insert time data records
        time_data = [[i, i.hour, i.day, i.week, i.month, i.year, i.weekday()] for i in t]
        column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
        time_df = pd.DataFrame(time_data, columns=column_labels)

        for i, row in time_df.iterrows():
            _cursor.execute(time_table_insert, list(row))

        # load user table
        user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

        # insert user records
        for i, row in user_df.iterrows():
            _cursor.execute(user_table_insert, row)

        # insert songplay records
        for index, row in df.iterrows():

            # get songid and artistid from song and artist tables
            _cursor.execute(song_select, (row.song, row.artist, row.length))
            results = _cursor.fetchone()

            if results:
                artistid, songid = results
            else:
                artistid, songid = None, None

            # insert songplay record
            songplay_data = (
                pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location,
                row.userAgent)
            _cursor.execute(songplay_table_insert, songplay_data)

    def _process_data(self, filepath: Path, func: Callable):
        """
            traverse the given directory tree and find and collect json files to process.
             then iterate through the files and call `func` on each file passing
              the current db connection cursor to it
        :param filepath: directory to search for files from
        :param func: processing function
        """
        # get all files matching extension from directory
        all_files = []
        for root, dirs, files in os.walk(filepath):
            files = glob.glob(os.path.join(root, '*.json'))
            for f in files:
                all_files.append(os.path.abspath(f))

        # get total number of files found
        num_files = len(all_files)
        self.log.info('{} files found in {}'.format(num_files, filepath))

        # iterate over files and process
        for i, datafile in enumerate(all_files, 1):
            func(self._cursor, datafile)
            self._conn.commit()
            self.log.info('{}/{} files processed... processing: {}'.format(i, num_files, datafile.split("/")[-1]))

    def process(self):
        try:
            self._cursor = self._conn.cursor()
            print(type(self._cursor))
        except Exception as reason:
            self.log.exception(f"an error occured while trying to connect to database: {reason}")
        self._process_data(filepath=self.data_dir / "song_data", func=ETL._process_song_file)
        self._process_data(filepath=self.data_dir / 'log_data', func=ETL._process_log_file)
        self._conn.close()


if __name__ == "__main__":
    connection = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    data_dir = Path('data')
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)
    assert data_dir.is_dir(), "Please provide a valid directory"
    etl = ETL(connection, data_dir, logger)
    etl.process()
