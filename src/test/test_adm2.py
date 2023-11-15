import unittest
from flask import Flask
from mongoengine import connect, disconnect
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Import the Flask application from your app.py file
from app import app
from ormWP import Adm2

class TestAdm2Blueprint(unittest.TestCase):
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

    def test_show_adm3(self):
        response = self.client.get('/adm2')
        self.assertEqual(response.status_code, 401)
        # Here you can verify the response content if necessary

    def test_add_adm2(self):
        data = {'name': 'Test Adm2', 'ext_id': '123','adm1':'64d1bec4f8b9461ac6ed74cc'}
        response = self.client.post('/adm2/add', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        # Verify if the data is saved in the in-memory database (if applicable)


    def test_delete_adm2(self):
        # Simulate existing data in the in-memory database
        adm2 = Adm2(name='Test Adm1', ext_id='123', trace={},adm1='64d1bec4f8b9461ac6ed74cc')
        adm2.save()

        response = self.client.get(f'/deleteadm2/{adm2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        # Verify if the data is deleted correctly from the in-memory database (if applicable)

if __name__ == '__main__':
    unittest.main()
