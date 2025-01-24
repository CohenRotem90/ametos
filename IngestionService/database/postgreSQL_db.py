import psycopg2
from fastapi import HTTPException
import datetime


class PostgreSQL_db:
    def __init__(self, dbname, user, password, host, port):
        self.db = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )

    def send_data(self, event):
        cursor = self.db.cursor()
        event_dict = event.dict()
        columns = ', '.join(event_dict.keys())
        values = tuple(event_dict.values())
        query = f"""INSERT INTO events ({columns}) VALUES ({', '.join(['%s'] * len(event_dict))})"""

        try:
            cursor.execute(query, values)
            self.db.commit()
        except psycopg2.Error as e:
            raise HTTPException(status_code=400, detail="error: " + str(e))
        finally:
            cursor.close()

    def get_data(self, query, params):
        cursor = self.db.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if rows and len(columns) != len(rows[0]):
            raise ValueError("Mismatch between column names and row values.")
        result = []
        for row in rows:
            row_dict = dict(zip(columns, row))

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

    @staticmethod
    def get_query_syntax_and_params(start_time, end_time, event_type, device_type):
        query = "SELECT * FROM events WHERE 1=1"
        params = []

        if start_time:
            query += " AND timestamp >= %s"
            params.append(start_time)
        if end_time:
            query += " AND timestamp <= %s"
            params.append(end_time)
        if event_type:
            query += " AND event_type = %s"
            params.append(event_type)
        if device_type:
            query += " AND device_type = %s"
            params.append(device_type)
        return query, params
