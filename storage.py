import sqlite3

class StorageException(Exception):
    def __init__(self, arg):
        self.message = arg

class WriteError(StorageException):
    pass

def setup():
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS projects (id integer primary key, name text)')
    c.execute('''CREATE TABLE IF NOT EXISTS activities (id integer primary key, project_id integer NOT NULL, name text, FOREIGN KEY (project_id) REFERENCES projects(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS workdays (project_id integer NOT NULL, number_of_hours integer NOT NULL, date date, activity_id integer NOT NULL, FOREIGN KEY (project_id) REFERENCES projects(id), FOREIGN KEY (activity_id) REFERENCES activities(id))''')
    connection.commit()
    connection.close()

def add_project(project, success_callback):
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    try:
        if project_exists(project):
            print "Project exists, foo"
            return
        t = (project,)
        c.execute('INSERT INTO projects (name) VALUES (?)', t)
        connection.commit()
        success_callback()
    except sqlite3.OperationalError:
        raise WriteError("Error writing data")
    except TypeError:
        pass
    finally:
        connection.close()

def list_projects():
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    for row in c.execute('SELECT * FROM projects'):
        print row[1]

def set_hours(hours, project, date):
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    #Get project id from name
    #Update workdays with hours where id=x and date=y

def get_project_id(project):
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    t = (project + "%",)
    for row in c.execute('SELECT * FROM projects WHERE name LIKE ?', t):
        print row

def project_exists(project):
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    t = (project,)
    c.execute('SELECT * FROM projects WHERE name LIKE ?', t)
    response = c.fetchall()
    return len(response) > 0
