import sqlite3
from flask_restful import Resource

class Data(Resource):
    def __init__(self):
        # Connect to DB and create a cursor
        self.sqliteConnection = sqlite3.connect('/opt/nostr-data/nostr.db')
        print('DB Init')

    def __del__(self):
        if self.sqliteConnection:
            self.sqliteConnection.close()
            print('SQLite Connection closed')

    def get(self):
        try:        
            # Write a query and execute it with cursor
            cursor = self.sqliteConnection.cursor()
            query = '.dump event;'
            cursor.execute(query)
        
            # Fetch result
            result_data = cursor.fetchall()

            # Close the cursor
            cursor.close()

            return result_data, 200
        
        # Handle errors
        except sqlite3.Error as error:
            print(f"Error occurred: {error}", 500)
            return f"Error occurred: {error}", 500
        

    def post(self):
        print("ERROR: Post not yet implemented")
        return "ERROR: Post not yet implemented", 500
    
    def delete(self, event_id):
        try:
            query = 'DELETE FROM tasks WHERE id=?'
            cursor = self.sqliteConnection.cursor()
            cursor.execute(query, (event_id,))
            self.sqliteConnection.commit()

            result = result_data, 200
        
        # Handle errors
        except sqlite3.Error as error:
            print(f"Error occurred: {error}", 500)
            return f"Error occurred: {error}", 500
        
