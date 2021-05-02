from base64 import b64encode

######################################  F U N C T I O N S  ############################################
def get_id(name):
    string = b64encode(name.encode()).decode('utf-8')
    if len(string)>22:
        string = string[:22]
    return string
######################################  C L A S S E S  ############################################
class Artist(db.Model):
    id = db.Column(db.String(100), primary_key = True, unique=True)
    name = db.Column(db.String(100))
    age= db.Column(db.Integer)
    # albums = db.relationship('Album', backref='Artista', lazy=True)
    # tracks = db.relationship('Cancion', backref='Artista', lazy=True)
    albums = db.Column(db.String(200))   #url
    tracks = db.Column(db.String(200))   #url
    url = db.Column(db.String(200))     #url
    def __init__(self, name, age):
        self.id = get_id(name)
        self.name = name
        self.age = age
        self.albums = 'http://localhost:5000/artists/'+self.id+'/albums'
        self.tracks = 'http://localhost:5000/artists/'+self.id+'/tracks'
        self.url = 'http://localhost:5000/artists/'+self.id

    def to_String(self):
        return ({'id':self.id, 
        'name':self.name, 
        'age':self.age, 
        'albums':self.albums, 
        'tracks':self.tracks,
        'self':self.url})

class Album(db.Model):
    id = db.Column(db.String(100), primary_key = True, unique=True)
    name = db.Column(db.String(100))
    artist_id = db.Column(db.String(200), db.ForeignKey('artist.id'), nullable=False)
    genre = db.Column(db.String(100))
    tracks = db.Column(db.String(200))  #url
    artist = db.Column(db.String(200))  #url
    url = db.Column(db.String(200))    #url
    def __init__(self, name, genre, artist_id):
        self.id = get_id(name)
        self.name = name
        self.artist_id = artist_id
        self.genre = genre
        self.artist = 'http://localhost:5000/artists/'+self.artist_id
        self.tracks = 'http://localhost:5000/albums/'+self.id+'/tracks'
        self.url = 'http://localhost:5000/albums/'+self.id
    def to_String(self):
        return ({'id':self.id, 
        'artist_id': self.artist_id,
        'name':self.name, 
        'genre':self.genre, 
        'artist':self.artist, 
        'tracks':self.tracks,
        'self':self.url})

class Track(db.Model):
    id = db.Column(db.String(100), primary_key = True, unique=True)
    name = db.Column(db.String(100))
    album_id = db.Column(db.String(100), db.ForeignKey('album.id'), nullable=False)
    duration = db.Column(db.Float)
    times_played = db.Column(db.Integer)
    album = db.Column(db.String(200))  #url
    artist = db.Column(db.String(200))  #url
    url = db.Column(db.String(200))    #url

    def __init__(self, name, album_id, duration, artist_id, n):
        self.id = get_id(name)
        self.name = name
        self.album_id = album_id
        self.duration = duration
        self.times_played = n
        self.artist = 'http://localhost:5000/artists/'+artist_id
        self.album = 'http://localhost:5000/albums/'+self.album_id
        self.url = 'http://localhost:5000/tracks/'+self.id

    def to_String(self):
        return ({'id':self.id, 
        'album_id': self.album_id,
        'name':self.name, 
        'duration':self.duration, 
        'times_played':self.times_played, 
        'artist':self.artist, 
        'album':self.album,
        'self':self.url})

    def play(self):
        self.times_played = self.times_played + 1

###################################### S C H E M A ######################################
class ArtistSchema(ma.Schema):
  class Meta:
      fields = ('id', 'name', 'age', 'albums', 'tracks', 'self')
class AlbumSchema(ma.Schema):
  class Meta:
    fields = ('id', 'artist_id', 'name', 'genre', 'artist', 'tracks', 'self')
class TrackSchema(ma.Schema):
  class Meta:
    fields = ('id', 'album_id', 'name', 'duration', 'times_played', 'artist', 'album', 'self')