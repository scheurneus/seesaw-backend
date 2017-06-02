import mysql.connector as mariadb

class dbconnector():
    def __init__(self, name, passw, dbase)
        self.db = mariadb.connect(username=user,password=passw,database=dbase)
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
        article = self.cursor.fetchone()
        self.cursor.reset()
        WriterUID, title, subtitle, submitdate, summary, body = article
        author = getDisplayName(WriterUID)
    
