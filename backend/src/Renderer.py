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
            return render_template("article_template.html", article=article)

        return dumps({
            'title': article.title,
            'author': article.author,
            'date': article.date,
            'formatting': article.formatting,
            'article_id': article.article_id
        })

    def render_list(api_request, articles, method, origin_id=False, tag=False):
        '''Renders/outputs an already sorted list of articles'''
        if not api_request:
            pass
            if method=="oldest":
                list_title = "Oldest Articles"
            elif method=="newest":
                list_title = "Newest Articles"
            elif method=="controversial":
                list_title = "Articles most activity"
            elif method=="tagged":
                list_title = "Articles with the tag %s" %tag
            elif method=="parents_of":
                list_title = "Articles that %s replies to" %origin_id
            elif method=="children_of":
                list_title = "Articles that reply to %s" %origin_id

            render_template("list.html", articles=articles, list_title=list_title)

        return dumps([{
            'title': article.title,
            'author': article.author,
            'date': article.date,
            'formatting': article.formatting,
            'article_id': article.article_id
        } for article in articles])
            
    def render_article_list(api_request, article_list):
        '''Renders a list of articles'''

        if not api_request:
            return render_template("featured_article_list_template.html", articles=article_list)
        return dumps([{
            'title': article.title,
            'author': article.author,
            'date': article.date,
            'formatting': article.formatting,
            'article_id': article.article_id
        } for article in article_list])

    def render_sorted_article_list(api_request, article_list, method, count, start):
        '''Renders a sorted list of articles'''

        if method != "oldest" and method != "newest" and method != "controversial":
            if api_request:
                return dumps({'error': 'Unknown sorting method'})
            return render_template("error.html", error_reason="The sorting method you selected does not (yet) exist")
        if api_request:
            return Renderer.render_article_list(True, article_list)

        return render_template("list.html",
                               articles=article_list, method=method,
                               count=count, start=start)

    def render_linked_articles(api_request, article_list, article_id):
        '''Renders a list of linked articles'''

        if api_request:
            return Renderer.render_article_list(True, article_list)
        return render_template("list.html",
                               articles=article_list, article_id=article_id)

