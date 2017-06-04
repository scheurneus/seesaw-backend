from flask import Flask
from flask import request
from flask_cors import CORS
from Renderer import Renderer
import time
from Article import Article

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
            return Renderer.render_index(False)

        @self.app.route("/articles/", methods=["GET"])
        def articles():
            '''
            Returns a list of articles
            '''
            return Renderer.render_article_list(False, Article.fake_article_list(5))

        @self.app.route("/articles/<int:article_id>", methods=["GET"])
        def get_article(article_id):
            '''
            Returns the article with article id {article_id}
            '''
            return Renderer.render_article(False, Article("1", "2", "3", "4", "5", "6"))

        @self.app.route("/articles/<method>/", defaults={
            "count": 10, "start": 0
        }, methods=["GET"])
        @self.app.route("/articles/<method>/<int:count>/", defaults={
            "start": 0
        }, methods=["GET"])
        @self.app.route("/articles/<method>/<int:count>/<int:start>", methods=[
            "GET"
        ])
        def article_sorted(method, count, start):
            '''
            Returns {count} sorted by {method} articles,
            starting from {start}
            '''
            if(method != "oldest"
               and method != "newest"
               and method != "controversial"):
                return "Unknown sorting method"
            return Renderer.render_sorted_article_list(
                False, Article.fake_article_list(count)[start:], method, count, start)

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

            return Renderer.render_linked_articles(
                False, Article.fake_article_list(count)[start:], article_id)

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
            '''
            Deletes the article with article id {article_id}
            '''
            return "Deleting the article {}".format(article_id)

        self.app.run(self.ip_adress, self.port)

if __name__ == "__main__":
    s = Server("127.0.0.1", 8080)
    s.start()
