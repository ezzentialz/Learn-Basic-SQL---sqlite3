import sqlite3

db_file = 'hotel_management_test2.db' # ใช้ชื่อไฟล์ที่เราสร้างไว้เมื่อกี้

try:
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # ส่วนนี้เป็นโค้ดเดิมเพื่อสร้างตารางและใส่ข้อมูล
        # เพื่อให้มั่นใจว่าเรามีข้อมูลทดสอบพร้อมใช้งาน
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL
        );
        """
        cursor.execute(create_table_sql)
        # print("สร้างตาราง Employees สำเร็จ (หรือมีอยู่แล้ว)!") # คอมเมนต์ออกไปเพื่อให้ Output ไม่เยอะเกินไป

        # ถ้าเราต้องการให้ข้อมูลเริ่มต้นเหมือนเดิมทุกครั้งที่รัน
        # อาจจะลบข้อมูลเก่าก่อนแล้วค่อยเพิ่มใหม่ (ถ้าไม่มั่นใจว่าข้อมูลจะซ้ำ)
        # cursor.execute("DELETE FROM Employees;")
        # insert_initial_data_sql = """
        # INSERT INTO Employees (first_name, last_name, position, salary) VALUES
        # ('Somsak', 'Klinhom', 'Manager', 75000.00),
        # ('Suchart', 'Jaidee', 'Front Desk', 35000.00),
        # ('Pornchai', 'Wongyai', 'Housekeeping', 28000.00),
        # ('Siriporn', 'Khamdee', 'Front Desk', 38000.00),
        # ('Chaiyot', 'Rungsang', 'Security', 30000.00),
        # ('Aree', 'Sukjai', 'Manager', 68000.00),
        # ('Nongluck', 'Srisuk', 'Housekeeping', 27000.00),
        # ('Somkid', 'Deejai', 'Manager', 80000.00),
        # ('S','Good student','CEO', 100000.00);
        # """
        # try:
        #     cursor.execute(insert_initial_data_sql)
        #     conn.commit()
        #     print("เพิ่มข้อมูลเริ่มต้นสำหรับทดสอบสำเร็จ!")
        # except sqlite3.IntegrityError:
        #     print("ข้อมูลเริ่มต้นอาจจะถูกเพิ่มไปแล้ว.")

        print("\n--- การสรุปข้อมูลด้วย Aggregate Functions และ GROUP BY ---")

        # 1. COUNT(): นับจำนวนพนักงานทั้งหมด
        print("\n**1. จำนวนพนักงานทั้งหมด (COUNT(*))**")
        cursor.execute("SELECT COUNT(*) FROM Employees;")
        total_employees = cursor.fetchone()[0] # ดึงค่าแรกจากผลลัพธ์ที่เป็น Tuple  << ตรงนี้มีการใส่ index ตำแหน่งแรก เพราะถ้าไม่ใส่ จะมี ตัว , เข้ามาด้วย
        print(f"จำนวนพนักงานทั้งหมด: {total_employees} คน")
        
        # 2. SUM(): ผลรวมเงินเดือนทั้งหมด
        print("\n**2. ผลรวมเงินเดือนทั้งหมด (SUM(salary))**")
        cursor.execute("SELECT SUM(salary) FROM Employees;")
        total_salary = cursor.fetchone()[0] #<< พอลองถอด index แล้วเกิด error เพราะ tuple ไม่สามารถระบุเป็น str ได้
        print(f"ผลรวมเงินเดือนของพนักงานทั้งหมด: {total_salary:,.2f} บาท") # .2f เพื่อจัดรูปแบบทศนิยม 2 ตำแหน่ง

        # 3. AVG(): เงินเดือนเฉลี่ยทั้งหมด
        print("\n**3. เงินเดือนเฉลี่ยทั้งหมด (AVG(salary))**")
        cursor.execute("SELECT AVG(salary) FROM Employees;")
        avg_salary = cursor.fetchone()[0]
        print(f"เงินเดือนเฉลี่ยของพนักงานทั้งหมด: {avg_salary:,.2f} บาท")

        # 4. MAX() และ MIN(): เงินเดือนสูงสุดและต่ำสุด
        print("\n**4. เงินเดือนสูงสุดและต่ำสุด (MAX(salary), MIN(salary))**")
        cursor.execute("SELECT MAX(salary), MIN(salary) FROM Employees;")
        max_min_salary = cursor.fetchone() 
        print(f"Debug max_min_salary: อยากรู้ว่ามีค่าอะไรบ้าง {max_min_salary}") # มี index 2 ตัวแหน่ง แยกเป็น value max และ min 
        print(f"เงินเดือนสูงสุด: {max_min_salary[0]:,.2f} บาท, เงินเดือนต่ำสุด: {max_min_salary[1]:,.2f} บาท") #ตอนprint มีการกำหนด index เพื่อแยกว่าอันไหนเป็น max และ min

        # ----------------------------------------------------
        # 5. GROUP BY: สรุปข้อมูลตามกลุ่ม
        print("\n**5. จำนวนพนักงานในแต่ละตำแหน่ง (GROUP BY position)**")
        group_by_position_count_sql = """
        SELECT position, COUNT(*) AS total_employees
        FROM Employees
        GROUP BY position;
        """
        cursor.execute(group_by_position_count_sql)
        for row in cursor.fetchall():
            print(f"Debug row: อยากรู้ ค่าทั้งหมดของrow {row}") # มี2ค่า คือ position, total_employees(จำนวนนับรวมทั้งหมด)
            print(f"ตำแหน่ง: {row[0]}, จำนวนพนักงาน: {row[1]} คน")

        print("\n**6. เงินเดือนเฉลี่ยในแต่ละตำแหน่ง (GROUP BY position พร้อม AVG)**")
        group_by_position_avg_sql = """
        SELECT position, AVG(salary) AS avg_salary
        FROM Employees
        GROUP BY position;
        """
        cursor.execute(group_by_position_avg_sql)
        for row in cursor.fetchall():
            print(f"ตำแหน่ง: {row[0]}, เงินเดือนเฉลี่ย: {row[1]:,.2f} บาท")

        print("\n**7. เงินเดือนรวม, เฉลี่ย, สูงสุด, ต่ำสุด และจำนวนพนักงานในแต่ละตำแหน่ง (Multiple Aggregates with GROUP BY)**")
        all_aggregates_sql = """
        SELECT
            position,
            COUNT(*) AS total_employees,
            SUM(salary) AS total_salary,
            AVG(salary) AS avg_salary,
            MAX(salary) AS max_salary,
            MIN(salary) AS min_salary
        FROM Employees
        GROUP BY position;
        """
        cursor.execute(all_aggregates_sql)
        print(f"{'ตำแหน่ง':<25} {'จำนวน':<8} {'รวมเงินเดือน':<15} {'เฉลี่ย':<10} {'สูงสุด':<10} {'ต่ำสุด':<10}") #อะไรคือ :<25 , :<8 , :<15? คิดว่าน่าจะเป็น len(str)
        print("-" * 80)
        for row in cursor.fetchall():
            print(f"{row[0]:<25} {row[1]:<8} {row[2]:<15,.2f} {row[3]:<10,.2f} {row[4]:<10,.2f} {row[5]:<10,.2f}")

        # 8. HAVING: กรองกลุ่มข้อมูล
        print("\n**8. ตำแหน่งที่มีพนักงานมากกว่า 1 คน และเงินเดือนเฉลี่ยมากกว่า 40000 บาท (GROUP BY พร้อม HAVING)**")
        having_clause_sql = """
        SELECT position, AVG(salary) AS avg_salary, COUNT(*) AS num_employees
        FROM Employees
        GROUP BY position
        HAVING COUNT(*) > 1 AND AVG(salary) > 40000;
        """
        cursor.execute(having_clause_sql)
        for row in cursor.fetchall():
            print(f"ตำแหน่ง: {row[0]}, เงินเดือนเฉลี่ย: {row[1]:,.2f} บาท, จำนวนพนักงาน: {row[2]} คน") #จากในฐานข้อมูล ไม่มีตำแหน่งไหนมีคนมากกว่า ทำให้ไม่ตรงกับเงื่อนไข เลยไม่มีอะไรปริ๊นออกมา
            

except sqlite3.Error as e:
    print(f"เกิดข้อผิดพลาดของ SQLite: {e}")
except Exception as e:
    print(f"เกิดข้อผิดพลาดทั่วไป: {e}")