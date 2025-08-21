    customers = [
        ('C11001', 'Daniel', 'Smith', '15/17/1988', '123 Main St, Anytown, CA 90210', '0467953696', 'danielsmith@gmail.com'),
        ('C11002', 'Sarah', 'Johnson', '02/11/1990', '456 Oak Ave, Somewhere, NY 10001', '0448295716', 'sarahj@gmail.com'),
        ('C11003', 'Michael', 'Williams', '08/03/1993', '789 Pine Rd, Nowhere, TX 75001', '0413579024', 'michaelw@gmail.com'),
        ('C11004', 'Emily', 'Brown', '30/09/1995', '321 Elm Blvd, Anycity, FL 33101', '0487654321', 'emilyb@gmail.com'),
        ('C11005', 'David', 'Jones', '14/12/1982', '654 Maple Ln, Yourtown, IL 60007', '0424681357', 'davidjones@gmail.com')
    ]

    bookings = [
        ('B10001', '01/01/2023', 'C11001'),
        ('B10002', '02/02/2023', 'C11002'),
        ('B10003', '03/03/2023', 'C11003'),
        ('B10004', '04/04/2023', 'C11004'),
        ('B10005', '05/05/2023', 'C11005')
    ]

    services = [
        ('S20001', 'Lawn Mowing', '50.00', '30', 'B10001'),
        ('S20002', 'Bush Trimming', '40.00', '45', 'B10002'),
        ('S20003', 'Leaf Removal', '60.00', '60', 'B10003'),
        ('S20004', 'Pest Control', '80.00', '90', 'B10004'),
        ('S20005', 'Weed Control', '120.00', '120', 'B10005')
    ]

    employees = [
        ('E30001', 'Alice', 'Green', '0401234567'),
        ('E30002', 'Bob', 'White', '0402345678'),
        ('E30003', 'Charlie', 'Black', '0403456789'),
        ('E30004', 'Diana', 'Blue', '0404567890'),
        ('E30005', 'Ethan', 'Red', '0405678901')
    ]

    payments = [
        ('P40001', 'Credit Card', 'Unpaid', 'B10001'),
        ('P40002', 'Cash', 'Paid', 'B10002'),
        ('P40003', 'Debit Card', 'Partially Paid', 'B10003'),
        ('P40004', 'PayPal', 'Paid', 'B10004'),
        ('P40005', 'Bank Transfer', 'Unpaid', 'B10005')
    ]

    jobs = [
        ('J50001', '01/01/2023', 'Finished', 'S20001', 'E30001'),
        ('J50002', '02/02/2023', 'Finished', 'S20002', 'E30002'),
        ('J50003', '03/03/2023', 'In Progress', 'S20003', 'E30003'),
        ('J50004', '04/04/2023', 'In Progress', 'S20004', 'E30004'),
        ('J50005', '05/05/2023', 'Not Started', 'S20005', 'E30005')
    ]

    for customer in customers:
        cursor.execute('SELECT 1 FROM Customer WHERE Customer_ID=? OR Customer_Phone=? OR Email=?', (customer[0], customer[5], customer[6]))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO Customer (Customer_ID, Customer_First_Name, Customer_Last_Name, 
                            Birth_Date, Address, Customer_Phone, Email)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', customer)

    for booking in bookings:
        cursor.execute('SELECT 1 FROM Booking WHERE Booking_ID=?', (booking[0],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO Booking (Booking_ID, Booking_Date, Customer_ID)
                            VALUES (?, ?, ?)''', booking)

    for service in services:
        cursor.execute('SELECT 1 FROM Service WHERE Service_ID=?', (service[0],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO Service (Service_ID, Service_Type, Service_Cost, Service_Duration, Booking_ID)
                            VALUES (?, ?, ?, ?, ?)''', service)

    for employee in employees:
        cursor.execute('SELECT 1 FROM Employee WHERE Employee_ID=? OR Employee_Phone=?', (employee[0], employee[3]))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO Employee (Employee_ID, Employee_First_Name, Employee_Last_Name, Employee_Phone)
                            VALUES (?, ?, ?, ?)''', employee)

    for payment in payments:
        cursor.execute('SELECT 1 FROM Payment WHERE Payment_ID=?', (payment[0],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO Payment (Payment_ID, Payment_Method, Payment_Status, Booking_ID)
                            VALUES (?, ?, ?, ?)''', payment)
 
    for job in jobs:
        cursor.execute('SELECT 1 FROM Job WHERE Job_ID=?', (job[0],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO Job (Job_ID, Job_Date, Job_Status, Service_ID, Employee_ID)
                            VALUES (?, ?, ?, ?, ?)''', job)
    con.commit()