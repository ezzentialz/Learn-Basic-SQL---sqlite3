import sqlite3

db_file = 'hotel_management_test2.db'

try:
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # ตรวจสอบว่าตาราง Employees มีอยู่แล้วหรือไม่
        # (ส่วนนี้จะคล้ายกับโค้ดเดิม เพื่อให้แน่ใจว่าตารางพร้อมใช้งาน)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT, -- เพิ่ม AUTOINCREMENT ให้รัน ID อัตโนมัติ
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL
        );
        """
        cursor.execute(create_table_sql)
        print("สร้างตาราง Employees สำเร็จ (หรือมีอยู่แล้ว)!")

        # ----------------------------------------------------
        print("\n--- การจัดการข้อมูล: INSERT, UPDATE, DELETE ---")
        # 1. INSERT INTO: เพิ่มข้อมูลใหม่
        print("\n**1. เพิ่มข้อมูลใหม่ (INSERT INTO)**")
        insert_new_employee_sql = """
        INSERT INTO Employees (first_name, last_name, position, salary)
        VALUES ('Nongluck', 'Srisuk', 'Housekeeping', 27000.00);
        """
        try:
            cursor.execute(insert_new_employee_sql)
            conn.commit()
            print("เพิ่มพนักงาน Nongluck Srisuk สำเร็จ!")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเพิ่มข้อมูล Nongluck: {e}")

        # เพิ่มพนักงานอีกคน เพื่อให้มีข้อมูลเยอะขึ้น
        insert_another_employee_sql = """
        INSERT INTO Employees (first_name, last_name, position, salary)
        VALUES ('Somkid', 'Deejai', 'Manager', 80000.00),
        ('S','Good student','CEO', 100000.00); 
        """#ลองเพิ่มของตัวเองเข้าไป
        try:
            cursor.execute(insert_another_employee_sql)
            conn.commit()
            print("เพิ่มพนักงาน Somkid Deejai สำเร็จ! ของ S ด้วยคนนะครับ")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเพิ่มข้อมูล Somkid หรือ S: {e}")

        print("\n--- ข้อมูลพนักงานทั้งหมดหลัง INSERT ---")
        cursor.execute("SELECT employee_id, first_name, last_name, position, salary FROM Employees;")
        for row in cursor.fetchall():
            print(row)

        # 2. UPDATE: แก้ไขข้อมูล
        print("\n**2. แก้ไขข้อมูล (UPDATE)**")
        # สมมติว่าต้องการอัปเดตเงินเดือนของ Nongluck (ซึ่ง employee_id อาจจะเป็น 7 หรือ 8 ขึ้นอยู่กับการรันครั้งก่อนๆ)
        # เราจะหา employee_id ของ Nongluck ก่อนเพื่อความแม่นยำ
        cursor.execute("SELECT employee_id FROM Employees WHERE first_name = 'Nongluck' AND last_name = 'Srisuk';")
        nongluck_id = cursor.fetchone()
        print(f"Debug checking nongluck_id INTEGER PRIMARY: {nongluck_id}") #ขอเช็คnongluck_id ว่ามีค่าเป็นแบบไหนนะครับ
        if nongluck_id:
            nongluck_id = nongluck_id[0] #ตรงนี้ผมเข้าใจว่าน่าจะ index 0 หรือตำแหน่งที่1
            update_nongluck_salary_sql = f"""
            UPDATE Employees
            SET salary = 29000.00, position = 'Housekeeping Supervisor'
            WHERE employee_id = {nongluck_id}; 
            """ #WHERE employee_id = {nongluck_id} แปลตามความคิดผมคือ (if) employee_id = {nongluck_id} ให้ เปลี่ยน salary = 29,000.00 และ เปลี่ยน position เป็น 'Housekeeping Sup'
            cursor.execute(update_nongluck_salary_sql)
            conn.commit()# save update_nongluck_salary_sql เข้าไปเก็บไว้ใน cursor.execute() 
            print(f"อัปเดตข้อมูลพนักงาน Nongluck (ID: {nongluck_id}) สำเร็จ! (เงินเดือน: 29000.00, ตำแหน่ง: Housekeeping Supervisor)")
        else:
            print("ไม่พบพนักงาน Nongluck Srisuk ในฐานข้อมูลเพื่ออัปเดต.")

        print("\n--- ข้อมูลพนักงานหลัง UPDATE Nongluck ---")
        cursor.execute("SELECT employee_id, first_name, last_name, position, salary FROM Employees;")
        for row in cursor.fetchall(): #กำหนดให้ row วนลูปอ่านค่าใน cursor โดยใช้คำสั่ง .fetchall()
            print(row) #ให้ row แสดงผลทั้งหมด

        # 3. DELETE FROM: ลบข้อมูล
        print("\n**3. ลบข้อมูล (DELETE FROM)**")
        # ลบพนักงานชื่อ "S" แก้เป็นชื่อผมนะ
        delete_S_sql = """ 
        DELETE FROM Employees
        WHERE first_name = 'S'; 
        """#ใช้เป็นชื่อผมละกันครับ  ผมลองสังเกตดูแล้วเห็นว่า การใช้ WHERE สามารถระบุเป็น คอลัมนั้น ตามด้วย value หรือ จะเป็นการสร้างตัวแปรเพื่อระบุ integer/index ของตัวนั้น
        cursor.execute(delete_S_sql)
        conn.commit()
        print("ลบพนักงาน S สำเร็จ!") 

        print("\n--- ข้อมูลพนักงานทั้งหมดหลัง DELETE S ---")
        cursor.execute("SELECT employee_id, first_name, last_name, position, salary FROM Employees;")
        for row in cursor.fetchall():
            print(row)
            
        #ลองเพิ่มพนักงานเข้าไปใหม่นะครับ
        insert_some_employee = """INSERT INTO Employees (first_name, last_name, position, salary)
        VALUES ('Pornchai', 'Wongyai', 'Housekeeping', 20000.00);
        """
        try: 
            cursor.execute(insert_some_employee)
            conn.commit()
            print("\nเพิ่ม Pornchai กลับเข้าไปแล้ว")
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
            
        #ปริ๊นรายชื่อทั้งหมด
        cursor.execute("SELECT employee_id, first_name, last_name, position, salary FROM Employees;")
        for all_names in cursor.fetchall():
            print(all_names) #ผมลองเปลี่ยนชื่อ ตัววนลูปดูครับ
            
        # ลองเพิ่มข้อมูลเดิมที่เราลบไปแล้วกลับเข้าไป (เพื่อจะได้มีข้อมูลครบสำหรับการทดลองอื่นๆ)
        # INSERT INTO Employees (first_name, last_name, position, salary) VALUES ('Pornchai', 'Wongyai', 'Housekeeping', 28000.00);
        # conn.commit()
        # print("\nเพิ่ม Pornchai กลับเข้าไปแล้ว (ถ้าต้องการ)")


except sqlite3.Error as e:
    print(f"เกิดข้อผิดพลาดของ SQLite: {e}")
except Exception as e:
    print(f"เกิดข้อผิดพลาดทั่วไป: {e}")