from flask import render_template
from json import dumps


class Renderer:
    '''Class that, given response data, decides what to return to the client'''

    def render_index(api_request):
        '''Renders the index of the website'''

        if(api_request):
            return "index"
        return render_template("index.html")

    def render_article(api_request, article):
        '''
        Renders a single article
        '''
        if not api_request:
            return render_template("article.html", article=article)

        return dumps({
            'title': article.title,
            'subtitle': article.subtitle,
            'author': article.author,
            'date': article.date,
            'article_id': article.article_id
        })

    def render_article_list(api_request, articles, method, origin=False):
        '''Renders/outputs an already sorted list of articles'''
        if not api_request:
            pass
            if method == "oldest":
                list_title = "Oldest Articles"
            elif method == "newest":
                list_title = "Newest Articles"
            elif method == "controversial":
                list_title = "Articles with most activity"
            elif method == "tagged":
                list_title = "Articles with the tag %s" % origin
            elif method == "parents_of":
                list_title = "Articles that %s replies to" % origin
            elif method == "children_of":
                list_title = "Articles that reply to %s" % origin

            render_template("list.html", articles=articles, list_title=list_title)

        return dumps([{
            'title': article.title,
            'author': article.author,
            'date': article.date,
            'formatting': article.formatting,
            'article_id': article.article_id
        } for article in articles])

    def render_error(api_request, reason):
        if api_request:
            return dumps(reason)
        return render_template("error.html", error_reason=reason)
