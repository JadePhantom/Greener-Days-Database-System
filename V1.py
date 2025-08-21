import sqlite3

con = sqlite3.connect('greener_days.db')
cursor = con.cursor()

def create_tables(): 
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
                    Customer_ID TEXT PRIMARY KEY,
                    Customer_First_Name TEXT,
                    Customer_Last_Name TEXT,
                    Birth_Date DATE,
                    Address TEXT,
                    Customer_Phone TEXT,
                    Email TEXT
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Booking (
                    Booking_ID TEXT PRIMARY KEY,
                    Booking_Date DATE,
                    Total_Cost REAL,
                    Total_Duration INTEGER,
                    Customer_ID TEXT
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Service (
                    Service_ID TEXT PRIMARY KEY,
                    Service_Type TEXT,
                    Service_Cost REAL,
                    Service_Duration INTEGER
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employee (
                    Employee_ID TEXT PRIMARY KEY,
                    Employee_First_Name TEXT,
                    Employee_Last_Name TEXT,
                    Employee_Phone TEXT
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment (
                    Payment_ID TEXT PRIMARY KEY,
                    Payment_Method TEXT,
                    Payment_Completed BOOLEAN,
                    Booking_ID TEXT
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Job (
                    Job_ID TEXT PRIMARY KEY,
                    Job_Date DATE,
                    Job_Completed BOOLEAN,
                    Service_ID TEXT,
                    Employee_ID TEXT
                    )''')
    
    con.commit()

def display_menu():
    print("Booking System Database Interface")
    print("1. Add New Record")
    print("2. View Records")
    print("3. Update Record")
    print("4. Delete Record")
    print("5. Exit")

def add_record():
    pass

def view_records():
    pass

def update_record():
    pass
        
def delete_record():
    pass

def main():
    create_tables()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_record()
        elif choice == '2':
            view_records()
        elif choice == '3':
            update_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
    
    con.close()

main()