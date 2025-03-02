import json
import datetime
import os

# Load books data from JSON file(books.json)
def load_books():
    with open("books.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Save the updated books data back to JSON file
def save_books(books):
    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)

# Save transaction log tied to user ID
def save_log(user_id, user_name, log_data):
    file_name = f"{user_id}_transaction_log.txt"
    with open(file_name, "a", encoding="utf-8") as log_file:
        log_file.write(log_data)

# Save the daily library transaction log
def save_daily_log(transaction_data):
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f"library_transactions_{current_date}.txt"
    with open(file_name, "a", encoding="utf-8") as daily_log:
        daily_log.write(transaction_data)

# Borrow a book
def borrow_book():
    user_name = input("Enter your name: ")
    user_id = input("Enter your library ID: ")
    books = load_books()
    title = input("Enter the book title to borrow: ")
    
    if title in books and books[title]["available"]:
        books[title]["available"] = False
        borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Current date as borrow date
        books[title]["borrow_date"] = borrow_date
        transaction = f"{datetime.datetime.now()}: {user_name} (ID: {user_id}) borrowed '{title}' on {borrow_date}\n"
        save_log(user_id, user_name, transaction)
        save_daily_log(transaction)  # Save to daily log
        save_books(books)
        print(f"{user_name}, you have successfully borrowed '{title}'!")
    else:
        print("The book is either unavailable or doesn't exist.")
        print("Enter Correct Book Title")

# Return a book
def return_book():
    user_name = input("Enter your name: ")
    user_id = input("Enter your library ID: ")
    books = load_books()
    title = input("Enter the book title to return: ")
    
    if title in books and not books[title]["available"]:
        borrow_date = datetime.datetime.strptime(books[title]["borrow_date"], "%Y-%m-%d")
        return_date = datetime.datetime.now()
        overdue_days = (return_date - borrow_date).days
        
        fine = calculate_fine(overdue_days)
        books[title]["available"] = True
        transaction = f"{datetime.datetime.now()}: {user_name} (ID: {user_id}) returned '{title}', Fine: ₹{fine}, Borrowed on: {borrow_date}\n"
        save_log(user_id, user_name, transaction)
        save_daily_log(transaction)  # Save to daily log
        save_books(books)
        print(f"{user_name}, you have successfully returned '{title}'. \n Fine: ₹{fine}")
    else:
        print("This book wasn't borrowed or doesn't exist.")

# Calculate fine based on overdue days
def calculate_fine(overdue_days):
    fine_per_day = 5  # ₹5 per day
    if overdue_days > 0:
        fine = overdue_days * fine_per_day
        return fine
    return 0  # No fine if not overdue

# Search and filter books by title, author, or genre
def search_books(books, search_term, filter_type):
    results = []
    for book, details in books.items():
        if filter_type == "title" and search_term.lower() in book.lower():
            results.append({book: details})
        elif filter_type == "author" and search_term.lower() in details["author"].lower():
            results.append({book: details})
        elif filter_type == "genre" and search_term.lower() in details["genre"].lower():
            results.append({book: details})
    return results

# Display books
def display_books(books):
    for book, details in books.items():
        print(f"\nTitle: {book}")
        print(f"Author: {details['author']}")
        print(f"ISBN: {details['isbn']}")
        print(f"Genre: {details['genre']}")
        print(f"Price: {details['price']}")
        print(f"Age Recommendation: {details['age_recommendation']}")
        print(f"Available: {'Yes' if details['available'] else 'No'}")

# Function to search and filter books
def search_filter_books():
    books = load_books()
    print("\nSearch and Filter Books")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by Genre")
    choice = input("Please Choose an option (1/2/3): ")

    if choice == "1":
        search_term = input("Enter book title to search: ")
        results = search_books(books, search_term, "title")
    elif choice == "2":
        search_term = input("Enter author name to search: ")
        results = search_books(books, search_term, "author")
    elif choice == "3":
        search_term = input("Enter genre to search: ")
        results = search_books(books, search_term, "genre")
    else:
        print("Invalid choice. Please try again.")
        return

    if results:
        print("\nSearch Results:")
        for result in results:
            for book, details in result.items():
                print(f"\nTitle: {book}")
                print(f"Author: {details['author']}")
                print(f"ISBN: {details['isbn']}")
                print(f"Genre: {details['genre']}")
                print(f"Price: {details['price']}")
                print(f"Age Recommendation: {details['age_recommendation']}")
                print(f"Available: {'Yes' if details['available'] else 'No'}")
    else:
        print("\nNo books found matching your search.")

# Show user's transaction history
def show_my_account():
    user_id = input("Enter your library ID to view transaction history: ")
    file_name = f"{user_id}_transaction_log.txt"
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as log_file:
            print("\nYour Transaction History:")
            print(log_file.read())
    else:
        print("No transaction history found for your account.")

# Show daily transaction log for the library
def show_daily_log():
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f"library_transactions_{current_date}.txt"
    
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as log_file:
            print("\nLibrary Daily Transaction Log:")
            print(log_file.read())
    else:
        print("No transactions have been recorded for today.")

# Main function
def main():
    while True:
        print("\n Welcome To Our Digital Library Management System")
        print("@ruby-library")
        print("1. Display all books in thr library")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search and Filter Books")
        print("5. Show My Personal Account (Transaction History)")
        print("6. View Library Daily Transaction Log")
        print("7. Exit")
        
        choice = input("Kindly enter your choice: ")

        if choice == "1":
            books = load_books()
            display_books(books)
        elif choice == "2":
            borrow_book()
        elif choice == "3":
            return_book()
        elif choice == "4":
            search_filter_books()
        elif choice == "5":
            show_my_account()
        elif choice == "6":
            show_daily_log()
        elif choice == "7":
            print("Thank you for visiting our Digital Library ")
            print("@ruby-library")
            print("Exiting Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()