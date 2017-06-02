import mysql.connector as mariadb

class db_connector():
    def __init__(self, uname, passw, dbase):
        self.db = mariadb.connect(user=uname,password=passw,database=dbase)
        self.cursor = self.db.cursor()
    
    def getDisplayName(self,uid):
        self.cursor.execute("SELECT displayname, username FROM Users WHERE UID=%s",(uid,))
        displayname, username = self.cursor.fetchone()
        self.cursor.reset()
        if displayname:
            return displayname
        else:
            return username
    
    def getArticle(self, aid):
        self.cursor.execute("SELECT WriterUID, title, subtitle, submitdate, summary, body FROM Articles WHERE AID=%s", (aid,))
        WriterUID, title, subtitle, submitdate, summary, body = self.cursor.fetchone()
        self.cursor.reset()
        author = self.getDisplayName(WriterUID)
        # Get parents and children, stored in a list of ints.
        self.cursor.execute("SELECT ParentAID FROM Links WHERE ChildAID=%s",(aid,))
        parents = [i[0] for i in self.cursor.fetchall()]
        self.cursor.execute("SELECT ChildAID FROM Links WHERE ParentAID=%s",(aid,))
        children = [i[0] for i in self.cursor.fetchall()]
        # Get tags, stored in a list strings.
        self.cursor.execute("SELECT tag FROM Tags WHERE AID=%s",(aid,))
        tags = [i[0] for i in self.cursor.fetchall()]
