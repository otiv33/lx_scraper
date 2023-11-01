import psycopg2
from psycopg2 import extras

class Db:
    cursor = None
    dbname="sreality"
    user="postgres"
    password="postgres"
    host="postgres-db" # For docker
    port="5432"
            
    def __init__(self) -> None:
        self._connect_db()
        
    def __del__(self):
        if(self.cursor):
            self.cursor.close()

    def _connect_db(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.autocommit = True
        self.cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    def create_db(self):
        conn = psycopg2.connect(
            dbname="postgres",
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        
        conn.autocommit = True
        new_db_name = "sreality"
        create_db_query = f"CREATE DATABASE {new_db_name};"

        try:
            cur = conn.cursor()
            cur.execute(create_db_query)
            print(f"Database '{new_db_name}' created successfully")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS apartments (
                    id SERIAL PRIMARY KEY, 
                    title VARCHAR(255), 
                    image VARCHAR(255)
                );
            """)
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{new_db_name}' already exists")
        finally:
            if 'cur' in locals():
                cur.close()
            conn.close()

    def fill_data(self, results):
        # Clear table
        self.cursor.execute("""
            TRUNCATE TABLE apartments;
        """)
        for result in results:
            self.cursor.execute("""
                INSERT INTO apartments (title, image) VALUES (%s, %s);
            """, (result['title'], result['image']))
        
    def get_apartments(self):
        self.cursor.execute("""
            SELECT * FROM apartments;
        """)
        return self.cursor.fetchall()