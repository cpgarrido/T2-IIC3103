from app import app, db
######################################  R U N   S E R V E R  #####################################
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)