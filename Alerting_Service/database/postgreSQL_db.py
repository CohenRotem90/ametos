import psycopg2
from fastapi import HTTPException
import datetime


class PostgreSQL_db:
    def __init__(self, dbname, user, password, host, port):

        self.connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )

    def send_alert_data(self, table, alert):

        cursor = self.connection.cursor()
        alert_dict = alert.dict()
        columns = ', '.join(alert_dict.keys())
        values = tuple(alert_dict.values())
        query = f"""INSERT INTO {table} ({columns}) VALUES ({', '.join(['%s'] * len(alert_dict))})"""

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except psycopg2.Error as e:
            raise HTTPException(status_code=400, detail="error: " + str(e))
        finally:
            cursor.close()

    def get_data(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if rows and len(columns) != len(rows[0]):
            raise ValueError("Mismatch between column names and row values.")
        result = []
        for row in rows:
            row_dict = dict(zip(columns, row))

            # Handle non-serializable types
            for key, value in row_dict.items():
                if isinstance(value, memoryview):
                    row_dict[key] = value.tobytes().decode("utf-8")
                elif isinstance(value, datetime.datetime):
                    row_dict[key] = value.isoformat()

            result.append(row_dict)
        for item in result:
            item.pop("id", None)

        cursor.close()
        return result

    def is_authorized(self, user_id):
        query = "SELECT is_authorized FROM users_authorization WHERE user_id = %s;"
        params = [user_id]
        data = self.get_data(query, params)
        if len(data) > 0 and len(data[0]) > 0:
            return data[0][0]
        return False

    @staticmethod
    def get_query_syntax_and_params(**kwargs):
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        # Loop through all keyword arguments and check if they are provided
        for field, value in kwargs.items():
            if value:
                # Add condition to query and the value to params
                query += f" AND {field} = %s"
                params.append(value)

        return query, params
