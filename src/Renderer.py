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
            'article_id': article.article_id,
            'title': article.title,
            'subtitle': article.subtitle,
            'author_id': article.author_id,
            'author': article.author,
            'date': str(article.date),
            'content': article.content
        })

    def render_article_list(api_request, articles, sort, amount, offset, method=False, tag=False, article_id=False):
        '''Renders/outputs an already sorted list of articles'''
        if not api_request:
            pass
            if method == "tagged":
                list_title = "Articles with the tag %s" % tag
            elif method == "parents_of":
                list_title = "Articles that %s replies to" % origin
            elif method == "children_of":
                list_title = "Articles that reply to %s" % origin
            else:
                list_title = "All Articles"

            return render_template("list.html", articles=articles, list_title=list_title)

        return dumps([{
            'article_id': article.article_id,
            'title': article.title,
            'subtitle': article.subtitle,
            'author_id': article.author_id,
            'author': article.author,
            'date': str(article.date)
        } for article in articles])

    def render_page(api_request, page):
        if not api_request:
            return render_template("static_page.html", page=page)
        return dumps({
            'title':            page.title,
            'in_page_title':    page.in_page_title,
            'summary':          page.summary,
            'content':          page.content
        })
    def render_error(api_request, reason):
        if api_request:
            return dumps(reason)
        return render_template("error.html", error_reason=reason)
