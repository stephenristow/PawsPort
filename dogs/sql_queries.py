from django.db import connection
import mysql.connector
import os

def create_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "mysql"),              # ✅ Must match the service name in mysql.yaml
        user=os.environ.get("MYSQLUSER","pawsportuser"),       # ✅ Must match MYSQL_USER from your mysql.yaml
        password=os.environ.get("MYSQL_ROOT_PASSWORD", "pawsportpass"),   # ✅ Must match MYSQL_PASSWORD from your mysql.yaml
        database=os.environ.get("MYSQL_DATABASE", "pawsportdb")      # ✅ Must match MYSQL_DATABASE from your mysql.yaml
    )
    return connection

def get_dog(username, dog_name):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
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
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Dog.username, Dog.dog_name, GROUP_CONCAT(DISTINCT breed_name SEPARATOR ' / ') AS breed_names, sex, age
    FROM Dog INNER JOIN DogBreed ON Dog.username=DogBreed.username AND Dog.dog_name=DogBreed.dog_name 
    WHERE Dog.username=%s
    GROUP BY Dog.username, Dog.dog_name
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
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Dog.username, Dog.dog_name, GROUP_CONCAT(DISTINCT breed_name SEPARATOR ' / ') AS breed_names, sex, age
    FROM Dog INNER JOIN DogBreed ON Dog.username=DogBreed.username AND Dog.dog_name=DogBreed.dog_name
    WHERE Dog.username IN (SELECT username FROM Friendship WHERE friend_username=%s AND date_connected IS NOT NULL) 
    GROUP BY Dog.username, Dog.dog_name
"""
    cursor.execute(query, (username, ))
    dogs = cursor.fetchall()
    cursor.close()
    connection.close()
    return dogs

def add_new_dog(username, dog_name, bio, sex, age, breed_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        dog_query = """
        INSERT INTO Dog (dog_name, bio, sex, age, username) VALUES (%s, %s, %s, %s, %s)
    """
        cursor.execute(dog_query, (dog_name, bio, sex, age, username))
        breed_query = """
        INSERT INTO DogBreed (username, dog_name, breed_name) VALUES (%s, %s, %s)
"""
        cursor.execute(breed_query, (username, dog_name, breed_name))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error occurred: {e}") 
        return False
    
def get_breeds():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM Breed
"""
    cursor.execute(query)
    breeds = cursor.fetchall()
    cursor.close()
    connection.close()
    return breeds
