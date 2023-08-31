import unittest
from flask import Flask
from mongoengine import connect, disconnect
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Import the Flask application from your app.py file
from app import app
from ormWP import Typecontent

class TesttypecontentBlueprint(unittest.TestCase):
    def setUp(self):
        # Configure the application in testing mode
        app.config['TESTING'] = True
        self.client = app.test_client()
        disconnect(alias='default')
        
        # Connect to the in-memory database
        self.db_name = 'testdb'
        connect(self.db_name, host='mongomock://localhost')

    def tearDown(self):
        # Disconnect from the in-memory database after tests
        disconnect(alias=self.db_name)
        pass  # You can add clean-up logic here if necessary

    def test_show_typecontent(self):
        response = self.client.get('/typecontent')
        self.assertEqual(response.status_code, 200)
        # Here you can verify the response content if necessary

    def test_add_typecontent(self):
        data = {'name': 'content1'}
        response = self.client.post('/typecontent/add', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify if the data is saved in the in-memory database (if applicable)

    def test_edit_typecontent(self):
        # Simulate existing data in the in-memory database
        typecontent = Typecontent(name='content2')
        typecontent.save()

        data = {'name': 'New Name'}
        response = self.client.post(f'/editypecontent/{typecontent.id}', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify if the data is updated correctly in the in-memory database (if applicable)

    def typecontent(self):
        # Simulate existing data in the in-memory database
        typecontent = Typecontent(name='content3',)
        typecontent.save()

        response = self.client.get(f'/deletetypecontnt/{typecontent.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify if the data is deleted correctly from the in-memory database (if applicable)

if __name__ == '__main__':
    unittest.main()
