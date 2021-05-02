from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from models import get_id, Artist, Album, Track, ArtistSchema, AlbumSchema, TrackSchema


######################################  I N I T  ############################################
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#data base
database_path = os.getenv('DATABASE_URL', default_database_path)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

#INIT DB
db = SQLAlchemy(app)
#INIT MARSHMALLOW
ma = Marshmallow(app)


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many = True)
album_schema  = AlbumSchema()
albums_schema  = AlbumSchema(many = True)
track_schema  = TrackSchema()
tracks_schema  = TrackSchema(many = True)

######################################  R E Q U E S T S ############################################
@app.route('/')
def index():
    return "<h1> Deployed to Heroku</h1>"
######################## POST #############################
### CREATE AN ARTIST ###
@app.route('/artists', methods = ['POST'])       
def create_artist():
    n = 'name'
    a = 'age'
    valido = False
    if n in request.json and a in request.json:
        name   = request.json['name']
        age    = request.json['age']
        if type(name)== str and type(age) == int:
            valido = True
    if valido == False:
        return 'input inválido', 400
    else:
        all_artists = Artist.query.all()
        if all_artists:
            result = artists_schema.dump(all_artists)
            for artist in result:
                if artist["name"] == request.json['name']:
                    artist_id = artist["id"]
                    artist = Artist.query.filter_by(id = artist_id).first()
                    return artist.to_String(), 409
        new_artist = Artist(name, age)
        db.session.add(new_artist)
        db.session.commit()
        #artista creado
        return new_artist.to_String(), 201
        
### CREATE AN ALBUM ###
@app.route('/artists/<artist_id>/albums', methods = ['POST'])       
def create_album(artist_id):
    n = 'name'
    g = 'genre'
    valido = False
    if n in request.json and g in request.json:
        name   = request.json['name']
        genre   = request.json['genre']
        if type(name)== str and type(genre) == str and type(artist_id) == str:
            valido = True
    if valido == False:
        return 'input inválido', 400
    elif Artist.query.get(artist_id) is None:
        return 'artista no existe', 422
    all_albums = Album.query.filter_by(artist_id = artist_id).all()
    if all_albums:
        result = albums_schema.dump(all_albums)
        for album in result:
            if album['name'] == request.json['name']:
                #album ya existe
                a = Album.query.filter_by(id = album["id"]).first()
                return a.to_String(), 409    
    new_album = Album(name, genre, artist_id)
    db.session.add(new_album)
    db.session.commit()
    return new_album.to_String(), 201
    
### CREATE A TRACK ###
@app.route('/albums/<album_id>/tracks', methods = ['POST'])       
def create_track(album_id):
    n = 'name'
    d = 'duration'
    valido = False
    if n in request.json and d in request.json:
        name   = request.json['name']
        duration = request.json['duration']
        if type(album_id) == str and type(name) == str and type(duration)== float:
            valido = True
    if valido == False:
        return "input inválido", 400
    elif Album.query.get(album_id) is None:
        return 'álbum no existe', 422
    elif Album.query.get(album_id):
        all_tracks = Track.query.filter_by(album_id = album_id).all()
        result = tracks_schema.dump(all_tracks)
        for track in result:
            if track['name'] == request.json['name']:
                #canción ya existe
                t = Track.query.filter_by(id = track["id"]).first()
                return t.to_String(), 409
            
        album = Album.query.get(album_id)
        artist_id = album.artist_id
        new_track = Track(name, album_id, duration, artist_id, 0)
        db.session.add(new_track)
        db.session.commit()
        return new_track.to_String(), 201

######################## GET #############################

### GET ALL ARTIST ###
@app.route('/artists', methods=['GET'])
def get_artists():
    all_artists = Artist.query.all()
    a = [artist.to_String() for artist in all_artists]
    return jsonify(a), 200

### GET ALL ALBUMS ###
@app.route('/albums', methods = ['GET'])
def get_albums():
    all_albums = Album.query.all()
    a = [album.to_String() for album in all_albums]
    return jsonify(a), 200

### GET ALL TRACKS ###
@app.route('/tracks', methods = ['GET'])
def get_tracks():
    all_tracks = Track.query.all()
    a = [track.to_String() for track in all_tracks]
    return jsonify(a), 200

