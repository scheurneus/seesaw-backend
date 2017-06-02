import mysql.connector as mariadb

class db_connector():
    def __init__(self, db_username, db_password, db_host):
        self.db = mariadb.connect(user=db_username,password=db_password,database=db_host)
        self.cursor = self.db.cursor()
    
    def get_displayname(self,uid):
        self.cursor.execute("SELECT displayname, username FROM Users WHERE UID=%s",(uid,))
        displayname, username = self.cursor.fetchone()
        self.cursor.reset()
        if displayname:
            return displayname
        else:
            return username
    
    def get_article(self, aid):
        self.cursor.execute("SELECT WriterUID, title, subtitle, submitdate, summary, body FROM Articles WHERE AID=%s", (aid,))
        author_uid, title, subtitle, submitdate, summary, body = self.cursor.fetchone()
        self.cursor.reset()
        author = self.get_display_name(writer_uid)
        # Get parents and children, stored in a list of ints.
        self.cursor.execute("SELECT ParentAID FROM Links WHERE ChildAID=%s",(aid,))
        parents = [i[0] for i in self.cursor.fetchall()]
        self.cursor.execute("SELECT ChildAID FROM Links WHERE ParentAID=%s",(aid,))
        children = [i[0] for i in self.cursor.fetchall()]
        # Get tags, stored in a list strings.
        self.cursor.execute("SELECT tag FROM Tags WHERE AID=%s",(aid,))
        tags = [i[0] for i in self.cursor.fetchall()]

    def push_article(self, writer_uid, title, subtitle, submitdate, summary, body, links_ids=[], tags=[]):
        query = "INSERT INTO Articles (WriterUID, title, subtitle, submitdate, summary, body) VALUES(%d,%s,%s,%s,%s,%s);"
        try:
            self.cursor.execute(query, (writer_uid, title, subtitle, submitdate, summary, body))
            article_id = cursor.lastrowid
            for link_id in link_ids:
                self.cursor.execute("INSERT INTO Links (ChildAID, ParentAid) Values(%d, %d)", (article_id, link_id))
            for tag in tags:
                self.cursor.execute("INSERT INTO Tags (AID, tag) Values(%d, %s)", (article_id, tag))
            return article_id
        except:
            return False

    def push_user(self, username, password, email, displayname=""):
        password = hash(password)
        regdate = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO Users (displayname, username, password, email, regdate) Values(%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (displayname, username, password, email, regdate))
            return curser.lastrowid
        except:
            return False
    
    def modify_user(self, user_id, username=False, password=False, email=False, displayname=False):
        if username:
            pass
        if password:
            pass
        if email:
            pass
        if displayname:
            pass
    def check_password(self, username, password):
        pass
