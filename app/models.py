from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), index=True)
    password = db.Column(db.String(500), index=True)
    requests = db.Column(db.Integer)
    books = db.relationship('Book', secondary="loans")


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), index=True)
    author = db.Column(db.String(500), index=True)
    dateReleased = db.Column(db.Date)
    copies = db.Column(db.Integer)
    owners = db.relationship('User', secondary="loans")

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookId = db.Column(db.Integer, db.ForeignKey('books.id'))
    user = db.relationship(User, backref=db.backref("loans", cascade="all, delete-orphan"))
    book = db.relationship(Book, backref=db.backref("loans", cascade="all, delete-orphan"))