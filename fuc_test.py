from app import db
from app.models import User, Post

users = User.query.all()
posts = Post.query.all()

for u in users:
    db.session.delete(u)

for p in posts:
    db.session.delete(p)

db.session.commit()
