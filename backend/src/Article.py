class Article:
    '''
    Represents an article and its properties
    '''

    def __init__(self, article_id, title, author, date, formatting):
        self.title = title
        self.author = author
        self.date = date
        self.formatting = formatting
        self.article_id = article_id
