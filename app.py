import os
import sys
from flask import Flask, render_template, jsonify, request
import sqlite3

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, 
            template_folder=resource_path('templates'))

def get_puzzle_from_db(min_rating, max_rating):
    db_path = resource_path('puzzles.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = """
        SELECT FEN, Moves, Rating 
        FROM puzzles 
        WHERE Popularity > 80 
        AND Rating BETWEEN ? AND ? 
        ORDER BY RANDOM() LIMIT 1
    """
    cursor.execute(query, (min_rating, max_rating))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "fen": row["FEN"],
            "moves": row["Moves"].split(),
            "rating": row["Rating"]
        }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_puzzle')
def get_puzzle():
    min_r = request.args.get('min', type=int)
    max_r = request.args.get('max', type=int)
    data = get_puzzle_from_db(min_r, max_r)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)