### GET A SINGLE ARTIST ###
@app.route('/artists/<artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return 'artista no encontrado', 404
    return artist.to_String(), 200

### GET ALL ALBUMS OF AN ARTIST ###
@app.route('/artists/<artist_id>/albums', methods=['GET'])
def get_artist_albums(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return 'artista no encontrado', 404
    all_albums = Album.query.filter_by(artist_id = artist_id).all()
    a = [album.to_String() for album in all_albums]
    return jsonify(a), 200

### GET ALL TRACKS OF AN ARTIST ###   
@app.route('/artists/<artist_id>/tracks', methods=['GET'])
def get_artist_tracks(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return 'artista no encontrado', 404
    all_albums = Album.query.filter_by(artist_id = artist_id).all()
    result = albums_schema.dump(all_albums)
    result_tracks= []
    for album in result:
        all_tracks = Track.query.filter_by(album_id = album['id']).all()
        a = [track.to_String() for track in all_tracks]
        result_tracks+= a
    return jsonify(result_tracks), 200

### GET A SINGLE ALBUM ### 
@app.route('/albums/<album_id>', methods=['GET'])
def get_album(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return 'álbum no encontrado', 404
    return album.to_String(), 200

### GET  ALL TRACKS OF AN ALBUM ### 
@app.route('/albums/<album_id>/tracks', methods=['GET'])
def get_album_tracks(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return 'álbum no encontrado', 404
    all_tracks = Track.query.filter_by(album_id = album_id).all()
    a = [track.to_String() for track in all_tracks]
    return jsonify(a), 200

### GET A SINGLE TRACK ### 
@app.route('/tracks/<track_id>', methods=['GET'])
def get_track(track_id):
    track = Track.query.get(track_id)
    if track is None:
        return 'canción no encontrada', 404
    return track.to_String(), 200

######################## PUT #############################
### PUT ALL TRACKS OF AN ARTIST ###
@app.route('/artists/<artist_id>/albums/play', methods=['PUT'])
def put_artist_tracks(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        all_albums = Album.query.filter_by(artist_id = artist_id).all()
        result = albums_schema.dump(all_albums)
        for album in result:
            all_tracks = Track.query.filter_by(album_id = album['id']).all()
            for track in all_tracks:
                track.play()
        return "todas las canciones del artista fueron reproducidas", 200
    else:
        return "artista no encontrado", 404

### PUT ALL TRACKS OF AN ALBUM ###
@app.route('/albums/<album_id>/tracks/play', methods=['PUT'])
def put_album_tracks(album_id):
    album = Album.query.get(album_id)
    if album:
        all_tracks = Track.query.filter_by(album_id = album_id).all()
        for track in all_tracks:
            track.play()
        return "todas las canciones del álbum fueron reproducidas", 200
    else:
        return "álbum no encontrado", 404  

### PUT A TRACK ###
@app.route('/tracks/<track_id>/play', methods=['PUT'])
def put_track(track_id):
    track = Track.query.get(track_id)
    if track:
        track.play()
        return "canción reproducida", 200
    else:
        return "canción no encontrado", 404  

######################## DELETE #############################

### DELETE A ARTIST ###
@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        all_albums = Album.query.filter_by(artist_id = artist_id).all()
        result = albums_schema.dump(all_albums)
        for album in result:
            all_tracks = Track.query.filter_by(album_id = album['id']).all()
            for track in all_tracks:
                db.session.delete(track)
                db.session.commit()
            db.session.delete(Album.query.get(album['id']))
            db.session.commit()
        db.session.delete(artist)
        db.session.commit()
        return "artista eliminado", 204
    else:
        return "artista inexistente", 404

### DELETE AN ALBUM ### 
@app.route('/albums/<album_id>', methods=['DELETE'])
def delete_album(album_id):
    album = Album.query.get(album_id)
    if album:
        all_tracks = Track.query.filter_by(album_id = album_id).all()
        for track in all_tracks:
            db.session.delete(track)
            db.session.commit()
        db.session.delete(album)
        db.session.commit()
        return "album eliminado", 204
    else:
        return "album inexistente", 404   

### DELETE A TRACK ### 
@app.route('/tracks/<track_id>', methods=['DELETE'])
def delete_track(track_id):
    track = Track.query.get(track_id)
    if track:
        db.session.delete(track)
        db.session.commit()
        return "canción eliminada", 204
    else:
        return "canción inexistente", 404

######################################  R U N   S E R V E R  #####################################

