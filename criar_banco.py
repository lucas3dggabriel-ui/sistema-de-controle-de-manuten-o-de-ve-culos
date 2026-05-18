import sqlite3

def configurar():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY,
        modelo TEXT NOT NULL,
        placa TEXT NOT NULL UNIQUE,
        ano INTEGER
    )
    """)
    conn.commit()
    conn.close()
    print("Banco de dados e tabelas prontos!")
configurar()
    
