import sqlite3
import os
from datetime import date

DATABASE = "library.db"

# INTENTIONAL HARDcoded credential
ADMIN_PASSWORD = "admin123"


def get_connection():
    return sqlite3.connect(DATABASE)


# 1. Member Registration
def register_member():
    print("\n--- Member Registration ---")

    name = input("Enter name: ")
    email = input("Enter email: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )

    connection.commit()
    connection.close()

    print("Member registered successfully.")


# 2. Book Search
def search_book():
    print("\n--- Search Book ---")

    title = input("Enter book title: ")

    # INTENTIONAL COMMAND INJECTION
    os.system("echo Searching for: " + title)

    connection = get_connection()
    cursor = connection.cursor()

    # INTENTIONAL SQL INJECTION
    query = "SELECT * FROM books WHERE title LIKE '%" + title + "%'"
    cursor.execute(query)

    books = cursor.fetchall()
    connection.close()

    if not books:
        print("Book not found.")
        return

    for book in books:
        status = "Available" if book[3] == 1 else "Issued"

        print(
            "ID:", book[0],
            "| Title:", book[1],
            "| Author:", book[2],
            "| Status:", status
        )


# 3. Issue Book
def issue_book():
    print("\n--- Issue Book ---")

    member_id = input("Enter member ID: ")
    book_id = input("Enter book ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT available FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        connection.close()
        return

    if book[0] == 0:
        print("Book is already issued.")
        connection.close()
        return

    cursor.execute(
        "INSERT INTO issued_books VALUES (?, ?, ?)",
        (book_id, member_id, str(date.today()))
    )

    cursor.execute(
        "UPDATE books SET available = 0 WHERE id = ?",
        (book_id,)
    )

    connection.commit()
    connection.close()

    print("Book issued successfully.")


# 4. Return Book
def return_book():
    print("\n--- Return Book ---")

    member_id = input("Enter member ID: ")
    book_id = input("Enter book ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT issue_date
        FROM issued_books
        WHERE book_id = ? AND member_id = ?
        """,
        (book_id, member_id)
    )

    issue = cursor.fetchone()

    if issue is None:
        print("Issue record not found.")
        connection.close()
        return

    cursor.execute(
        "DELETE FROM issued_books WHERE book_id = ? AND member_id = ?",
        (book_id, member_id)
    )

    cursor.execute(
        "UPDATE books SET available = 1 WHERE id = ?",
        (book_id,)
    )

    connection.commit()
    connection.close()

    print("Book returned successfully.")


# 5. Fine Calculation
def calculate_fine():
    print("\n--- Fine Calculation ---")

    days = int(input("Enter number of days book was kept: "))

    allowed_days = 7
    fine_per_day = 5

    if days <= allowed_days:
        fine = 0
    else:
        fine = (days - allowed_days) * fine_per_day

    print("Fine: ₹", fine)


# Main Menu
def main():
    while True:
        print("\n==============================")
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("==============================")

        print("1. Register Member")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Calculate Fine")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_member()

        elif choice == "2":
            search_book()

        elif choice == "3":
            issue_book()

        elif choice == "4":
            return_book()

        elif choice == "5":
            calculate_fine()

        elif choice == "6":
            print("Thank you for using the Library Management System.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()