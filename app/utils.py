import bcrypt

def create_data(db, models):
    user = models.Users.query.get("1")
    if user is None:
        user = models.Users(
            email = "bob@gmail.com",
            username="bobhenson",
            password="123"
        )
        db.session.add(user)
        db.session.commit()