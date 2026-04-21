import sqlite3
import os

def run_script(conn, script_path):
    print(f"\n--- Executing Script: {os.path.basename(script_path)} ---")
    with open(script_path, 'r') as f:
        sql_script = f.read()
    
    # Split script into individual queries
    queries = sql_script.split(';')
    cursor = conn.cursor()
    
    for query in queries:
        query = query.strip()
        if not query:
            continue
            
        # Clean query for checking type (remove comments)
        clean_query = ' '.join([line for line in query.split('\n') if not line.strip().startswith('--')]).strip()
        
        print(f"\nExecuting Query:\n{query}")
        try:
            if clean_query.lower().startswith('select'):
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    # Print column names
                    col_names = [description[0] for description in cursor.description]
                    print(" | ".join(col_names))
                    print("-" * (len(" | ".join(col_names)) + 4))
                    for row in results:
                        print(row)
                else:
                    print("No results found.")
            else:
                cursor.execute(query)
                conn.commit()
                print("Query executed successfully.")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

def main():
    db_file = 'student_database.db'
    
    # Remove existing DB if it exists for a fresh start
    if os.path.exists(db_file):
        os.remove(db_file)
        
    conn = sqlite3.connect(db_file)
    
    # Run setup script
    run_script(conn, 'setup_database.sql')
    
    # Run queries script
    run_script(conn, 'queries.sql')
    
    conn.close()
    print("\n--- Database operations complete. ---")

if __name__ == "__main__":
    main()
