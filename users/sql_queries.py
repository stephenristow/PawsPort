from django.db import connection
import mysql.connector

from argon2 import PasswordHasher

ph = PasswordHasher()

def create_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Scubasteve123!",
        database = "PawsPort"
    )
    return connection

def create_user(username, password, email):
    try: 
        password = ph.hash(password)
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO PawsUser (email, pawsword, username) VALUES (%s, %s, %s)
"""
        cursor.execute(query, (email, password, username))
        connection.commit()
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()
        connection.close()


def get_user(username, password):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        SELECT pawsword FROM PawsUser WHERE username=%s
    """
        cursor.execute(query, (username, ))
        hashed_password = cursor.fetchone()[0]
        ph.verify(hashed_password, password)
        cursor.close()
        connection.close()
        return username
    except Exception as e:
        return None


def does_user_exist(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT username FROM PawsUser WHERE username=%s
"""
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user

def does_email_exist(email):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT email FROM PawsUser WHERE email=%s
    """
    cursor.execute(query, (email, ))
    user = cursor.fetchone()

    return False if user is None else True

# def does_password_match(username, password):
#     connection = create_connection()
#     cursor = connection.cursor()
#     query = """
#     SELECT username FROM PawsUser WHERE username=%s and pawsword!=%s
# """
#     cursor.execute(query, (username, password))
#     user = cursor.fetchone()
#     cursor.close()
#     connection.close()

#     return user