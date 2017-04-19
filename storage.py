import sqlite3
import dates as datesmod

class StorageException(Exception):
    def __init__(self, arg):
        self.message = arg

class WriteError(StorageException):
    pass

class NonExistentProjectError(StorageException):
    pass

class NoWorkdaysForDateError(StorageException):
    pass

def setup():
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS projects (id integer primary key, name text)')
    c.execute('''CREATE TABLE IF NOT EXISTS activities (id integer primary key, project_id integer NOT NULL, name text, FOREIGN KEY (project_id) REFERENCES projects(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS workdays (project_id integer NOT NULL, number_of_hours integer NOT NULL, date timestamp, activity_id integer NOT NULL, FOREIGN KEY (project_id) REFERENCES projects(id), FOREIGN KEY (activity_id) REFERENCES activities(id), UNIQUE(project_id, date))''')
    connection.commit()
    connection.close()

def add_project(project):
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    try:
        if project_exists(project):
            print "Project exists, foo"
            return
        t = (project,)
        c.execute('INSERT INTO projects (name) VALUES (?)', t)
        connection.commit()
    except sqlite3.OperationalError:
        raise WriteError("Error writing data")
    except TypeError:
        pass
    finally:
        connection.close()

def list_projects():
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    projects = []
    for row in c.execute('SELECT * FROM projects'):
        projects.append(row[1])
    return projects

def list_workdays():
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    workdays = []
    for row in c.execute('SELECT * FROM workdays'):
        workdays.append(row)
    return workdays

def delete_workdays():
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    c.execute('DELETE FROM workdays')
    connection.commit()
    connection.close()

def set_hours(hours, date, project):
    setup()
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    pid = get_project_id(project)
    if pid is None:
        raise NonExistentProjectError('project ' + project + 'does not exist')
    c.execute('''INSERT OR IGNORE INTO workdays(project_id, date, activity_id, number_of_hours) VALUES(?, ?, ?, ?)''', (pid, date, 0, 0))
    c.execute('''UPDATE workdays SET number_of_hours = ? WHERE project_id = ? AND date = ?''', (hours, pid, date))
    connection.commit()
    connection.close()

def show_date_for_project(date, project):
    setup()
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    pid = get_project_id(project)
    if pid is None:
        raise NonExistentProjectError('project ' + project + 'does not exist')
    for row in c.execute('SELECT * FROM workdays WHERE project_id = ? AND date = ?', (pid, date)):
        return row
    raise NoWorkdaysForDateError("")

def show_dates_for_week_and_project(week, project):
    setup()
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    pid = get_project_id(project)
    if pid is None:
        raise NonExistentProjectError('project ' + project + 'does not exist')

    dates = datesmod.DateHandler.dates_in_week(week)
    workdays = []
    for date in dates:
        c.execute('SELECT * FROM workdays WHERE project_id = ? AND date = ?', (pid, date))
        result = c.fetchall()
        if result:
            workdays.append(result[0])
        else:
            workdays.append((2, 0, date, 0))

    if workdays:
        return workdays
    else:
        raise NoWorkdaysForDateError("")

def show_date(date):
    setup()
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    for row in c.execute('SELECT * FROM workdays WHERE date = ?', (date,)):
        return row
    raise NoWorkdaysForDateError("")

def show_dates_for_week(week):
    setup()
    connection = sqlite3.connect('px.db')
    c = connection.cursor()

    dates = datesmod.DateHandler.dates_in_week(week)
    rows = []
    workdays_for_project = dict()
    projectids = set()
    #TODO: Improve crappy algorithm
    for date in dates:
        c.execute('SELECT * FROM workdays WHERE date = ?', (date,))
        days = c.fetchall()

        for day in days:
            pid = day[0]
            projectids.add(pid)

    for date in dates:
        c.execute('SELECT * FROM workdays WHERE date = ?', (date,))
        days = c.fetchall()

        for key in projectids:
            workdays_for_project.setdefault(key, dict())[date] = 0

        for day in days:
            pid = day[0]
            hours = day[1]
            workdays_for_project[pid][date] = hours

    if workdays_for_project:
        return workdays_for_project
    else:
        raise NoWorkdaysForDateError("")

def get_project_id(project):
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    t = (project + "%",)
    for row in c.execute('SELECT * FROM projects WHERE name LIKE ?', t):
        return row[0]

def project_exists(project):
    setup()
    connection = sqlite3.connect('px.db')
    c = connection.cursor()
    t = (project,)
    c.execute('SELECT * FROM projects WHERE name LIKE ?', t)
    response = c.fetchall()
    return len(response) > 0
