#!/usr/bin/env python3
"""
Author: Arthur H. Gould
Email: gould.arthur@outlook.com
Date: 2024-03-07

Data citation:
        Bonica, Adam, 2015, "Database on Ideology, Money in Politics, and Elections (DIME)",
        https://doi.org/10.7910/DVN/O5PX0B, Harvard Dataverse, V3
"""
# minimizing imports as much as possible
from requests import get as req_get
from sqlite3 import connect
from gzip import open as gz_open

FIELDS = {"amount": "INTEGER", "bonica_cid": "INTEGER", "contributor_cfscore": "FLOAT",
          "candidate_cfscore": "FLOAT"}


URLS = {1980: "OQQ2NW",
        1982: "CUDWEU",
        1984: "WDLQE5",
        1986: "JFDKGE",
        1988: "MFUNX4",
        1990: "02KGNE",
        1992: "1AVELD",
        1994: "ASO5KB",
        1996: "61ZNPR",
        1998: "N8YSBZ",
        2000: "M3BZUP",
        2002: "T4PHDD",
        2004: "JV6KYR",
        2006: "I01NT6",
        2008: "JHLIEZ",
        2010: "NXTDHV",
        2012: "YQGIZJ",
        2014: "HDZZO7"}


DATE_TO_URLS = lambda year: f"https://dataverse.harvard.edu/api/access/"\
                            f"datafile/:persistentId?persistentId=doi:10.7910/DVN/O5PX0B/{URLS[year]}"


TABLES_MAP = {
    "Transactions": [1, 0, 2, 3, 4, 5, 23],
    "Contributor_Org": [5, 6, 44, 15, 21],  # still need location id from that table
    "Contributor_Indv": [5, 6, 44, 15, 7, 8, 9, 10, 11, 12, 14, 19, 20, 32, 33, 34],  # above and this determined by element 13
    "Recipient": [23, 22, 24, 25, 26, 27, 28, 31]
    # "Location": [17, 16, 18]  # need to add an id
}


MAPPED_STRING = dict()
for key in TABLES_MAP.keys():
    MAPPED_STRING[key] = "?, " * TABLES_MAP[key].__len__()
    MAPPED_STRING[key] = MAPPED_STRING[key][:-2]  # chop trailing ','


