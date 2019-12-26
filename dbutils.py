import sqlite3


def check_file(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
        print('SQLite DB found, version {}'.format(sqlite3.version))
        return conn
    except Error as e:
        print('Connection failed with error: '.format(e))
        return False
    finally:
        if conn:
            print('Closing DB for now')
            conn.close()


def check_tables(dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute("SELECT * FROM test;")
        data = c.fetchone()
        if data is None:
            if createdb(dbfile):
                return True
            else:
                return False
        else:
            return False
    except Error as e:
        print(e)
        return False


def createdb(dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute('''CREATE TABLE test (name TEXT, number REAL);''')
        c.execute('''CREATE TABLE songs (id INTEGER PRIMARY KEY, url TEXT, user TEXT, datetime TEXT);''')
        c.execute('''CREATE TABLE memes (id INTEGER PRIMARY KEY, filename TEXT, user TEXT, datetime TEXT)''')
        c.execute('''INSERT INTO test values ('A', '1');''')
        conn.close()
        return True
    except Error as e:
        print(e)
        return False


def select(query, dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute(query)
        data = c.fetchall()
        if data is None:
            return False
        else:
            return data
    except Error as e:
        print(e)
        return False


def addsong(ytlink, user, dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute("INSERT INTO test values (?, ?, DateTime('now'))", (ytlink, user))
        conn.close()
        return True
    except Error as e:
        print('Error in inserting URL: '.format(ytlink))
        print(e)
        return False


def addMemeTemplate(filename, user, dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute("INSERT INTO memes VALUES (?, ?, DateTime('now'))", (filename, user))
        conn.close()
        return True
    except Error as e:
        print(e)
        return False
