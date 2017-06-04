class Article:
    '''
    Represents an article and its properties
    '''

    def __init__(self, article_id, title, author, date, formatting, content):
        self.title = title
        self.author = author
        self.date = date
        self.formatting = formatting
        self.article_id = article_id
        self.content = content

    def fake_article_list(n):
        return [Article(x, x, x, x, x, x) for x in range(n)]
