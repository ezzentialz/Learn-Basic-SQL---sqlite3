import sqlite3 as sql
# สร้างไฟล์ฐานข้อมูล SQLite ชื่อ hotel_customer_db.db (ใช้ชื่อใหม่นะคะ จะได้ไม่ปนกับไฟล์เดิม)
hotel_customer_db = 'hotel_customer_db.db'

try:
    with sql.connect(hotel_customer_db) as conn:
        cursor = conn.cursor()# สร้าง sql ที่มีชื่อ hotel_customer_db
    #สร้าง 2 ตารางในฐานข้อมูลนี้
    #ตารางที่ 1: Customers (ข้อมูลลูกค้า)
        create_customer_table_sql = """ 
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE, 
            phone TEXT,
            registration_date TEXT
        );
        """
        cursor.execute(create_customer_table_sql)
        #สร้างตาราง customer
        
        #ตารางที่ 2: Bookings (ข้อมูลการจอง)
        create_bookings_table_sql = """
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            room_type TEXT NOT NULL,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT NOT NULL,
            total_price REAL,
            status TEXT      
        );
        """
        cursor.execute(create_bookings_table_sql)
        #สร้างตาราง booking
        
        try:
            cursor.execute("DELETE FROM Customers;")
            cursor.execute("DELETE FROM Bookings;")
            conn.commit()
            print("ลบข้อมูลเก่าใน Customers และ Bookings สำเร็จ!")
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
            
        #เพิ่มข้อมูลเริ่มต้น (INSERT):
        #เพิ่มข้อมูลลูกค้าอย่างน้อย 5 คนในตาราง Customers
        print(f"เพิ่มข้อมูลลูกค้า")
        insert_customer_sql ="""
        INSERT INTO Customers (first_name, last_name, email, phone,registration_date)
        VALUES  ('Alice', 'Wellington', 'alice@example.com', '0801511541', '2025-06-01'),
                ('Bob', 'Rainwood', 'bob@example.com', '0811544526', '2025-06-01'),
                ('Chris', 'Califorge', 'chris@example.com', '0806548596', '2025-06-02'),
                ('Dough', 'Wilbert', 'dough@example.com', '0894859696', '2025-06-02'),
                ('Ellis', 'Runeterra', 'ellis@example.com', '0841596597', '2025-06-03');
        """
        try:  
            cursor.execute(insert_customer_sql)
            #ใส่data เข้าไปในตาราง customer
            conn.commit() # save
            print("เพิ่มข้อมูลลูกค้าสำเร็จ")
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
            
        cursor.execute("SELECT customer_id, first_name, last_name, email, phone,registration_date FROM Customers;")    
        for row in cursor.fetchall():
            print(row)
        print('ปริ๊นข้อมูลลูกค้าออกมาได้แล้ว')
        
        #เพิ่มข้อมูลการจองอย่างน้อย 7 รายการในตาราง Bookings โดยให้มีการจองจากลูกค้าที่ต่างกัน 
        # และมีลูกค้าบางคนมีการจองมากกว่า 1 ครั้ง เพื่อให้เราได้ฝึก GROUP BY และ JOIN ในอนาคตค่ะ
        insert_booking_sql = """
        INSERT INTO Bookings (customer_id, room_type, check_in_date, check_out_date, total_price, status)
        VALUES  (1,'Deluxe', '2025-06-10', '2025-06-12', 6000.00, 'Confirmed'),
                (2,'Stadard','2025-06-10', '2025-06-13', 6000.00, 'Confirmed'),
                (2,'Deluxe', '2025-06-10', '2025-06-13', 9000.00, 'Pending'),
                (3,'Suite', '2025-06-12', '2025-06-13', 5000.00, 'Confirmed'),
                (4,'Deluxe', '2025-06-13', '2025-06-16', 9000.00, 'Cancelled'),
                (4,'Deluxe', '2025-06-14', '2025-06-16', 6000.00, 'Pending'),
                (5,'Suite', '2025-06-15','2025-06-18', 15000.00, 'Confirmed');
        """
        try:
            cursor.execute(insert_booking_sql)
            conn.commit()
            print(f"เพิ่มข้อมูล bookingสำเร็จ")
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
        
        #ดำเนินการตามคำสั่ง DML (UPDATE & DELETE):
        #UPDATE:
        #แก้ไข phone ของลูกค้าคนใดคนหนึ่ง
        #แก้ไข status การจองของรายการจองใดรายการจองหนึ่ง (เช่น จาก 'Pending' เป็น 'Confirmed')
        
        cursor.execute("SELECT phone FROM Customers WHERE last_name = 'Rainwood';")
        bob_id = cursor.fetchone()[0]
        print(bob_id)
        update_bob_phone = f"""
        UPDATE Customers
        SET phone = '0800010012'
        WHERE customer_id = {bob_id};
        """
        try:
            cursor.execute(update_bob_phone)
            conn.commit()
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
            
        cursor.execute("SELECT status FROM Bookings WHERE check_in_date = '2025-06-14' AND check_out_date = '2025-06-16';")
        status_change = cursor.fetchone()[0]
        print(status_change)
        update_status_change = f"""
        UPDATE Bookings
        SET status = 'Confirmed'
        WHERE booking_id = 6;
        """ 
        try:   
            cursor.execute(update_status_change)
            conn.commit()
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
            
        #DELETE:
        #ลบลูกค้า 1 คนออกจากตาราง Customers (เลือกคนที่ไม่ได้มีการจองในตาราง Bookings เพื่อหลีกเลี่ยงปัญหา Foreign Key ที่เรายังไม่ได้เรียนนะคะ)
        #ลบรายการจอง 1 รายการออกจากตาราง Bookings

        delete_customers = """
        DELETE FROM Customers
        WHERE customer_id = '1';
        """
        try:
            cursor.execute(delete_customers)
            conn.commit()
            print('ลบลูกค้าที่มี customer_id 1')
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
            
        try:    
            cursor.execute("DELETE FROM Bookings WHERE status = 'Cancelled';")
            conn.commit()
            print('ลบbooking ที่มีvalue = Cancelled')
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
        #ดึงและสรุปข้อมูล (SELECT, Aggregate Functions, GROUP BY, HAVING):

        #SELECT:
        #ดึงข้อมูลลูกค้าทั้งหมด (ทุกคอลัมน์)
        cursor.execute("SELECT * FROM Bookings LIMIT 5")
        for all in cursor.fetchall():
            print(all)
        #ดึงเฉพาะ first_name, email ของลูกค้าที่มี registration_date ในปี 2025 (ใช้ LIKE '2025%' หรือ strftime('%Y', registration_date) = '2025')
        cursor.execute("SELECT first_name, email FROM Customers WHERE registration_date LIKE '2025%'")
        for row in cursor.fetchall():
            print(row)
        #ดึงข้อมูลการจองทั้งหมดที่สถานะเป็น 'Confirmed' และเรียงตาม check_in_date จากเก่าไปใหม่
        cursor.execute("SELECT * FROM Bookings WHERE status = 'Confirmed' ORDER BY check_in_date ASC")
        for all in cursor.fetchall():
            print(all)

        #Aggregate Functions & GROUP BY:
        #นับจำนวนลูกค้าทั้งหมด
        cursor.execute("SELECT COUNT(*) FROM Customers")
        total_customers = cursor.fetchone()[0]
        print(total_customers)
        #หาค่าเฉลี่ยของ total_price จากการจองทั้งหมด
        cursor.execute("SELECT AVG(total_price) FROM Bookings")
        avg_price = cursor.fetchone()[0]
        print(f"{avg_price:,.2f}")
        #นับจำนวนการจองในแต่ละ room_type
        group_room = """
        SELECT room_type, COUNT(*) FROM Bookings GROUP BY room_type;
        """
        cursor.execute(group_room)
        count_room = cursor.fetchall()
        for row in count_room:
            print(f"room type: {row[0]} have {row[1]} rooms")
        #หา SUM(total_price) สำหรับการจองแต่ละ status
        group_sum_total_price = """
        SELECT status, SUM(total_price) FROM Bookings GROUP BY status;
        """
        cursor.execute(group_sum_total_price)
        count_status = cursor.fetchall()
        for row in count_status:
            print(f"room status: {row[0]} | have total price : {row[1]:,.2f} ")
        #หา AVG(total_price) ของการจองสำหรับแต่ละ room_type ที่มีจำนวนการจองมากกว่า 1 รายการ (ใช้ HAVING)
        room_type_avg_price = """
        SELECT room_type, AVG(total_price) AS avg_price_per_room, COUNT(*) AS num_bookings FROM Bookings GROUP BY room_type HAVING COUNT(*) > 1;
        """
        cursor.execute(room_type_avg_price)
        room_avg_price = cursor.fetchall()
        for w in room_avg_price:
            print(f"room type : {w[0]} | average price : {w[1]:,.2f} ")

        print("\n--- การเชื่อมตารางด้วย INNER JOIN ---")

        # ตัวอย่างที่ 1: ดึงชื่อลูกค้าและรายละเอียดการจองทั้งหมดที่ Confirm แล้ว
        # เราต้องการข้อมูลจากทั้งตาราง Customers (first_name, last_name)
        # และจากตาราง Bookings (room_type, check_in_date, total_price, status)
        # โดยเชื่อมด้วย customer_id
        inner_join_confirmed_bookings_sql = """
        SELECT
            C.first_name,
            C.last_name,
            B.room_type,
            B.check_in_date,
            B.check_out_date,
            B.total_price,
            B.status
        FROM
            Customers AS C -- กำหนดชื่อย่อ C ให้ Customers เพื่อให้โค้ดสั้นลง
        INNER JOIN
            Bookings AS B ON C.customer_id = B.customer_id
        WHERE
            B.status = 'Confirmed'
        ORDER BY
            C.last_name, B.check_in_date;
        """
        print("\n**1. รายชื่อลูกค้าและการจองที่ 'Confirmed' แล้ว (INNER JOIN)**")
        cursor.execute(inner_join_confirmed_bookings_sql)
        confirmed_bookings_data = cursor.fetchall()

        if confirmed_bookings_data:
            print(f"{'ชื่อลูกค้า':<20} {'ประเภทห้อง':<15} {'เช็คอิน':<12} {'เช็คเอาท์':<12} {'ราคา':<10} {'สถานะ':<10}")
            print("-" * 80)
            for row in confirmed_bookings_data:
                print(f"{row[0]} {row[1]:<15} {row[2]:<15} {row[3]:<12} {row[4]:<12} {row[5]:<10,.2f} {row[6]:<10}")
        else:
            print("ไม่พบข้อมูลการจองที่ 'Confirmed' (อาจเกิดจากการลบหรืออัปเดตสถานะไปก่อนหน้า)")


        # ตัวอย่างที่ 2: นับจำนวนการจองของแต่ละลูกค้า (INNER JOIN + GROUP BY)
        # เราต้องการนับว่าลูกค้าแต่ละคนมีการจองกี่ครั้ง
        count_bookings_per_customer_sql = """
        SELECT
            C.first_name,
            C.last_name,
            COUNT(B.booking_id) AS total_bookings
        FROM
            Customers AS C
        INNER JOIN
            Bookings AS B ON C.customer_id = B.customer_id
        GROUP BY
            C.customer_id, C.first_name, C.last_name -- ต้อง Group By ด้วยคอลัมน์ที่เลือกมา
        ORDER BY
            total_bookings DESC;
        """
        print("\n**2. จำนวนการจองของลูกค้าแต่ละคน (INNER JOIN + GROUP BY)**")
        cursor.execute(count_bookings_per_customer_sql)
        customer_booking_counts = cursor.fetchall()

        if customer_booking_counts:
            print(f"{'ชื่อลูกค้า':<20} {'จำนวนการจอง':<15}")
            print("-" * 35)
            for row in customer_booking_counts:
                print(f"{row[0]} {row[1]:<13} {row[2]:<15}")
        else:
            print("ไม่พบข้อมูลการจองสำหรับลูกค้าใดๆ")


        print("\n--- การเชื่อมตารางด้วย LEFT JOIN ---")

        # ตัวอย่างที่ 3: ดึงข้อมูลลูกค้าทั้งหมด และข้อมูลการจอง (ถ้ามี)
        # ใช้ LEFT JOIN เพื่อให้ลูกค้าทุกคนปรากฏในผลลัพธ์ ไม่ว่าจะมีข้อมูลการจองหรือไม่ก็ตาม
        left_join_all_customers_sql = """
        SELECT
            C.first_name,
            C.last_name,
            B.room_type,
            B.check_in_date,
            B.status
        FROM
            Customers AS C
        LEFT JOIN
            Bookings AS B ON C.customer_id = B.customer_id
        ORDER BY
            C.last_name;
        """
        print("\n**3. ลูกค้าทั้งหมดและการจอง (ถ้ามี) (LEFT JOIN)**")
        cursor.execute(left_join_all_customers_sql)
        all_customers_data = cursor.fetchall()

        if all_customers_data:
            print(f"{'ชื่อลูกค้า':<20} {'ประเภทห้อง':<15} {'เช็คอิน':<12} {'สถานะ':<10}")
            print("-" * 60)
            for row in all_customers_data:
                # จัดการกรณีที่ข้อมูลการจองเป็น NULL (ไม่มีการจอง)
                room_type = row[2] if row[2] else "N/A"
                check_in = row[3] if row[3] else "N/A"
                status = row[4] if row[4] else "N/A"
                print(f"{row[0]} {row[1]:<13} {room_type:<15} {check_in:<12} {status:<10}")
        else:
            print("ไม่พบข้อมูลลูกค้า")
            
        #ดึงข้อมูลการจองทั้งหมดที่ยังอยู่ในสถานะ 'Pending' (รอดำเนินการ) พร้อมกับ ชื่อและนามสกุลของลูกค้าที่ทำการจองนั้นๆ ด้วยค่ะ
        left_join_all_customer_pending = """
        SELECT  C.first_name,
                C.last_name,
                B.room_type,
                B.check_in_date,
                B.status
                
        FROM Customers AS C
        LEFT JOIN Bookings AS B ON C.customer_id = B.customer_id
        WHERE B.status = 'Pending'
        ORDER BY B.check_in_date ASC;
        
        """
        print("ลูกค้าทั้งหมด ที่ยังอยู่ในสถานะ Pending")
        cursor.execute(left_join_all_customer_pending)
        all_customers_pending = cursor.fetchall()
        
        if all_customers_pending:
            for row in all_customers_pending:
                room_type = row[2] if row[2] else 'N/A'
                check_in_date = row[3] if row[3] else 'N/A'
                status = row[4] if row[4] else 'N/A'
            
            print(row[0], row[1], room_type, check_in_date, status)
        else:
            print('ไม่พบข้อมูล')

except sql.Error as e:
    print(f"เกิดข้อผิดพลาดของ SQLite: {e}")
except Exception as e:
    print(f"เกิดข้อผิดพลาดทั่วไป: {e}")
