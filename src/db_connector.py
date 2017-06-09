import time
import mysql.connector as mariadb
from passlib.apps import custom_app_context as pwd_context
from Config import config
from Article import Article


class db_connector():
    def __init__(self):
        self.db = mariadb.connect(user=config['DB_USER'],
                                  password=config['DB_PASS'],
                                  database=config['DB_NAME'])

        self.cursor = self.db.cursor()
        self.db.paramstyle = 'format'

    # ARTICLE MANAGEMENT
    def get_article(self, article_id):
        # gets an article from the database,
        # returns a dictionary with article content and everything
        # try:
        self.cursor.execute(
            "SELECT WriterUID, title, subtitle, submitdate, summary, body FROM Articles WHERE AID = %s",
            (article_id,))
        writer_user_id, title, subtitle, submitdate, summary, body = self.cursor.fetchall()[0]
        self.cursor.reset()
        writer = self.get_displayname(writer_user_id)
        return Article(
            article_id,
            title,
            subtitle,
            writer_user_id,
            writer,
            submitdate,
            body
        )
        # except Exception as e:
        #   return False

    def push_article(self, writer_user_id, title, subtitle, summary, body, link_ids=[], tags=[]):
        # adds a new article to the database,
        # returns a bool describing whether the action was successfull and a second field containing either the reason for failure or the article's newly generated article id upon success
        submitdate = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        try:
            self.cursor.execute(
                "INSERT INTO Articles (WriterUID, title, subtitle, submitdate, summary, body) VALUES(%s,%s,%s,%s,%s,%s);",
                (writer_user_id, title, subtitle, submitdate, summary, body))
            article_id = self.cursor.lastrowid
            for link_id in link_ids:
                self.cursor.execute("INSERT INTO Links (ChildAID, ParentAid) Values(%s, %s)", (article_id, link_id))
            for tag in tags:
                self.cursor.execute("INSERT INTO Tags (AID, tag) Values(%s, %s)", (article_id, tag))
            self.db.commit()
            return True, article_id
        except:
            return False, "query execution failed"

    def delete_article(self, article_id):
        pass

    # ARTICLE LISTS
    def get_article_list(self, sort, amount, offset, method=False, tag=False, article_id=False):
        # add amount, offset
        # try:
        if method == "children":
            self.cursor.execute("SELECT ChildAID FROM Links WHERE ParentAID=%s;", (article_id,))
        elif method == "parents":
            self.cursor.execute("SELECT ParentAID FROM Links WHERE ChildAID=%s;", (article_id,))
        elif method == "tagged":
            self.cursor.execute("SELECT AID FROM Tags WHERE tag=%s;", (tag,))
        elif method is False:
            self.cursor.execute("SELECT AID FROM Articles;")
        else:
            raise ValueError("This method doesn't exist")
        # except:
        #    raise IOError("Article list query failed")
        return [self.get_article(i[0]) for i in self.cursor.fetchall()]

    # USER MANAGEMENT
    def get_displayname(self, user_id):
        # gets the name to be displayed for a given user id
        # returns a string with displayname or username if the user has no displayname. If the user doesn't exist, it returns false.
        if not self.check_user_exists(user_id=user_id):
            return False
        self.cursor.execute("SELECT displayname, username FROM Users WHERE UID = %s", (user_id,))
        displayname, username = self.cursor.fetchone()
        self.cursor.reset()
        if displayname:
            return displayname
        return username

    def push_user(self, username, password, email, displayname=""):
        # adds a new user account to the database,
        # returns a bool describing whether the action was successfull and in the second field the newly generated user id upon success or the reason for failure upon failure
        password = pwd_context.hash(password)
        regdate = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        if self.check_user_exists(username=username):
            raise ValueError("a user with the given username already exists")
        try:
            self.cursor.execute(
                "INSERT INTO Users (displayname, username, password, email, regdate) Values(%s, %s, %s, %s, %s)",
                (displayname, username, password, email, regdate))
            self.db.commit()
            return True, self.cursor.lastrowid
        except:
            raise IOError("User pushing query failed")

    def modify_user(self, user_id, username=False, password=False, email=False, displayname=False):
        # modifies the properties of a preexisting user acocunt,
        # returns True if all goes well
        # server.py needs to check whether the user already has a session before executing this function
        if not self.check_user_exists(username=username):
            raise ValueError("a user with the given username doesnt exist")
        # still need to update this so it doesn't fail when people try to input their own username
        if username:
            try:
                self.cursor.execute("UPDATE Users SET username=%s WHERE UID=%s", (username, user_id))
            except:
                raise IOError("username query failed")
        if password:
            try:
                self.cursor.execute("UPDATE Users SET password=%s WHERE UID=%s", (pwd_context.hash(password), user_id))
            except:
                raise IOError("password query failed")
        if email:
            try:
                self.cursor.execute("UPDATE Users SET email=%s WHERE UID=%s", (email, user_id))
            except:
                raise IOError("email query failed")
        if displayname:
            try:
                self.cursor.execute("UPDATE Users SET displayname=%s WHERE UID=%s", (displayname, user_id))
            except:
                raise IOError("displayname query failed")
        try:
            self.db.commit()
        except:
            raise IOError("Committing changes to database failed")

    def check_user_exists(self, username=False, user_id=False):
        # checks whether a user exists with the properties in the variables
        # returns bool
        # todo: maybe add email too?
        if username and user_id:
            self.cursor.execute(
                "SELECT UID from Users where username=%s and UID=%s",
                (username, user_id,))
            return bool(self.cursor.fetchone())
        elif username:
            self.cursor.execute(
                "SELECT UID from Users where username=%s",
                (username,))
            return bool(self.cursor.fetchone())
        elif user_id:
            self.cursor.execute(
                "SELECT UID from Users where UID=%s",
                (user_id,))
            return bool(self.cursor.fetchone())
        return False

    def check_password(self, username, password):
        # checks whether the supplied password is correct,
        # returns bool
        if not self.check_user_exists(username=username):
            raise ValueError("no user with the given username exists")
        self.cursor.execute("SELECT password from Users where username=%s", (username,))
        fetched_hash = self.cursor.fetchone()[0]
        if pwd_context.verify(password, fetched_hash):
            return True
        return False
