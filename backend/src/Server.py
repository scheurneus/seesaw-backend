from flask import Flask, request
from flask_cors import CORS

import time

class Server:
    """
    This is the main class that handles
    routing and most of the server functionalities
    """
    def __init__(self, ip, port):
        """
        Inits the server.
        """
        self.ip_adress = ip
        self.port = port
        self.app = Flask("Server")
        self.app.debug = True
        CORS(self.app)

    def start(self):
        """
        Starts the server
        """

        @self.app.route("/", methods=["GET"])
        def index():
            '''
            Index page
            '''
            return "index"

        @self.app.route("/articles", methods=["GET"])
        def articles():
            '''
            Returns a list of articles
            '''
            return "articles"

        @self.app.route("/articles/<int:article_id>", methods=["GET"])
        def get_article(article_id):
            '''
            Returns the article with article id {article_id}
            '''
            return "Returning the article {}".format(article_id)

        @self.app.route("/articles/<method>/", defaults={
            "count": 10, "start": 0
        }, methods=["GET"])
        @self.app.route("/articles/<method>/<int:count>/", defaults={
            "start": 0
        }, methods=["GET"])
        @self.app.route("/articles/<method>/<int:count>/<int:start>", methods=[
            "GET"
        ])
        def article_sorted(list_type, count, start):
            '''
            Returns {count} sorted by {method} articles,
            starting from {start}
            '''
            if list_type == "newest":
                pass
            elif list_type == "oldest":
                pass
            elif list_type == "controversial":
                pass
            else:
                return "Unknown sorting method"
            return '''{} articles
            sorted by {}, starting from {}'''.format(count, method, start)

        @self.app.route("/articles/<int:article_id>/linked", defaults={
            'count': 10,
            'start': 0
        }, methods=["GET"])
        @self.app.route("/articles/<int:article_id>/linked/<int:count>/",
                        defaults={
                            'start': 0
                        }, methods=["GET"])
        @self.app.route(
            "/articles/<int:article_id>/linked/<int:count>/<int:start>",
            methods=["GET"])
        def linked_articles(article_id, count, start):
            '''
            Returns all articles linked to the article with
            article id = {article_id}
            '''
            return '''{} articles linked to {}
                , starting from {}'''.format(count, article_id, start)

        @self.app.route("/articles", methods=["POST"])
        def create_article():
            '''
            Creates an article using POST parameters
            '''
            return '''
                Creating an article with title {},
                 posted by {} on {}, using format {}.
                 Content : {}
            '''.format(request.form.get("name"),
                       request.form.get("author"),
                       time.strftime("%c"),
                       request.form.get("formatting"),
                       request.form.get("text"))

        @self.app.route("/articles/<int:article_id>", methods=["PUT"])
        def update_article(article_id):
            return "Updating the content of article {}".format(article_id)


        @self.app.route("/articles/<int:article_id>", methods=["DELETE"])
        def delete_article(article_id):
            return "Deleting the article {}".format(article_id)

        self.app.run(self.ip_adress, self.port)

if __name__ == "__main__":
    s = Server("127.0.0.1", 8080)
    s.start()
