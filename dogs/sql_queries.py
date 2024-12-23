from django.db import connection
import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Scubasteve123!",
        database = "PawsPort"
    )
    return connection

def get_dog(username, dog_name):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT Dog.dog_name, GROUP_CONCAT(DISTINCT breed_name SEPARATOR ' / ') AS breed_names, bio, sex, age 
    FROM Dog INNER JOIN DogBreed ON Dog.username=DogBreed.username AND Dog.dog_name=DogBreed.dog_name 
    WHERE Dog.username=%s AND Dog.dog_name=%s
    GROUP BY Dog.dog_name
"""
    cursor.execute(query, (username, dog_name))
    dog = cursor.fetchone()
    cursor.close()
    connection.close()
    return dog

def get_dogs(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT Dog.dog_name, GROUP_CONCAT(DISTINCT breed_name SEPARATOR ' / ') AS breed_names, sex, age
    FROM Dog INNER JOIN DogBreed ON Dog.username=DogBreed.username AND Dog.dog_name=DogBreed.dog_name 
    WHERE Dog.username=%s
    GROUP BY Dog.dog_name
"""
    cursor.execute(query, (username, ))
    dogs = cursor.fetchall()
    cursor.close()
    connection.close()
    return dogs

def get_dog_list(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT Dog.dog_name, GROUP_CONCAT(DISTINCT breed_name SEPARATOR ' / ') AS breed_names, bio, sex, age 
    FROM Dog INNER JOIN DogBreed ON Dog.username=DogBreed.username AND Dog.dog_name=DogBreed.dog_name 
    WHERE Dog.username!=%s
    GROUP BY Dog.dog_name
    """
    cursor.execute(query, (username, ))
    dogs = cursor.fetchall()
    cursor.close()
    connection.close()
    return dogs

def get_dog_friend_list(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT dog_name, sex, age
    FROM Dog 
    WHERE username IN (SELECT username FROM Friendship WHERE friend_username=%s) OR username IN (SELECT friend_username FROM Friendship WHERE username=%s)
"""
    cursor.execute(query, (username, username, ))
    dogs = cursor.fetchall()
    cursor.close()
    connection.close()
    return dogs

def add_new_dog(username, dog_name, bio, sex, age):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO Dog (dog_name, bio, sex, age, username) VALUES (%s, %s, %s, %s, %s)
    """
        cursor.execute(query, (dog_name, bio, sex, age, username))
        cursor.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        return False