class Article:
    '''
    Represents an article and its properties
    '''

    def __init__(self, article_id, title, subtitle, author_id, author, date, content):
        self.article_id = article_id
        self.title = title
        self.subtitle = subtitle
        self.author_id = author_id
        self.author = author
        self.date = date
        self.content = content

    def fake_article_list(n):
        return [Article(x, x, x, x, x, x) for x in range(n)]
