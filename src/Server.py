from flask import Flask, request
from flask_cors import CORS
from Renderer import Renderer
import time
from db_connector import db_connector


class Server:
    """
    This is the main class that handles
    routing and most of the server functionalities
    """
    def __init__(self, ip, port):
        """Inits the server."""

        self.ip_adress = ip
        self.port = port
        self.app = Flask("Server")
        self.app.debug = True
        CORS(self.app)
        self.db = db_connector()

    def get_sorting_params(self, get_vars):
        return "newest", 10, 0
#        sort = "newest" if get_vars["sort"] not in ["newest", "oldest", "controversial"] else get_vars["sort"]
#        amount = 10 if not type(get_vars["amount"]) == int else get_vars["amount"]
#        offset = 0 if not type(get_vars["offset"]) == int else get_vars["offset"]
#        return sort, amount, offset

    def start(self):
        """Starts the server"""

        # INDEX
        @self.app.route("/", methods=["GET"])
        def index():
            '''Index page'''
            return Renderer.render_index(False)

        # ARTICLE MANAGEMENT
        @self.app.route("/articles/<int:article_id>",     methods=["GET"], defaults={"api": False})
        @self.app.route("/api/articles/<int:article_id>", methods=["GET"], defaults={"api": True})
        def get_article(article_id, api):
            '''Returns the article with article id {article_id}'''
            # try:
            article = self.db.get_article(article_id)
            return Renderer.render_article(api, article)
            # except:
            #   return Renderer.render_error(api, "blarg")

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


        # ARTICLE LISTS
        @self.app.route("/articles/",           methods=["GET"], defaults={'api': False})
        @self.app.route("/api/articles/",           methods=["GET"], defaults={'api': True})
        def article_list(api):
            sort, amount, offset = self.get_sorting_params(request.args)
            articles = self.db.get_article_list(sort, amount, offset)
            return Renderer.render_article_list(api, articles, sort, amount, offset)

        @self.app.route("/articles/tagged/<tag>/",      defaults={'api': False})
        @self.app.route("/api/articles/tagged/<tag>/",  defaults={'api': True})
        def tagged_article_list(api, tag):
            sort, amount, offset = self.get_sorting_params(request.args)
            articles = self.db.get_article_list(sort, amount, offset, method="tagged", tag=tag)
            return Renderer.render_article_list(api, articles, sort, amount, offset, method="tagged", tag=tag)

        @self.app.route("/articles/children/<article_id>/",         defaults={'api': False})
        @self.app.route("/api/articles/children/<article_id>/",     defaults={'api': True})
        def children_article_list(api, article_id):
            sort, amount, offset = self.get_sorting_params(request.args)
            articles = self.db.get_article_list(sort, amount, offset, method="children", article_id=article_id)
            return Renderer.render_article_list(api, articles, sort, amount, offset, method="children", article_id=article_id)

        @self.app.route("/articles/parents/<article_id>/",      defaults={'api': False})
        @self.app.route("/api/articles/parents/<article_id>/",  defaults={'api': True})
        def parents_article_list(api, article_id):
            sort, amount, offset = self.get_sorting_params(request.args)
            articles = self.db.get_article_list(sort, amount, offset, method="parents", article_id=article_id)
            return Renderer.render_article_list(api, articles, sort, amount, offset, method="parents", article_id=article_id)

        # ACOUNT MANAGEMENT
        @self.app.route("/login", methods=["POST"])
        def login():
            pass

        @self.app.route("/register", methods=["POST"])
        def register():
            pass

        @self.app.route("/modify_user", methods=["PUSH"])
        def modify_user():
            pass

        @self.app.errorhandler(404)
        def page_not_found(e):
            return Renderer.render_error(False, "404: page not found.")

        self.app.run(self.ip_adress, self.port)

if __name__ == "__main__":
    s = Server("127.0.0.1", 8080)
    s.start()
