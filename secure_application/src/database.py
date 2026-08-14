import sqlite3

DATABASE = "library.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            available INTEGER
        )
    """)

    # Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)

    # Issued books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            book_id INTEGER,
            member_id INTEGER,
            issue_date TEXT
        )
    """)

    # Add sample books
    cursor.execute("SELECT COUNT(*) FROM books")

    if cursor.fetchone()[0] == 0:
        books = [
            (1, "The Alchemist", "Paulo Coelho", 1),
            (2, "Wings of Fire", "A. P. J. Abdul Kalam", 1),
            (3, "1984", "George Orwell", 1),
            (4, "The Great Gatsby", "F. Scott Fitzgerald", 1),
            (5, "Introduction to Algorithms", "Cormen", 1)
        ]

        cursor.executemany(
            "INSERT INTO books VALUES (?, ?, ?, ?)",
            books
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")