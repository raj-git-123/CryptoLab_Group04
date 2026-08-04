import os
from collections import Counter
from datetime import datetime


def log_activity(option):
    # Create logs folder if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Open log file in append mode
    with open("logs/execution.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {option}\n")


def analyze_file():
    filename = input("Enter filename (e.g., sample1.txt): ")

    # Create file path
    path = os.path.join("datasets", filename)

    # Check if file exists
    if not os.path.exists(path):
        print("File not found!")
        return

    # Read file
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    # Analysis
    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    unique_characters = len(set(text))

    letters = [char.lower() for char in text if char.isalpha()]
    frequency = Counter(letters)

    # Display results
    print("\n========== File Analysis ==========")
    print("Characters        :", characters)
    print("Words             :", words)
    print("Lines             :", lines)
    print("Unique Characters :", unique_characters)

    print("\nLetter Frequency:")
    for letter in sorted(frequency):
        print(f"{letter} : {frequency[letter]}")


# Main Menu
while True:
    print("\n=================================")
    print("        CryptoLabX")
    print("=================================")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        log_activity("Encrypt")
        print("Encrypt - Coming Soon")

    elif choice == "2":
        log_activity("Decrypt")
        print("Decrypt - Coming Soon")

    elif choice == "3":
        log_activity("Attack")
        print("Attack - Coming Soon")

    elif choice == "4":
        log_activity("Analyze")
        analyze_file()

    elif choice == "5":
        log_activity("Exit")
        print("Thank you for using CryptoLabX!")
        break

    else:
        print("Invalid choice! Please try again.")