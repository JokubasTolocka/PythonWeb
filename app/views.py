from flask import render_template, flash, session, redirect, request
from app import app, models, db, bcrypt
from .forms import Login, Register, Book, Request, Return, ChangePassword
import logging

def authorizedHandler():
    return session.get('isLoggedIn') == True

def unauthorizedHandler():
    return session.get('isLoggedIn') is None or session.get('isLoggedIn') == False

@app.route('/', methods=['GET'])
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if authorizedHandler() == True:
        return redirect('/main')

    form = Login()

    if form.validate_on_submit():
        foundUser = models.User.query.filter_by(username=form.username.data).first()

        if foundUser is None:
            flash('User by the name of %s doesnt exits. You may need to sign up first.'%(form.username.data))
        elif bcrypt.check_password_hash(foundUser.password, form.password.data) == False:
            flash('Wrong password. Try again')
        else:
            session['isLoggedIn'] = True
            session['id'] = foundUser.id
            session['username'] = foundUser.username
            return redirect('/main')

    return render_template('unauthorized/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if authorizedHandler() == True:
        return redirect('/main')

    form = Register()

    if form.validate_on_submit():
        userInDatabase = models.User.query.filter_by(username=form.username.data).first()

        if userInDatabase is None:
            if form.password.data != form.repeatPassword.data:
                flash("The passwords don't match")
            elif form.password.data == form.repeatPassword.data:
                hashedPassword = bcrypt.generate_password_hash(form.password.data)

                newUser = models.User(username = form.username.data, password = hashedPassword, requests = 0)
                db.session.add(newUser)
                db.session.commit() 
                flash("You registered! You can now log in to the library.")
        else:
            app.logger.info('User tried to register with an already existing username') 
            flash("The user with this name already exists in the database")

    return render_template('unauthorized/register.html', form=form)

@app.route('/main', methods=['GET', 'POST'])
def main():
    if unauthorizedHandler() == True:
        return redirect('/')

    currentUsername = session.get('username')

    allBooks = models.Book.query.all()
    form = Request()

    if request.method == 'POST':
        bookToRequestId = form.id.data
        book = models.Book.query.filter_by(id = bookToRequestId).first()

        myUserId = session.get('id')
        myUser = models.User.query.filter_by(id = myUserId).first()

        if myUser is None or book is None or myUser.requests is None:
            app.logger.info('No user or no book') 
            return redirect('/')
        else:
            book.copies = book.copies - 1
            myUser.requests = myUser.requests + 1

            book.owners.append(myUser)
            myUser.books.append(book)
            db.session.commit()

    def checkIfIHaveTheBook(bookId):
        book = models.Book.query.filter_by(id = bookId).first()

        if book.owners is None:
            return False

        myUserId = session.get('id')
        myUserIndexInOwners = next((i for i, item in enumerate(book.owners) if int(item.id) == int(myUserId)), -1)

        if myUserIndexInOwners == -1:
            return False
        
        return True

    allUsers = models.User.query.all()
    usersSortedByRequests = sorted(allUsers, key=lambda x: x.requests, reverse=True)

    return render_template('index.html', username=currentUsername, books=allBooks, form=form, checkIfIHaveTheBook=checkIfIHaveTheBook, usersSortedByRequests = usersSortedByRequests)

@app.route('/mybooks', methods=['GET', 'POST'])
def mybooks():
    if unauthorizedHandler() == True:
        app.logger.info('Unauthorized user tried to reach my books route') 
        return redirect('/')

    myUserId = session.get('id')
    myUser = models.User.query.filter_by(id=myUserId).first()

    form = Return()

    if request.method == 'POST':
        bookToReturnId = form.id.data
        bookInLibrary = models.Book.query.filter_by(id = bookToReturnId).first()

        if myUser is None or bookInLibrary is None or myUser.requests is None:
            return redirect('/')
        else:
            bookInLibrary.copies = bookInLibrary.copies + 1

            myUserIndex = next((i for i, item in enumerate(bookInLibrary.owners) if int(item.id) == int(myUserId)), -1)
            bookInLibrary.owners.pop(myUserIndex)
            db.session.commit()


    return render_template('mybooks.html', books=myUser.books, form=form)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if unauthorizedHandler() == True:
        app.logger.info('Unauthorized user tried to reach create route') 
        return redirect('/')

    currentUsername = session.get('username')

    if currentUsername != 'admin':
        return redirect('/')

    form = Book()

    if form.validate_on_submit():
        newBook = models.Book(title = form.title.data, author = form.author.data, dateReleased = form.dateReleased.data, copies = form.copies.data)
        db.session.add(newBook)
        db.session.commit() 
        return redirect('/')

    return render_template('create.html', form=form)

@app.route('/change', methods=['GET', 'POST'])
def changePassword():
    if unauthorizedHandler() == True:
        app.logger.info('Unauthorized user tried to reach change password route') 
        return redirect('/')

    form = ChangePassword()

    if form.validate_on_submit():

        myUserId = session.get('id')
        myUser = models.User.query.filter_by(id=myUserId).first()

        if form.password.data != form.repeatPassword.data:
            flash("The new passwords don't match")
        elif bcrypt.check_password_hash(myUser.password, form.currentPassword.data) == False:
            flash("Incorrect current password")
        elif form.password.data == form.repeatPassword.data and bcrypt.check_password_hash(myUser.password, form.currentPassword.data) == True:
            hashedPassword = bcrypt.generate_password_hash(form.password.data)

            myUser.password = hashedPassword
            db.session.commit() 
            flash("You password was changed!")

    return render_template('change.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session['isLoggedIn'] = False
    app.logger.info('User logged out') 
    return redirect('/')

