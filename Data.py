import sqlite3
from flask_restful import Resource

class Data(Resource):

    def get(self):
        try:
            self.sqliteConnection = sqlite3.connect('/opt/nostr-data/nostr.db')
            print('DB Init')
                    
            # Write a query and execute it with cursor
            cursor = self.sqliteConnection.cursor()
            query = "SELECT * FROM event;"
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
        
        finally:
            if self.sqliteConnection:
                self.sqliteConnection.close()
                print('SQLite Connection closed')
        

    def post(self):
        print("ERROR: Post not yet implemented")
        return "ERROR: Post not yet implemented", 500
    
    def delete(self, event_id):
        try:
            self.sqliteConnection = sqlite3.connect('/opt/nostr-data/nostr.db')
            print('DB Init')

            query = 'DELETE FROM tasks WHERE id=?'
            cursor = self.sqliteConnection.cursor()
            cursor.execute(query, (event_id,))
            self.sqliteConnection.commit()
        
        # Handle errors
        except sqlite3.Error as error:
            print(f"Error occurred: {error}", 500)
            return f"Error occurred: {error}", 500
        except Exception as error:
            print(f"Error occurred: {error}", 404)
            return f"Error occurred: {error}", 404

        finally:
            if self.sqliteConnection:
                self.sqliteConnection.close()
                print('SQLite Connection closed')
