from flask_login import UserMixin
import os
from hashlib import pbkdf2_hmac, sha1
import base64
from models.database import connect_to_postgres, perform_postgres_query
from Crypto.Protocol.KDF import PBKDF2
import json
import hmac
import hashlib

class User(UserMixin):
    def __init__(self, user_obj):
        self.user_obj = user_obj
        self.id = user_obj["email"] 

    @staticmethod
    def get_user_by_username(username):
        postgres_connection = connect_to_postgres()

        query_result = perform_postgres_query(postgres_connection, f"SELECT * FROM user_entity WHERE email = '{username}';")

        if query_result:
            print(f"el query es {query_result}")
            user_id = query_result[0][0]
            email = query_result[0][1]
            user_obj = {'id': user_id, 'email': email}
            print(user_obj)
            return User(user_obj)

        return None

    @staticmethod
    def get_realm_id():
        postgres_connection = connect_to_postgres()

        query_result_realm = perform_postgres_query(postgres_connection, "SELECT * FROM realm WHERE name = 'waterpoints-monitoring';")

        # Verificar si se obtuvo algún resultado
        if query_result_realm:
            id_realm = query_result_realm[0][0]
            return id_realm

        return None

    @staticmethod
    def get_role_id_by_name(realm_id):
        postgres_connection = connect_to_postgres()

        query_result_role = perform_postgres_query(
            postgres_connection,
            f"SELECT * FROM keycloak_role WHERE realm_id = '{realm_id}' AND name = 'admin-webadmin';"
        )


        if query_result_role:
            id_role = query_result_role[0][0]

            return id_role


        return None

    @staticmethod
    def get_user_role_mapping_by_role_id(role_id):
        postgres_connection = connect_to_postgres()

        query_result_user_role_mapping = perform_postgres_query(
            postgres_connection,
            f"SELECT * FROM user_role_mapping WHERE role_id = '{role_id}';"
        )

        if query_result_user_role_mapping:
            return query_result_user_role_mapping

        return None

    @staticmethod
    def check_user_has_role(user_id, query_result_user_role_mapping):
        if any(user_id in role for role in query_result_user_role_mapping):
            return True
        else:
            return False
    @staticmethod
    def get_credentials(id_user):
        postgres_connection = connect_to_postgres()
        query_credentials= perform_postgres_query(postgres_connection, f"SELECT * FROM credential WHERE user_id = '{id_user}';")
        if query_credentials:
            return query_credentials[0]
    @staticmethod
    def verify_password(input_password, user_data):
        user_id, _, _, _, _, _, stored_data, additional_parameters, _ = user_data
        
        stored_data = json.loads(stored_data)
        salt = base64.b64decode(stored_data['salt'])
        stored_hash = base64.b64decode(stored_data['value'])

        if isinstance(additional_parameters, str):
            additional_parameters = json.loads(additional_parameters)

        # Parámetros para PBKDF2
        iterations = additional_parameters.get('hashIterations', 10000)

        derived_key = PBKDF2(input_password.encode('utf-8'), salt, dkLen=len(stored_hash), count=iterations, prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest())

        if derived_key == stored_hash:
            return True
        else:
            return False
        
       
    
    def get_id(self):
        return self.id

