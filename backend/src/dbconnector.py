import mysql.connector as mariadb

class dbconnector():
    def __init__(self, name, passw, database)
        self.db = mariadb.connect(user,passw,database)
        self.cursor = self.db.cursor()
    def getArticle(self, aid)
        self.cursor.execute("SELECT WriterUID, title, subtitle, submitdate, summary, body FROM Articles WHERE AID=%s", (aid,))
        article = self.cursor.fetchone()
        WriterUID, title, subtitle, submitdate, summary, body = article
           
        
