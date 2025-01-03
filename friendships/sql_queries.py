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


def is_friend(username, friend_username):
    try: 
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        SELECT username FROM Friendship WHERE (username=%s AND friend_username=%s) OR (username=%s AND friend_username=%s)
    """
        cursor.execute(query, (username, friend_username, friend_username, username))
        friend = cursor.fetchall()
        cursor.close()
        connection.close()
        if friend:
            print("true")
            return True
        else:
            print("false")
            return False
    except Exception as e:
        return False


def create_new_friend_request(username, friend_username):
    try: 
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO Friendship (username, friend_username, date_connected) VALUES (%s, %s, NULL)
    """
        cursor.execute(query, (username, friend_username))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        return False


def get_pending_received_requests(username):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Friendship.username, GROUP_CONCAT(DISTINCT dog_name SEPARATOR ', ') AS dog_names
    FROM Friendship INNER JOIN Dog ON Friendship.username=Dog.username
    WHERE Friendship.friend_username=%s AND date_connected IS NULL
    """
    cursor.execute(query, (username, ))
    requests = cursor.fetchall()
    cursor.close()
    connection.close()
    return requests


def get_pending_sent_requests(username):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT friend_username, GROUP_CONCAT(DISTINCT dog_name SEPARATOR ', ') AS dog_names
    FROM Friendship INNER JOIN Dog ON Friendship.friend_username=Dog.username
    WHERE Friendship.username=%s AND date_connected IS NULL
    GROUP BY friend_username
"""
    cursor.execute(query, (username, ))
    requests = cursor.fetchall()
    cursor.close()
    connection.close()    
    return requests


def accept_friend_request(username, friend_username):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        UPDATE Friendship
        SET date_connected = CURRENT_DATE()
        WHERE username=%s and friend_username=%s
        """
        cursor.execute(query, (friend_username, username))
        print(query)
        query = """
        DELETE FROM Friendship
        WHERE username=%s AND friend_username=%s
"""
        print(query)
        cursor.execute(query, (username, friend_username))
        query = """
        INSERT INTO Friendship (username, friend_username, date_connected) VALUES (%s, %s, CURRENT_DATE())
"""
        print(query)
        cursor.execute(query, (username, friend_username))
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connection.close()


def reject_friend_request(username, friend_username):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        DELETE FROM Friendship
        WHERE username=%s AND friend_username=%s
        """
        cursor.execute(query, (friend_username, username))
        cursor.execute(query, (username, friend_username))
        connection.commit()
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()
        connection.close()


def cancel_friend_request(username, friend_username):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        DELETE FROM Friendship
        WHERE username=%s and friend_username=%s
        """
        cursor.execute(query, (username, friend_username))
        cursor.execute(query, (friend_username, username))
        connection.commit()
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()
        connection.close()