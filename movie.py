class Movie():
    def __init__(self, film_id, title, certificate, length, poster_url):
        self.film_id = film_id
        self.title = title
        self.certificate = certificate
        self.length = length
        self.poster_url = poster_url

    def serialize(self):
        return {
                    'film_id': self.film_id,
                    'title': self.title,
                    'certificate': self.certificate,
                    'length': self.length,
                    'poster_url': self.poster_url
        }

