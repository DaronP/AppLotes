import pymysql


def execute_query(conn, query, params=None):
    with conn.cursor() as cursor:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
    return result

def execute_non_query(conn, query, params=None):
    with conn.cursor() as cursor:
        cursor.execute(query, params or ())
    conn.commit()