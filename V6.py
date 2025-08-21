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
                    Customer_ID TEXT NOT NULL,
                    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
                    UNIQUE (Booking_Date, Customer_ID)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Service (
                    Service_ID TEXT PRIMARY KEY CHECK (Service_ID GLOB 'S[0-9][0-9][0-9][0-9][0-9]'),
                    Service_Type TEXT NOT NULL UNIQUE CHECK (Service_Type GLOB '[A-Za-z ]*'),
                    Service_Cost REAL NOT NULL CHECK (Service_Cost = ROUND(Service_Cost, 2)),
                    Service_Duration INTEGER NOT NULL CHECK (typeof(Service_Duration) = 'integer'),
                    Booking_ID TEXT NOT NULL,
                    FOREIGN KEY (Booking_ID) REFERENCES Booking(Booking_ID)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employee (
                    Employee_ID TEXT PRIMARY KEY CHECK (Employee_ID GLOB 'E[0-9][0-9][0-9][0-9][0-9]'),
                    Employee_First_Name TEXT NOT NULL CHECK (Employee_First_Name GLOB '[A-Za-z]*'),
                    Employee_Last_Name TEXT NOT NULL CHECK (Employee_Last_Name GLOB '[A-Za-z]*'),
                    Employee_Phone TEXT NOT NULL UNIQUE CHECK (Employee_Phone GLOB '04[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') 
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment (
                    Payment_ID TEXT PRIMARY KEY CHECK (Payment_ID GLOB 'P[0-9][0-9][0-9][0-9][0-9]'),
                    Payment_Method TEXT NOT NULL CHECK (Payment_Method GLOB '[A-Za-z ]*'),
                    Payment_Status TEXT NOT NULL CHECK (Payment_Status IN ('Paid', 'Unpaid', 'Partially Paid')),
                    Booking_ID TEXT NOT NULL,
                    FOREIGN KEY (Booking_ID) REFERENCES Booking(Booking_ID),
                    UNIQUE (Booking_ID, Payment_Method)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Job (
                    Job_ID TEXT PRIMARY KEY CHECK (Job_ID GLOB 'J[0-9][0-9][0-9][0-9][0-9]'),
                    Job_Date DATE NOT NULL CHECK (Job_Date LIKE '__/__/____'),
                    Job_Status TEXT NOT NULL CHECK (Job_Status IN ('Finished', 'Not Started', 'In Progress')),                        
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
    print("5. Reports")
    print("6. Exit")

def add_record():
    print("\nSelect Table to Add Record:")
    print("1. Customer")
    print("2. Booking")
    print("3. Service")
    print("4. Employee")
    print("5. Payment")
    print("6. Job")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == '1':  
        customer_id = input("Customer ID (CXXXXX): ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        birth_date = input("Birth Date (DD/MM/YYYY): ")
        address = input("Address: ")
        phone = input("Phone (04XXXXXXXX): ")
        email = input("Email (local-part@domain.tld): ")
        try:
            cursor.execute('''INSERT INTO Customer (Customer_ID, Customer_First_Name, Customer_Last_Name, 
                            Birth_Date, Address, Customer_Phone, Email) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                            (customer_id, first_name, last_name, birth_date, address, phone, email))
            con.commit()
            print("Customer added successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not add customer record.")
            if "UNIQUE constraint failed" in str(e):
                print("Customer ID, phone, or email must be unique. The value/s you entered already exists.")
            elif "CHECK constraint failed: Customer.Customer_ID" in str(e):
                print("Customer ID must start with 'C' followed by 5 digits (e.g., C12345).")
            elif "CHECK constraint failed: Customer.Customer_First_Name" in str(e):
                print("First Name must contain only letters.")
            elif "CHECK constraint failed: Customer.Customer_Last_Name" in str(e):
                print("Last Name must contain only letters.")
            elif "CHECK constraint failed: Customer.Birth_Date" in str(e):
                print("Birth Date must be in DD/MM/YYYY format. (e.g., 04/05/2008)")
            elif "CHECK constraint failed: Customer.Customer_Phone" in str(e):
                print("Phone must start with '04' and be followed by 8 digits (e.g., 0405200867).")
            elif "CHECK constraint failed: Customer.Email" in str(e):
                print("Email must be in local-part@domain.tld format (e.g., john@gmail.com).")
            else:
                print(f"Database error: {e}")
        
    elif choice == '2':  
        booking_id = input("Booking ID (BXXXXX): ")
        booking_date = input("Booking Date (DD/MM/YYYY): ")
        customer_id = input("Customer ID: ")
        try:
            cursor.execute('''INSERT INTO Booking (Booking_ID, Booking_Date, Customer_ID) 
                            VALUES (?, ?, ?)''', (booking_id, booking_date, customer_id))
            con.commit()
            print("Booking added successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not add booking record.")
            if "UNIQUE constraint failed" in str(e):
                print("Booking ID must be unique, and/or a customer cannot have two bookings on the same date.")
            elif "CHECK constraint failed: Booking.Booking_ID" in str(e):
                print("Booking ID must start with 'B' followed by 5 digits (e.g., B12345).")
            elif "CHECK constraint failed: Booking.Booking_Date" in str(e):
                print("Booking Date must be in DD/MM/YYYY format. (e.g., 04/05/2008)")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Customer ID does not exist. Please enter a valid Customer ID.")
            else:
                print(f"Database error: {e}")
        
    elif choice == '3':  
        service_id = input("Service ID (SXXXXX): ")
        service_type = input("Service Type: ")
        service_cost = input("Service Cost (XX.XX): ")
        service_duration = input("Service Duration (mins): ")
        booking_id = input("Booking ID: ")
        try:
            cursor.execute('''INSERT INTO Service (Service_ID, Service_Type, Service_Cost, Service_Duration, Booking_ID) 
                            VALUES (?, ?, ?, ?, ?)''', (service_id, service_type, service_cost, service_duration, booking_id))
            con.commit()
            print("Service added successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not add service record.")
            if "UNIQUE constraint failed" in str(e):
                print("Service ID and Service Type must be unique. The value/s you entered already exists.")
            elif "CHECK constraint failed" in str(e):
                print("One of the following constraints has failed:")
                print("Service ID must start with 'S' followed by 5 digits (e.g., S12345).")
                print("Service Type must contain only letters and spaces.")
                print("Service Cost must be a number to 2 decimal places. (e.g., 100.00)")
                print("Service Duration must be a positive integer.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Booking ID does not exist. Please enter a valid Booking ID.")
            else:
                print(f"Database error: {e}")
        
    elif choice == '4':  
        employee_id = input("Employee ID (EXXXXX): ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        phone = input("Phone (04XXXXXXXX): ")
        try:
            cursor.execute('''INSERT INTO Employee (Employee_ID, Employee_First_Name, Employee_Last_Name, Employee_Phone) 
                            VALUES (?, ?, ?, ?)''', (employee_id, first_name, last_name, phone))
            con.commit()
            print("Employee added successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not add employee record.")
            if "UNIQUE constraint failed" in str(e):
                print("Employee ID and phone must be unique. The value/s you entered already exists.")
            elif "CHECK constraint failed: Employee.Employee_ID" in str(e):
                print("Employee ID must start with 'E' followed by 5 digits (e.g., E12345).")
            elif "CHECK constraint failed: Employee.Employee_First_Name" in str(e):
                print("First Name must contain only letters.")
            elif "CHECK constraint failed: Employee.Employee_Last_Name" in str(e):
                print("Last Name must contain only letters.")
            elif "CHECK constraint failed: Employee.Employee_Phone" in str(e):
                print("Phone must start with '04' and be followed by 8 digits. (e.g., 0405200867).")
            else:
                print(f"Database error: {e}")
        
    elif choice == '5':  
        payment_id = input("Payment ID (PXXXXX): ")
        payment_method = input("Payment Method: ")
        payment_status = input("Payment Status (Paid/Unpaid/Partially Paid): ")
        booking_id = input("Booking ID: ")
        try:
            cursor.execute('''INSERT INTO Payment (Payment_ID, Payment_Method, Payment_Status, Booking_ID) 
                            VALUES (?, ?, ?, ?)''', (payment_id, payment_method, payment_status, booking_id))
            con.commit()
            print("Payment added successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not add payment record.")
            if "UNIQUE constraint failed" in str(e):
                print("Payment ID must be unique, and/or a booking cannot have two payments with the same method.")
            elif "CHECK constraint failed: Payment.Payment_ID" in str(e):
                print("Payment ID must start with 'P' followed by 5 digits (e.g., P12345).")
            elif "CHECK constraint failed: Payment.Payment_Method" in str(e):
                print("Payment Method must contain only letters and spaces.")
            elif "CHECK constraint failed: Payment.Payment_Status" in str(e):
                print("Payment Status must be Paid, Unpaid or Partially Paid.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Booking ID does not exist. Please enter a valid Booking ID.")
            else:
                print(f"Database error: {e}")
        
    elif choice == '6':  
        job_id = input("Job ID: ")
        job_date = input("Job Date (DD/MM/YYYY): ")
        job_status = input("Job Status (Finished/Not Started/In Progress): ")
        service_id = input("Service ID: ")
        employee_id = input("Employee ID: ")
        try:
            cursor.execute('''INSERT INTO Job (Job_ID, Job_Date, Job_Status, Service_ID, Employee_ID) 
                            VALUES (?, ?, ?, ?, ?)''', (job_id, job_date, job_status, service_id, employee_id))
            con.commit()
            print("Job added successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not add job record.")
            if "UNIQUE constraint failed" in str(e):
                print("Job ID must be unique, and/or a service and employee cannot have two jobs on the same date.")
            elif "CHECK constraint failed: Job.Job_ID" in str(e):
                print("Job ID must start with 'J' followed by 5 digits (e.g., J12345).")
            elif "CHECK constraint failed: Job.Job_Date" in str(e):
                print("Job Date must be in DD/MM/YYYY format. (e.g., 04/05/2008).")
            elif "CHECK constraint failed: Job.Job_Status" in str(e):
                print("Job Status must be Finished, Not Started or In Progress.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Service ID and/or Employee ID does not exist. Please enter valid .")
            else:
                print(f"Database error: {e}")
        
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
    print("6. Job")
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
        print("ID | Type | Cost ($) | Duration (mins)| Booking ID")
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
        cursor.execute("SELECT * FROM Job")
        rows = cursor.fetchall()
        print("\nJob Records:")
        print("ID | Date | Status | Service ID | Employee ID")
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
    print("6. Job")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == '1':  
        customer_id = input("Enter Customer ID to update: ")
        print("Enter new values (leave blank to keep current):")
        new_customer_id = input("New Customer ID (CXXXXX): ")
        first_name = input("New First Name: ")
        last_name = input("New Last Name: ")
        birth_date = input("New Birth Date (DD/MM/YYYY): ")
        address = input("New Address: ")
        phone = input("New Phone (04XXXXXXXX): ")
        email = input("New Email (local-part@domain.tld): ")

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
            print("Could not update customer record.")
            if "UNIQUE constraint failed" in str(e):
                print("Customer ID, phone, or email must be unique. The value/s you entered already exists.")
            elif "CHECK constraint failed: Customer.Customer_ID" in str(e):
                print("Customer ID must start with 'C' followed by 5 digits (e.g., C12345).")
            elif "CHECK constraint failed: Customer.Customer_First_Name" in str(e):
                print("First Name must contain only letters.")
            elif "CHECK constraint failed: Customer.Customer_Last_Name" in str(e):
                print("Last Name must contain only letters.")
            elif "CHECK constraint failed: Customer.Birth_Date" in str(e):
                print("Birth Date must be in DD/MM/YYYY format. (e.g., 04/05/2008)")
            elif "CHECK constraint failed: Customer.Customer_Phone" in str(e):
                print("Phone must start with '04' and be followed by 8 digits (e.g., 0405200867).")
            elif "CHECK constraint failed: Customer.Email" in str(e):
                print("Email must be in local-part@domain.tld format (e.g., john@gmail.com).")
            else:
                print(f"Database error: {e}")
        
    elif choice == '2':  
        booking_id = input("Enter Booking ID to update: ")
        print("Enter new values (leave blank to keep current):")
        new_booking_id = input("New Booking ID (BXXXXX): ")
        booking_date = input("New Booking Date (DD/MM/YYYY): ")
        customer_id = input("New Customer ID: ")

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
            print("Could not update booking record.")
            if "UNIQUE constraint failed" in str(e):
                print("Booking ID must be unique, and/or a customer cannot have two bookings on the same date.")
            elif "CHECK constraint failed: Booking.Booking_ID" in str(e):
                print("Booking ID must start with 'B' followed by 5 digits (e.g., B12345).")
            elif "CHECK constraint failed: Booking.Booking_Date" in str(e):
                print("Booking Date must be in DD/MM/YYYY format. (e.g., 04/05/2008)")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Customer ID does not exist. Please enter a valid Customer ID.")
            else:
                print(f"Database error: {e}")
        
    elif choice == '3':  
        service_id = input("Enter Service ID to update: ")
        print("Enter new values (leave blank to keep current):")
        new_service_id = input("New Service ID (SXXXXX): ")
        service_type = input("New Service Type: ")
        service_cost = input("New Service Cost (XX.XX): ")
        service_duration = input("New Service Duration: ")
        new_booking_id = input("New Booking ID: ")

        updates = []
        params = []

        if new_service_id:
            updates.append("Service_ID=?")
            params.append(new_service_id)
        if service_type:
            updates.append("Service_Type=?")
            params.append(service_type)
        if service_cost:
            updates.append("Service_Cost=?")
            params.append(service_cost)
        if service_duration:
            updates.append("Service_Duration=?")
            params.append(service_duration)
        if new_booking_id:
            updates.append("Booking_ID=?")
            params.append(new_booking_id)

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
            print("Could not update service record.")
            if "UNIQUE constraint failed" in str(e):
                print("Service ID and Service Type must be unique. The value/s you entered already exists.")
            elif "CHECK constraint failed" in str(e):
                print("One of the following constraints has failed:")
                print("Service ID must start with 'S' followed by 5 digits (e.g., S12345).")
                print("Service Type must contain only letters and spaces.")
                print("Service Cost must be a number to 2 decimal places. (e.g., 100.00)")
                print("Service Duration must be a positive integer.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Booking ID does not exist. Please enter a valid Booking ID.")
            else:
                print(f"Database error: {e}")
        
    elif choice == '4':  
        employee_id = input("Enter Employee ID to update: ")
        print("Enter new values (leave blank to keep current):")
        new_employee_id = input("New Employee ID (EXXXXX): ")
        first_name = input("New First Name: ")
        last_name = input("New Last Name: ")
        phone = input("New Phone (04XXXXXXXX): ")

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
            print("Could not update employee record.")
            if "UNIQUE constraint failed" in str(e):
                print("Employee ID and phone must be unique. The value/s you entered already exists.")
            elif "CHECK constraint failed: Employee.Employee_ID" in str(e):
                print("Employee ID must start with 'E' followed by 5 digits (e.g., E12345).")
            elif "CHECK constraint failed: Employee.Employee_First_Name" in str(e):
                print("First Name must contain only letters.")
            elif "CHECK constraint failed: Employee.Employee_Last_Name" in str(e):
                print("Last Name must contain only letters.")
            elif "CHECK constraint failed: Employee.Employee_Phone" in str(e):
                print("Phone must start with '04' and be followed by 8 digits. (e.g., 0405200867).")
            else:
                print(f"Database error: {e}")
        
    elif choice == '5':  
        payment_id = input("Enter Payment ID to update: ")
        print("Enter new values (leave blank to keep current):")
        new_payment_id = input("New Payment ID (PXXXXX): ")
        payment_method = input("New Payment Method: ")
        payment_status = input("New Payment Status (Finished/Not Finished/In Progress): ")
        booking_id = input("New Booking ID: ")

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
            print("Could not update payment record.")
            if "UNIQUE constraint failed" in str(e):
                print("Payment ID must be unique, and/or a booking cannot have two payments with the same method.")
            elif "CHECK constraint failed: Payment.Payment_ID" in str(e):
                print("Payment ID must start with 'P' followed by 5 digits (e.g., P12345).")
            elif "CHECK constraint failed: Payment.Payment_Method" in str(e):
                print("Payment Method must contain only letters and spaces.")
            elif "CHECK constraint failed: Payment.Payment_Status" in str(e):
                print("Payment Status must be Paid, Unpaid or Partially Paid.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Booking ID does not exist. Please enter a valid Booking ID.")
            else:
                print(f"Database error: {e}")
        
    elif choice == '6':  
        job_id = input("Enter Job ID to update: ")
        print("Enter new values (leave blank to keep current):")
        new_job_id = input("New Job ID (JXXXXX): ")
        new_job_date = input("New Job Date (DD/MM/YYYY): ")
        new_job_status = input("New Job Status (Finished/Not Finished/In Progress): ")
        service_id = input("New Service ID: ")
        employee_id = input("New Employee ID: ")

        updates = []
        params = []

        if new_job_id:
            updates.append("Job_ID=?")
            params.append(new_job_id)
        if new_job_date:
            updates.append("Job_Date=?")
            params.append(new_job_date)
        if new_job_status:
            updates.append("Job_Status=?")
            params.append(new_job_status)
        if service_id:
            updates.append("Service_ID=?")
            params.append(service_id)
        if employee_id:
            updates.append("Employee_ID=?")
            params.append(employee_id)

        if not updates:
            print("No changes made.")
            return

        query = "UPDATE Job SET " + ", ".join(updates) + " WHERE Job_ID=?"
        params.append(job_id)

        try:
            cursor.execute(query, params)
            con.commit()
            print("Job updated successfully!")
        except sqlite3.IntegrityError as e:
            print("Could not update job record.")
            if "UNIQUE constraint failed" in str(e):
                print("Job ID must be unique, and/or a service and employee cannot have two jobs on the same date.")
            elif "CHECK constraint failed: Job.Job_ID" in str(e):
                print("Job ID must start with 'J' followed by 5 digits (e.g., J12345).")
            elif "CHECK constraint failed: Job.Job_Date" in str(e):
                print("Job Date must be in DD/MM/YYYY format. (e.g., 04/05/2008).")
            elif "CHECK constraint failed: Job.Job_Status" in str(e):
                print("Job Status must be Finished, Not Started or In Progress.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print("Service ID and/or Employee ID does not exist. Please enter valid ID.")
            else:
                print(f"Database error: {e}")
        
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
    print("6. Job")
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
        cursor.execute("DELETE FROM Job WHERE Job_ID=?", (job_id,))
        con.commit()
        print("Job deleted successfully!")
        
    elif choice == '7':
        return
    else:
        print("Invalid choice. Please try again.")

def generate_report():
    print("\nSelect Table to Update Record:")
    print("1. Unpaid Jobs")
    print("2. Employee Scedules")
    print("3. Services In Bookings")
    print("4. Total Booking Cost & Duration")
    print("5. Bookings By Customer")
    print("6. Paid Payments")
    print("7. Back to Main Menu")
    
    choice = input("Enter your choice (1-7): ")

    if choice == '1':  
        query = """
        SELECT
            Booking.Customer_ID,
            Customer.Customer_First_Name,
            Customer.Customer_Last_Name,
            Customer.Email,
            Customer.Customer_Phone,
            Payment.Booking_ID,
            Booking.Booking_Date,
            SUM(Service.Service_Cost) AS Total_Booking_Cost,
            Payment.Payment_Status
        FROM
            Customer
            INNER JOIN (
                (
                    Booking
                    INNER JOIN Payment ON Booking.Booking_ID = Payment.Booking_ID
                )
                INNER JOIN Service ON Booking.Booking_ID = Service.Booking_ID
            ) ON Customer.Customer_ID = Booking.Customer_ID
        GROUP BY
            Booking.Customer_ID,
            Customer.Customer_Last_Name,
            Customer.Customer_First_Name,
            Customer.Email,
            Customer.Customer_Phone,
            Payment.Booking_ID,
            Booking.Booking_Date,
            Payment.Payment_Status
        HAVING
            Payment.Payment_Status = "Unpaid"
        ORDER BY
            Booking.Customer_ID,
            Booking.Booking_Date;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print("\nUnpaid Jobs:")
        print("Customer ID | Customer First Name | Customer Last Name | Customer Email | Customer Phone | Booking ID | Booking Date | Total Booking Cost ($) | Payment Status")
        for row in results:
            print(row)

    elif choice == '2':  
        query = """
                SELECT
                    Employee.Employee_ID,
                    Employee.Employee_First_Name,
                    Employee.Employee_Last_Name,
                    Booking.Booking_Date,
                    Booking.Booking_ID,
                    Service.Service_Type,
                    Job.Job_Status
                FROM
                    Employee
                    INNER JOIN (
                        Booking
                        INNER JOIN (
                            Service
                            INNER JOIN Job ON Service.Service_ID = Job.Service_ID
                        ) ON Booking.Booking_ID = Service.Booking_ID
                    ) ON Employee.Employee_ID = Job.Employee_ID
                ORDER BY
                    Employee.Employee_ID,
                    Booking.Booking_Date,
                    Booking.Booking_ID;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print("\nEmployee Scedule:")
        print("Employee ID | Employee First Name | Employee Last Name | Booking Date | Booking ID | Service Type | Job Status")
        for row in results:
            print(row)
        
    elif choice == '3':  
        query = """
                SELECT
                    Booking.Booking_ID,
                    Booking.Booking_Date,
                    Service.Service_Type,
                    Service.Service_Cost,
                    Service.Service_Duration
                FROM
                    Booking
                    INNER JOIN
                SERVICE ON Booking.Booking_ID = Service.Booking_ID
                ORDER BY
                    Booking.Booking_ID,
                    Service.Service_Type;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print("\nServices In Bookings:")
        print("Booking ID | Booking Date | Service Type | Service Cost ($) | Service Duration (mins)")
        for row in results:
            print(row)
        
    elif choice == '4':  
        query = """
                SELECT
                    Booking.Booking_ID,
                    Booking.Booking_Date,
                    Sum(Service.Service_Cost) AS TotalBookingCost,
                    Sum(Service.Service_Duration) AS TotalBookingDuration
                FROM
                    Booking
                    INNER JOIN
                Service ON Booking.Booking_ID = Service.Booking_ID
                GROUP BY
                    Booking.Booking_ID,
                    Booking.Booking_Date
                ORDER BY
                    Booking.Booking_ID,
                    Sum(Service.Service_Cost),
                    Sum(Service.Service_Duration);
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print("\nTotal Booking Cost & Duration:")
        print("Booking ID | Booking Date | Total Booking Cost ($) | Total Booking Duration (mins)")
        for row in results:
            print(row)
        
    elif choice == '5':  
        query = """
                SELECT
                    Customer.Customer_ID,
                    Customer.Customer_First_Name,
                    Customer.Customer_Last_Name,
                    Customer.Customer_Phone,
                    Booking.Booking_ID,
                    Booking.Booking_Date
                FROM
                    Customer
                    INNER JOIN 
                Booking ON Customer.Customer_ID = Booking.Customer_ID;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print("\nBookings By Customer:")
        print("Booking ID | Customer First Name | Customer Last Name | Customer Phone | Booking Date")
        for row in results:
            print(row)
        
    elif choice == '6':
        query = """
                SELECT
                    Booking.Booking_ID,
                    Payment.Payment_Status,
                    Payment.Payment_Method
                FROM
                    Customer
                    INNER JOIN Booking ON Customer.Customer_ID = Booking.Customer_ID
                    INNER JOIN Payment ON Booking.Booking_ID = Payment.Booking_ID
                WHERE
                    Payment.Payment_Status = "Paid";
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print("\nPaid Payments:")
        print("Booking ID | Payment Status | Payment Method")
        for row in results:
            print(row)
        
    elif choice == '7':
        return
    else:
        print("Invalid choice. Please try again.")

def main():
    create_tables()

    customers = [
        ('C11001', 'Daniel', 'Smith', '15/17/1988', '123 Main St, Anytown, CA 90210', '0467953696', 'danielsmith@gmail.com'),
        ('C11002', 'Sarah', 'Johnson', '02/11/1990', '456 Oak Ave, Somewhere, NY 10001', '0448295716', 'sarahj@gmail.com'),
        ('C11003', 'Michael', 'Williams', '08/03/1993', '789 Pine Rd, Nowhere, TX 75001', '0413579024', 'michaelw@gmail.com'),
        ('C11004', 'Emily', 'Brown', '30/09/1995', '321 Elm Blvd, Anycity, FL 33101', '0487654321', 'emilyb@gmail.com'),
        ('C11005', 'David', 'Jones', '14/12/1982', '654 Maple Ln, Yourtown, IL 60007', '0424681357', 'davidjones@gmail.com')
    ]

    for customer in customers:
        cursor.execute('''INSERT INTO Customer (Customer_ID, Customer_First_Name, Customer_Last_Name, 
                        Birth_Date, Address, Customer_Phone, Email)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', customer)
    con.commit()

    bookings = [
        ('B10001', '01/01/2023', 'C11001'),
        ('B10002', '02/02/2023', 'C11002'),
        ('B10003', '03/03/2023', 'C11003'),
        ('B10004', '04/04/2023', 'C11004'),
        ('B10005', '05/05/2023', 'C11005')
    ]

    for booking in bookings:
        cursor.execute('''INSERT INTO Booking (Booking_ID, Booking_Date, Customer_ID)
                        VALUES (?, ?, ?)''', booking)
        
    con.commit()

    services = [
        ('S20001', 'Lawn Mowing', '50.00', '30', 'B10001'),
        ('S20002', 'Bush Trimming', '40.00', '45', 'B10002'),
        ('S20003', 'Leaf Removal', '60.00', '60', 'B10003'),
        ('S20004', 'Pest Control', '80.00', '90', 'B10004'),
        ('S20005', 'Weed Control', '120.00', '120', 'B10005')
    ]

    for service in services:
        cursor.execute('''INSERT INTO Service (Service_ID, Service_Type, Service_Cost, Service_Duration, Booking_ID)
                        VALUES (?, ?, ?, ?, ?)''', service)
        
    con.commit()

    employees = [
        ('E30001', 'Alice', 'Green', '0401234567'),
        ('E30002', 'Bob', 'White', '0402345678'),
        ('E30003', 'Charlie', 'Black', '0403456789'),
        ('E30004', 'Diana', 'Blue', '0404567890'),
        ('E30005', 'Ethan', 'Red', '0405678901')
    ]

    for employee in employees:
        cursor.execute('''INSERT INTO Employee (Employee_ID, Employee_First_Name, Employee_Last_Name, Employee_Phone)
                        VALUES (?, ?, ?, ?)''', employee)
        
    con.commit()

    payments = [
        ('P40001', 'Credit Card', 'Unpaid', 'B10001'),
        ('P40002', 'Cash', 'Paid', 'B10002'),
        ('P40003', 'Debit Card', 'Partially Paid', 'B10003'),
        ('P40004', 'PayPal', 'Paid', 'B10004'),
        ('P40005', 'Bank Transfer', 'Unpaid', 'B10005')
    ]

    for payment in payments:
        cursor.execute('''INSERT INTO Payment (Payment_ID, Payment_Method, Payment_Status, Booking_ID)
                        VALUES (?, ?, ?, ?)''', payment)
        
    con.commit()

    jobs = [
        ('J50001', '01/01/2023', 'Finished', 'S20001', 'E30001'),
        ('J50002', '02/02/2023', 'Finished', 'S20002', 'E30002'),
        ('J50003', '03/03/2023', 'In Progress', 'S20003', 'E30003'),
        ('J50004', '04/04/2023', 'In Progress', 'S20004', 'E30004'),
        ('J50005', '05/05/2023', 'Not Started', 'S20005', 'E30005')
    ]

    for job in jobs:
        cursor.execute('''INSERT INTO Job (Job_ID, Job_Date, Job_Status, Service_ID, Employee_ID)
                        VALUES (?, ?, ?, ?, ?)''', job)
        
    con.commit()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            add_record()
        elif choice == '2':
            view_records()
        elif choice == '3':
            update_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            generate_report()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
    
    con.close()


main()