class Inscription(object):
    def __init__(self, year, slug, faculty):
        self.year = int(year)
        self.slug = slug
        self.faculty = faculty

    def __repr__(self):
        return '<Inscription %s %s %s>' % (self.year, self.slug, self.faculty)


class User(object):
    def __init__(self, netid):
        self.netid = netid
        self.raw_matricule = None
        self.matricule = None
        self.last_name = None
        self.first_name = None
        self.birthday = None
        self.mail = None
        self.library = None
        self.university = None
        self.inscriptions = []

    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key == 'inscriptions':
                self.inscriptions.extend(val)
            elif not getattr(self, key):
                setattr(self, key, val)
