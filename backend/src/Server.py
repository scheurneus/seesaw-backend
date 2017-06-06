from flask import Flask, request
from flask_cors import CORS
from Renderer import Renderer
import time
from Article import Article
from db_connector import db_connector
import Config

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
            #try:
            article = db.get_article(article_id) 
            return Renderer.render_article(api, article)
            #except:
                #return Renderer.render_error(api, "blarg")

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
        @self.app.route("/articles/",                                   methods=["GET"], defaults={'api': False, 'offset': False, 'var_2': False, 'var_1': False, 'method': 'newest'})
        @self.app.route("/articles/<method>/",                          methods=["GET"], defaults={'api': False, 'var_3': False, 'var_2': False, 'var_1': False})
        @self.app.route("/articles/<method>/<var_1>/",                  methods=["GET"], defaults={'api': False, 'var_3': False, 'var_2': False})
        @self.app.route("/articles/<method>/<var_1>/<var_2>/",          methods=["GET"], defaults={'api': False, 'var_3': False})
        @self.app.route("/articles/<method>/<var_1>/<var_2>/<var_3>/",  methods=["GET"], defaults={'api': False})
        @self.app.route("/api/articles/",                                   methods=["GET"], defaults={'api': True, 'var_3': False, 'var_2': False, 'var_1': False, 'method': 'newest'})
        @self.app.route("/api/articles/<method>/",                          methods=["GET"], defaults={'api': True, 'var_3': False, 'var_2': False, 'var_1': False})
        @self.app.route("/api/articles/<method>/<var_1>/",                  methods=["GET"], defaults={'api': True, 'var_3': False, 'var_2': False})
        @self.app.route("/api/articles/<method>/<var_1>/<var_2>/",          methods=["GET"], defaults={'api': True, 'var_3': False})
        @self.app.route("/api/articles/<method>/<var_1>/<var_2>/<var_3>/",  methods=["GET"], defaults={'api': True})
        def article_list(method, var_1, var_2, var_3, api):
            if method in ["newest", "oldest", "controversial"]:
                origin, amount, offset = False, var_1, var_2
            elif method in ["parents_of", "children_of", "tagged"]:
                origin, amount, offset = var_1, var_2, var_3
            else:
                return Renderer.render_error("This listing method doesn't seem to exist (yet).")
            article_list = db_connector.article_list(method, origin=origin, amount=amount, start=offset)
            return Renderer.render_article_list(api, article_list, method, origin=origin)


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
            return Renderer.render_error(False,"404: page not found.")

        self.app.run(self.ip_adress, self.port)

if __name__ == "__main__":
    s = Server("127.0.0.1", 8080)
    db = db_connector()
    s.start()
