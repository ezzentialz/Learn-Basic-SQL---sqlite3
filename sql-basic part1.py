import sqlite3

# 1. กำหนดชื่อไฟล์ฐานข้อมูล (ถ้ายังไม่มี ไฟล์จะถูกสร้างขึ้นมาใหม่)
db_file = 'hotel_management_test1.db'

try:
    # 2. เชื่อมต่อกับฐานข้อมูล (ถ้าไฟล์ไม่มี จะสร้างให้ใหม่)
    # หมอใช้ with statement เพื่อให้แน่ใจว่าการเชื่อมต่อจะถูกปิดโดยอัตโนมัติ
    with sqlite3.connect(db_file) as conn:
        print(f"เชื่อมต่อกับฐานข้อมูล {db_file} สำเร็จ!")

        # สร้าง Cursor object เพื่อใช้ในการรันคำสั่ง SQL
        cursor = conn.cursor()

        # 3. สร้างตาราง Employees
        # ใช้ triple quotes เพื่อให้เขียน SQL ได้หลายบรรทัด
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL
        );
        """
        cursor.execute(create_table_sql)
        print("สร้างตาราง Employees สำเร็จ (หรือมีอยู่แล้ว)!")

        # 4. เพิ่มข้อมูลตัวอย่างลงในตาราง Employees
        # ใช้ INSERT INTO เพื่อเพิ่มข้อมูล
        insert_data_sql = """
        INSERT INTO Employees (first_name, last_name, position, salary) VALUES
        ('Somsak', 'Klinhom', 'Manager', 75000.00),
        ('Suchart', 'Jaidee', 'Front Desk', 35000.00),
        ('Pornchai', 'Wongyai', 'Housekeeping', 28000.00),
        ('Siriporn', 'Khamdee', 'Front Desk', 38000.00),
        ('Chaiyot', 'Rungsang', 'Security', 30000.00),
        ('Aree', 'Sukjai', 'Manager', 68000.00);
        """
        try:
            cursor.execute(insert_data_sql)
            conn.commit() # ยืนยันการเปลี่ยนแปลง (บันทึกลงฐานข้อมูล)
            print("เพิ่มข้อมูลตัวอย่างสำเร็จ!")
        except sqlite3.IntegrityError:
            print("ข้อมูลตัวอย่างอาจจะถูกเพิ่มไปแล้ว (เนื่องจาก employee_id เป็น PRIMARY KEY และเราไม่ได้ระบุค่า)")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเพิ่มข้อมูล: {e}")

        # 5. ลองใช้คำสั่ง SELECT ที่เราเรียนมา!
        print("\n--- ข้อมูลพนักงานทั้งหมด (SELECT *) ---")
        select_all_sql = "SELECT * FROM Employees;"
        cursor.execute(select_all_sql)
        rows = cursor.fetchall() # ดึงข้อมูลทั้งหมดที่ได้จากคำสั่ง SELECT
        for row in rows:
            print(row)

        print("\n--- ชื่อและตำแหน่งของพนักงานที่มีตำแหน่ง Front Desk (SELECT WHERE) ---")
        select_front_desk_sql = "SELECT first_name, position FROM Employees WHERE position = 'Front Desk';"
        cursor.execute(select_front_desk_sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        print("\n--- พนักงานที่เงินเดือนมากกว่า 40000 เรียงจากเงินเดือนมากไปน้อย (SELECT WHERE ORDER BY) ---")
        select_high_salary_sql = "SELECT first_name, salary FROM Employees WHERE salary > 40000 ORDER BY salary DESC;"
        cursor.execute(select_high_salary_sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        print("\n--- พนักงาน 2 คนแรกที่มีเงินเดือนสูงสุด (SELECT ORDER BY LIMIT) ---")
        select_top_2_salary_sql = "SELECT first_name, salary FROM Employees ORDER BY salary DESC LIMIT 2;"
        cursor.execute(select_top_2_salary_sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            
        print("\n--- ลองดูพนักงานเงินเดือนน้อยสุด ---")
        select_low_salary_sql = "SELECT first_name, salary FROM Employees ORDER BY salary ASC LIMIT 3;"
        cursor.execute(select_low_salary_sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            
        print("\n--- ลองดูพนักงานตำแหน่งอื่นๆ housekeeping security ---")
        select_hk_secure_sql = "SELECT first_name, position FROM Employees WHERE position in ('Housekeeping', 'Security') LIMIT 2;"
        cursor.execute(select_hk_secure_sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

except sqlite3.Error as e:
    print(f"เกิดข้อผิดพลาดของ SQLite: {e}")
except Exception as e:
    print(f"เกิดข้อผิดพลาดทั่วไป: {e}")