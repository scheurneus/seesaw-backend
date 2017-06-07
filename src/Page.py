class Page:
    '''
    Represents an article and its properties
    '''

    def __init__(self, title, in_page_title, summary, content):
        self.title = title
        self.in_page_title = in_page_title
        self.summary = summary
        self.content = content
