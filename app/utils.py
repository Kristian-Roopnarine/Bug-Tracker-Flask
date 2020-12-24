import bcrypt

def create_data(db, models):
    user = models.Users.query.get("1")
    if user is None:
        passwd = bcrypt.hashpw("123".encode('utf-8'),bcrypt.gensalt())
        user = models.Users(
            email = "bob@gmail.com",
            username="bobhenson",
            password=passwd
        )
        db.session.add(user)
        db.session.commit()