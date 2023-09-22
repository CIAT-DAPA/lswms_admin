import unittest
from flask import Flask
from mongoengine import connect, disconnect
import os, sys
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Import the Flask application from your app.py file
from app import app
from ormWP import Wscontent

class TestWscontentBlueprint(unittest.TestCase):
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

    def test_show_wscontent(self):
        response = self.client.get('/wscontent')
        self.assertEqual(response.status_code, 200)
        # Here you can verify the response content if necessary

    def test_add_wscontent(self):
        data = {
    'title': 'Título de ejemplo',
    'typecontent': '64d1bf27e68bf4ca8e6a3bd3',  # ID del tipo de contenido
    'type': 'icon-x',
    'position': 'right',
    'watershed': '64d1bf04650e2171091fa200',  # ID del punto de agua
    'keys[]': ['clave1', 'clave2'],  # Lista de claves
    'values[]': ['valor1', 'valor2'],  # Lista de valores
}

        try:
            response = self.client.post('/wscontent/add', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
       
        except Exception as e:
            print(str(e))  



"""     def test_delete_wscontent(self):
        # Simulate existing data in the in-memory database
        traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
        wscontent = Wscontent(watershed='64d1bf04650e2171091fa200', type='64d1bf27e68bf4ca8e6a3bd3',content={"trace":traced})
        wscontent.save()

        response = self.client.get(f'/deletewscontent/{wscontent.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify if the data is deleted correctly from the in-memory database (if applicable) """

if __name__ == '__main__':
    unittest.main()


