import sqlite3

con = sqlite3.connect('greener_days.db')
cursor = con.cursor()
cursor.execute("DROP TABLE IF EXISTS Customer")
cursor.execute("DROP TABLE IF EXISTS Booking")
cursor.execute("DROP TABLE IF EXISTS Service")
cursor.execute("DROP TABLE IF EXISTS Job")
cursor.execute("DROP TABLE IF EXISTS Employee")
cursor.execute("DROP TABLE IF EXISTS Payment")
con.commit()

def create_tables(): 
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
                    Customer_ID TEXT PRIMARY KEY CHECK (Customer_ID GLOB 'C[0-9][0-9][0-9][0-9][0-9]'),
                    Customer_First_Name TEXT NOT NULL CHECK (Customer_First_Name GLOB '[A-Za-z]*'),
                    Customer_Last_Name TEXT NOT NULL CHECK (Customer_Last_Name GLOB '[A-Za-z]*'),
                    Birth_Date DATE NOT NULL CHECK (Birth_Date LIKE '__/__/____'),
                    Address TEXT NOT NULL,
                    Customer_Phone TEXT NOT NULL UNIQUE CHECK (Customer_Phone GLOB '04[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
                    Email TEXT NOT NULL UNIQUE CHECK (Email LIKE '%@%.%') 
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Booking (
                    Booking_ID TEXT PRIMARY KEY CHECK (Booking_ID GLOB 'B[0-9][0-9][0-9][0-9][0-9]'),
                    Booking_Date DATE NOT NULL CHECK (Booking_Date LIKE '__/__/____'),
                    Total_Cost REAL NOT NULL CHECK (Total_Cost = ROUND(Total_Cost, 2)),
                    Total_Duration INTEGER NOT NULL CHECK (typeof(Total_Duration) = 'integer'),
                    Customer_ID TEXT NOT NULL,
                    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
                    UNIQUE (Booking_Date, Customer_ID)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Service (
                    Service_ID TEXT PRIMARY KEY CHECK (Service_ID GLOB 'S[0-9][0-9][0-9][0-9][0-9]'),
                    Service_Type TEXT NOT NULL UNIQUE CHECK (Service_Type GLOB '[A-Za-z ]*'),
                    Service_Cost REAL NOT NULL CHECK (Service_Cost = ROUND(Service_Cost, 2)),
                    Service_Duration INTEGER NOT NULL CHECK (typeof(Service_Duration) = 'integer')
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employee (
                    Employee_ID TEXT PRIMARY KEY CHECK (Employee_ID GLOB 'J[0-9][0-9][0-9][0-9][0-9]'),
                    Employee_First_Name TEXT NOT NULL CHECK (Employee_First_Name GLOB '[A-Za-z]*'),
                    Employee_Last_Name TEXT NOT NULL CHECK (Employee_Last_Name GLOB '[A-Za-z]*'),
                    Employee_Phone TEXT NOT NULL UNIQUE CHECK (Employee_Phone GLOB '04[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') 
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment (
                    Payment_ID TEXT PRIMARY KEY CHECK (Payment_ID GLOB 'J[0-9][0-9][0-9][0-9][0-9]'),
                    Payment_Method TEXT NOT NULL CHECK (Payment_Method GLOB '[A-Za-z ]*'),
                    Payment_Completed BOOLEAN NOT NULL CHECK (Payment_Completed IN (True, False)),
                    Booking_ID TEXT NOT NULL,
                    FOREIGN KEY (Booking_ID) REFERENCES Booking(Booking_ID),
                    UNIQUE (Booking_ID, Payment_Method)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Job (
                    Job_ID TEXT PRIMARY KEY CHECK (Job_ID GLOB 'J[0-9][0-9][0-9][0-9][0-9]'),
                    Job_Date DATE NOT NULL CHECK (Job_Date LIKE '__/__/____'),
                    Job_Completed BOOLEAN NOT NULL CHECK (Job_Completed IN (True, False)),                        
                    Service_ID TEXT NOT NULL,
                    Employee_ID TEXT NOT NULL,
                    FOREIGN KEY (Service_ID) REFERENCES Service(Service_ID),
                    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
                    UNIQUE (Job_Date, Service_ID, Employee_ID)
                    )''')
    
    cursor.execute("PRAGMA foreign_keys = ON")
    con.commit()

def display_menu():
    print("\nBooking System Database Interface")
    print("1. Add New Record")
    print("2. View Records")
    print("3. Update Record")
    print("4. Delete Record")
    print("5. Exit")

def add_record():
    print("\nSelect Table to Add Record:")
    print("1. Customer")
    print("2. Booking")
    print("3. Service")
    print("4. Employee")
    print("5. Payment")
    print("6. Jobs")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == '1':  
        customer_id = input("Customer ID: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        birth_date = input("Birth Date (DD/MM/YYYY): ")
        address = input("Address: ")
        phone = input("Phone: ")
        email = input("Email: ")
        try:
            cursor.execute('''INSERT INTO Customer (Customer_ID, Customer_First_Name, Customer_Last_Name, 
                            Birth_Date, Address, Customer_Phone, Email) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                            (customer_id, first_name, last_name, birth_date, address, phone, email))
            con.commit()
            print("Customer added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding customer: {e}")
        
    elif choice == '2':  
        booking_id = input("Booking ID: ")
        booking_date = input("Booking Date (DD/MM/YYYY): ")
        total_cost = input("Total Cost: ")
        total_duration = input("Total Duration: ")
        customer_id = input("Customer ID: ")
        try:
            cursor.execute('''INSERT INTO Booking (Booking_ID, Booking_Date, Total_Cost, Total_Duration, Customer_ID) 
                            VALUES (?, ?, ?, ?, ?)''', (booking_id, booking_date, total_cost, total_duration, customer_id))
            con.commit()
            print("Booking added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding booking: {e}")
        
    elif choice == '3': 
        service_id = input("Service ID: ")
        service_type = input("Service Type: ")
        service_cost = input("Service Cost: ")
        service_duration = input("Service Duration (minutes): ")
        try:
            cursor.execute('''INSERT INTO Service (Service_ID, Service_Type, Service_Cost, Service_Duration) 
                            VALUES (?, ?, ?, ?)''', (service_id, service_type, service_cost, service_duration))
            con.commit()
            print("Service added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding service: {e}")
        
    elif choice == '4':  
        employee_id = input("Employee ID: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        phone = input("Phone: ")
        try:
            cursor.execute('''INSERT INTO Employee (Employee_ID, Employee_First_Name, Employee_Last_Name, Employee_Phone) 
                            VALUES (?, ?, ?, ?)''', (employee_id, first_name, last_name, phone))
            con.commit()
            print("Employee added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding employee: {e}")
        
    elif choice == '5':  
        payment_id = input("Payment ID: ")
        payment_method = input("Payment Method: ")
        payment_status = input("Payment Status: ")
        booking_id = input("Booking ID: ")
        try:
            cursor.execute('''INSERT INTO Payment (Payment_ID, Payment_Method, Payment_Status, Booking_ID) 
                            VALUES (?, ?, ?, ?)''', (payment_id, payment_method, payment_status, booking_id))
            con.commit()
            print("Payment added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding payment: {e}")
        
    elif choice == '6':  
        job_id = input("Job ID: ")
        service_id = input("Service ID: ")
        employee_id = input("Employee ID: ")
        try:
            cursor.execute('''INSERT INTO Jobs (Job_ID, Service_ID, Employee_ID) 
                            VALUES (?, ?, ?)''', (job_id, service_id, employee_id))
            con.commit()
            print("Job added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding job: {e}")
        
    elif choice == '7':
        return
    else:
        print("Invalid choice. Please try again.")

def view_records():
    print("\nSelect Table to View Records:")
    print("1. Customer")
    print("2. Booking")
    print("3. Service")
    print("4. Employee")
    print("5. Payment")
    print("6. Jobs")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == '1': 
        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()
        print("\nCustomer Records:")
        print("ID | First Name | Last Name | Birth Date | Address | Phone | Email")
        for row in rows:
            print(row)
            
    elif choice == '2':  
        cursor.execute("SELECT * FROM Booking")
        rows = cursor.fetchall()
        print("\nBooking Records:")
        print("ID | Booking Date | Customer ID")
        for row in rows:
            print(row)
            
    elif choice == '3':  
        cursor.execute("SELECT * FROM Service")
        rows = cursor.fetchall()
        print("\nService Records:")
        print("ID | Service Type | Price | Duration")
        for row in rows:
            print(row)
            
    elif choice == '4':  
        cursor.execute("SELECT * FROM Employee")
        rows = cursor.fetchall()
        print("\nEmployee Records:")
        print("ID | First Name | Last Name | Phone")
        for row in rows:
            print(row)
            
    elif choice == '5':  
        cursor.execute("SELECT * FROM Payment")
        rows = cursor.fetchall()
        print("\nPayment Records:")
        print("ID | Method | Status | Booking ID")
        for row in rows:
            print(row)
            
    elif choice == '6': 
        cursor.execute("SELECT * FROM Jobs")
        rows = cursor.fetchall()
        print("\nJobs Records:")
        print("ID | Service ID | Employee ID")
        for row in rows:
            print(row)
            
    elif choice == '7':
        return
    else:
        print("Invalid choice. Please try again.")

def update_record():
    print("\nSelect Table to Update Record:")
    print("1. Customer")
    print("2. Booking")
    print("3. Service")
    print("4. Employee")
    print("5. Payment")
    print("6. Jobs")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == '1':  
        customer_id = input("Enter Customer ID to update: ")
        new_customer_id = input("New Customer ID (leave blank to keep current): ")
        first_name = input("New First Name (leave blank to keep current): ")
        last_name = input("New Last Name (leave blank to keep current): ")
        birth_date = input("New Birth Date (DD/MM/YYYY, leave blank to keep current): ")
        address = input("New Address (leave blank to keep current): ")
        phone = input("New Phone (leave blank to keep current): ")
        email = input("New Email (leave blank to keep current): ")

        cursor.execute("SELECT * FROM Customer WHERE Customer_ID=?", (customer_id,))
        current = cursor.fetchone()
        if not current:
            print("Customer not found!")
            return

        updates = []
        params = []

        if new_customer_id:
            updates.append("Customer_ID=?")
            params.append(new_customer_id)
        if first_name:
            updates.append("Customer_First_Name=?")
            params.append(first_name)
        if last_name:
            updates.append("Customer_Last_Name=?")
            params.append(last_name)
        if birth_date:
            updates.append("Birth_Date=?")
            params.append(birth_date)
        if address:
            updates.append("Address=?")
            params.append(address)
        if phone:
            updates.append("Customer_Phone=?")
            params.append(phone)
        if email:
            updates.append("Email=?")
            params.append(email)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Customer SET " + ", ".join(updates) + " WHERE Customer_ID=?"
        params.append(customer_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Customer updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error updating customer: {e}")
        
    elif choice == '2':  
        booking_id = input("Enter Booking ID to update: ")
        new_booking_id = input("New Booking ID (leave blank to keep current): ")
        booking_date = input("New Booking Date (YYYY-MM-DD, leave blank to keep current): ")
        customer_id = input("New Customer ID (leave blank to keep current): ")

        updates = []
        params = []

        if new_booking_id:
            updates.append("Booking_ID=?")
            params.append(new_booking_id)
        if booking_date:
            updates.append("Booking_Date=?")
            params.append(booking_date)
        if customer_id:
            updates.append("Customer_ID=?")
            params.append(customer_id)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Booking SET " + ", ".join(updates) + " WHERE Booking_ID=?"
        params.append(booking_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Booking updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error updating booking: {e}")
        
    elif choice == '3':  
        service_id = input("Enter Service ID to update: ")
        new_service_id = input("New Service ID (leave blank to keep current): ")
        service_type = input("New Service Type (leave blank to keep current): ")
        service_price = input("New Service Price (leave blank to keep current): ")
        service_duration = input("New Service Duration (leave blank to keep current): ")

        updates = []
        params = []

        if new_service_id:
            updates.append("Service_ID=?")
            params.append(new_service_id)
        if service_type:
            updates.append("Service_Type=?")
            params.append(service_type)
        if service_price:
            updates.append("Service_Price=?")
            params.append(service_price)
        if service_duration:
            updates.append("Service_Duration=?")
            params.append(service_duration)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Service SET " + ", ".join(updates) + " WHERE Service_ID=?"
        params.append(service_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Service updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error updating service: {e}")
        
    elif choice == '4':  
        employee_id = input("Enter Employee ID to update: ")
        new_employee_id = input("New Employee ID (leave blank to keep current): ")
        first_name = input("New First Name (leave blank to keep current): ")
        last_name = input("New Last Name (leave blank to keep current): ")
        phone = input("New Phone (leave blank to keep current): ")

        updates = []
        params = []

        if new_employee_id:
            updates.append("Employee_ID=?")
            params.append(new_employee_id)
        if first_name:
            updates.append("Employee_First_Name=?")
            params.append(first_name)
        if last_name:
            updates.append("Employee_Last_Name=?")
            params.append(last_name)
        if phone:
            updates.append("Employee_Phone=?")
            params.append(phone)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Employee SET " + ", ".join(updates) + " WHERE Employee_ID=?"
        params.append(employee_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Employee updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error updating employee: {e}")
        
    elif choice == '5':  
        payment_id = input("Enter Payment ID to update: ")
        new_payment_id = input("New Payment ID (leave blank to keep current): ")
        payment_method = input("New Payment Method (leave blank to keep current): ")
        payment_status = input("New Payment Status (leave blank to keep current): ")
        booking_id = input("New Booking ID (leave blank to keep current): ")

        updates = []
        params = []

        if new_payment_id:
            updates.append("Payment_ID=?")
            params.append(new_payment_id)
        if payment_method:
            updates.append("Payment_Method=?")
            params.append(payment_method)
        if payment_status:
            updates.append("Payment_Status=?")
            params.append(payment_status)
        if booking_id:
            updates.append("Booking_ID=?")
            params.append(booking_id)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Payment SET " + ", ".join(updates) + " WHERE Payment_ID=?"
        params.append(payment_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Payment updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error updating payment: {e}")
        
    elif choice == '6':  
        job_id = input("Enter Job ID to update: ")
        new_job_id = input("New Job ID (leave blank to keep current): ")
        service_id = input("New Service ID (leave blank to keep current): ")
        employee_id = input("New Employee ID (leave blank to keep current): ")

        updates = []
        params = []

        if new_job_id:
            updates.append("Job_ID=?")
            params.append(new_job_id)
        if service_id:
            updates.append("Service_ID=?")
            params.append(service_id)
        if employee_id:
            updates.append("Employee_ID=?")
            params.append(employee_id)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Jobs SET " + ", ".join(updates) + " WHERE Job_ID=?"
        params.append(job_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Job updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error updating job: {e}")
        
    elif choice == '7':
        return
    else:
        print("Invalid choice. Please try again.")

def delete_record():
    print("\nSelect Table to Delete Record From:")
    print("1. Customer")
    print("2. Booking")
    print("3. Service")
    print("4. Employee")
    print("5. Payment")
    print("6. Jobs")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == '1':  
        customer_id = input("Enter Customer ID to delete: ")
        cursor.execute("DELETE FROM Customer WHERE Customer_ID=?", (customer_id,))
        con.commit()
        print("Customer deleted successfully!")
        
    elif choice == '2': 
        booking_id = input("Enter Booking ID to delete: ")
        cursor.execute("DELETE FROM Booking WHERE Booking_ID=?", (booking_id,))
        con.commit()
        print("Booking deleted successfully!")
        
    elif choice == '3':  
        service_id = input("Enter Service ID to delete: ")
        cursor.execute("DELETE FROM Service WHERE Service_ID=?", (service_id,))
        con.commit()
        print("Service deleted successfully!")
        
    elif choice == '4':  
        employee_id = input("Enter Employee ID to delete: ")
        cursor.execute("DELETE FROM Employee WHERE Employee_ID=?", (employee_id,))
        con.commit()
        print("Employee deleted successfully!")
        
    elif choice == '5':  
        payment_id = input("Enter Payment ID to delete: ")
        cursor.execute("DELETE FROM Payment WHERE Payment_ID=?", (payment_id,))
        con.commit()
        print("Payment deleted successfully!")
        
    elif choice == '6':  
        job_id = input("Enter Job ID to delete: ")
        cursor.execute("DELETE FROM Jobs WHERE Job_ID=?", (job_id,))
        con.commit()
        print("Job deleted successfully!")
        
    elif choice == '7':
        return
    else:
        print("Invalid choice. Please try again.")

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

if __name__ == "__main__":
    main()