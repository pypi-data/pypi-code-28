class Redirect(Exception):
    def __init__(self, url):
        self.url = url
