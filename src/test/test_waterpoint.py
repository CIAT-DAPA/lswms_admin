import unittest
from flask import Flask
from mongoengine import connect, disconnect
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Import the Flask application from your app.py file
from app import app
from ormWP import Waterpoint

class TestWaterpointBlueprint(unittest.TestCase):
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

    def test_show_waterpoint(self):
        response = self.client.get('/waterpoint')
        self.assertEqual(response.status_code, 200)
        # Here you can verify the response content if necessary

    def test_add_waterpoint(self):
        data = {'name': 'Test waterpoint', 'area': '123','watershed':'64d1bec4f8b9461ac6ed74cc','lat':'123','lon':'123','ext_id':'123'}
        response = self.client.post('/waterpoint/add', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify if the data is saved in the in-memory database (if applicable)


    def test_delete_waterpoint(self):
        # Simulate existing data in the in-memory database
        waterpoint = Waterpoint(name='Test waterpoint', area='123', lat= 3.23, lon=34.3, aclimate_id='',other_attributes=[''],climatology=[''], ext_id='123', trace={},watershed='64d1bec4f8b9461ac6ed74cc')
        waterpoint.save()

        response = self.client.get(f'/deletewaterpoint/{waterpoint.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify if the data is deleted correctly from the in-memory database (if applicable)

if __name__ == '__main__':
    unittest.main()


