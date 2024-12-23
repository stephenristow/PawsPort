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


def get_pending_received_requests(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = """"
    SELECT username 
    FROM Friendship
    WHERE friend_username=%s AND date_connected IS NULL
    """
    cursor.execute(query, (username, ))
    requests = cursor.fetchall()
    cursor.close()
    connection.close()
    return requests


def get_pending_sent_requests(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT friend_username
    FROM Friendship
    WHERE username=%s AND date_connected IS NULL
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
        query = """
        DELETE FROM Friendship
        WHERE username=%s AND friendship_username=%s
"""
        cursor.execute(query, (username, friend_username))
        query = """
        INSERT INTO Friendship (username, friend_username, date_connected) VALUES (%s, %s, CURRENT_DATE())
"""
        cursor.execute(query, (username, friend_username))
        connection.commit()
        return True
    except Exception as e:
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
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()
        connection.close()