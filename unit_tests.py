import os
import unittest
from flask import Flask, request, url_for
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_getIndexPage(self):
        response = self.app.get('/', follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_getMainPage(self):
        response = self.app.get('/main', follow_redirects=True)

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
