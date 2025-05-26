from sqlite3 import connect, Error
import pandas as pd

def get_room(room_name: str, db_path: str = "alif_task/office.db"):
    """Полуает запись из таблицы rooms_rent"""

    try:
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms_rent WHERE room_name = ?", (room_name,))
            row = cursor.fetchall()

            return pd.DataFrame(row, columns=['room_name', 'status', 'customer', 'email', 'number', 'start', 'end'])
        
    except Error as e:
        print(f"Ошибка при чтении данных: {e}")
        return False

def add_room(
    room_name: str,
    customer: str,
    email: str,
    number: str,
    start: str,
    end: str,
    status: int = 1,
    db_path: str = "alif_task/office.db"
) -> bool:
    """Добавляет новую запись в таблицу rooms_rent"""

    insert_query = """
        INSERT INTO rooms_rent (
            room_name, status, customer, email, number, start, end
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    try:
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (room_name, status, customer, email, number, start, end))
            conn.commit()

            print(f"Бронь комнаты {room_name}, с {start} до {end}")
            return True

    except Error as e:
        print(f"Ошибка при добавлении данных: {e}")
        return False