class Populator:
    """
    Responsible for populating a database.


    Args:
        database_name: str      - the database to which the Populator will create/connect.
                                    Default: "base_populated.db"
        forced_download: bool   - determines whether the zipped data will be downloaded should
                                    it already exit. Default: False

    Raises:
        ConnectionError:        - Occures when attempting to download gzip data returns code
                                    signifying Non-success
    """

    def __init__(self, database_name: str = "base_populated.db",
                 ignore_existing: bool = False, lower_memory: bool = False):
        self._database_name = database_name
        self._force_download = ignore_existing
        self._low_memory = lower_memory


    def populate(self, year: int) -> None:
        """
        Creates and populations a database given a year

        Args:
            year: int           - the year of data to download
        """
        filename = f"data_{year}.gz"
        if self._check_if_download(filename):
            self._download_data(year, filename)
        with gz_open(filename, "r") as fd:
            lines = fd.readline().decode('utf-8')
            column_number = self._create_table(lines)
            lines = fd.readlines(5000 if self._low_memory else -1)
            while lines:
                self._insert_data(column_number, lines)
                lines = fd.readlines(5000 if self._low_memory else -1)
 

    def _check_if_download(self, filename: str) -> bool:
        """
        Determines if a given filename should be downloaded

        Args:
            filename: str       - the filename for which to check

        Returns:
            (bool)              - True if file should be downloaded, False otherwise
        """
        if self._force_download:
            return True
        try:
            fd = open(filename, 'r')  # if it can open to read, then it exists
            fd.close()
            return False
        except FileNotFoundError:
            return True

    def _create_table_old(self, data: str, table_name: str = "DONATIONS") -> int:
        """
        Creates a table in the opened database

        Args:
            data: str           - the first line of a csv, signifying the column names
            table_name: str     - determines what the table will be names. Default: "DONATIONS"
        """
        cols = []
        for col in data.split(','):
            col = col.replace('"', '').replace(".", "_").strip()
            cols.append(f"{col} {FIELDS.get(col, 'TEXT')}")
        column_number = len(cols)
        cols = ', '.join(cols)
        self._cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({cols})")
        return column_number

    def _create_table(self, data: str, table_name: str = "DONATIONS") -> int:
        """
        Creates a table in the opened database

        Args:
            data: str           - the first line of a csv, signifying the column names
            table_name: str     - determines what the table will be names. Default: "DONATIONS"
        """
        cols = []
        for col in data.split(','):
            col = col.replace('"', '').replace(".", "_").strip()
            cols.append(f"{col} {FIELDS.get(col, 'TEXT')}")

        for table in TABLES_MAP.keys():
            data = [cols[i] for i in TABLES_MAP[table]]
            data[0] = data[0] + " PRIMARY KEY"
            insert_data = ', '.join(data)
            self._cur.execute(f"CREATE TABLE IF NOT EXISTS {table}({insert_data})")



    def _download_data(self, year: int, filename: str) -> None:
        """
        Downloads a gzipped file given a year and stores file to filename

        Args:
            year: int           - the year for which to download data
            filename: str       - name for which to store the file

        Raises:
            KeyError:           - Occures when an invalid or unsupported year is passed
            ConnectionError     - Occures when gzipped file fails to download
        """
        result = req_get(DATE_TO_URLS(year), stream=True)
        if result.status_code > 299:
            raise ConnectionError(f"Cannot Download information for year {year}")
        with open(filename, "wb") as fd:
            fd.write(result.content)

    def _clean_data(self, data: list) -> None:
        """
        Parses and cleans data for ingestion

        data: list[byte like]   - a list of bytelike objects to be cleaned
        """
        for i in range(len(data)):
            data[i] = data[i].decode("utf-8").replace("\" ", "").replace("\"", "").\
                strip().replace(", ", ". ").split(',')

    def _insert_data(self, column_number: int, data: list, table_name: str = "DONATIONS"):
        """
        Inserts data into database, under given table

        Args:
            column_number: int      - number of columns in the table
            data: list[byte-like]   - a bytelike list containing. Each element is a row
                                        to enter into the database
            table_name: str         - the table underwhich to enter the data.
                                        Default: "DONATIONS
        """

        self._clean_data(data)


        bad_data = []
        good_data = {i: [] for i in TABLES_MAP.keys() }



        for i in range(len(data)):
            if len(data[i]) != 46:
                bad_data.append(f"Malformed Data: ::: {data[i]} :::\n")
                continue
            for key in TABLES_MAP.keys():
                if key == "Contributor_Indv" and data[i][13] == "C":  # skip adding indv. cont. if contributor was org.
                    continue
                if key == "Contributor_Org" and data[i][13] != "C":  # skip adding org. cont. if contributor was indv.
                    continue
                self._cur.execute(f"INSERT OR IGNORE INTO {key} VALUES ({MAPPED_STRING[key]})",
                                  [data[i][j] for j in TABLES_MAP[key]])

        with open("malformed.log", "w") as err_log:
            err_log.writelines(bad_data)

        #self._cur.executemany(f"INSERT OR IGNORE INTO {table_name} VALUES ({values[:-1]})", good_data)



    def __open__(self):

        self._con = connect(self._database_name) if self._low_memory else connect(":memory:")
        self._cur = self._con.cursor()

    def __close__(self):
        self._con.commit()
        if not self._low_memory:
            disk_db = connect(self._database_name)
            with disk_db:
                self._con.backup(disk_db)
        self._con.close()
        self._con = None

    def __enter__(self):
        self.__open__()
        return self

    def __exit__(self, e_type, e_value, e_trace):
        # Exceptions not handles for version 1
        return self.__close__()

    def open(self):
        return self.__open__()

    def close(self):
        return self.__close__()
