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
            print('Closing DB file')
            conn.close()


def check_tables(dbfile):
    if select('''SELECT * FROM test;'''):
        return True
    else:
        return False


def createdb():
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE test (name TEXT, number REAL);''')
        c.execute('''CREATE TABLE songs (id INTEGER PRIMARY KEY, url TEXT, user TEXT, datetime TEXT);''')
        c.execute('''INSERT INTO test values ('A', '1');''')
        return True
    except Error as e:
        return False


def select(query):
    c = conn.cursor()
    c.execute(query)
    data = c.fetchone()
    if data is None:
        print('DB not created')
        createdb()
    else:
        pass


def addsong(ytlink, user):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO test values (ytlink, user, DateTime('now'))''')
    except Error as e:
        print('Error in inserting URL: '.format(ytlink))

