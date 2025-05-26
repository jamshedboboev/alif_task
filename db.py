from sqlite3 import connect, Error

create_table_query = """
    CREATE TABLE IF NOT EXISTS rooms_rent (
        room_id INTEGER PRIMARY KEY,
        room_name TEXT NOT NULL,
        customer TEXT,
        email TEXT,
        number TEXT,
        start TEXT,
        end TEXT);
"""

ROOMS = [
    (1, "Конференц-зал", 1, "Али", "Alichon@test.com", "+992987654321", "2024-05-28 10:00", "2024-05-28 11:00"),
    (2, "Переговорная A", 0, None, None, None, None, None),
    (3, "Переговорная B", 0, None, None, None, None, None),
    (4, "Открытая зона", 1, "Сухроб", "Suhrob_HR@test.com", "+992912345678", "2024-05-28 13:00", "2024-05-28 16:30"),
    (5, "Мини-офис", 0, None, None, None, None, None),
]

def init_database(query: str = create_table_query, db_path: str = "alif_task/office.db") -> None:
    try:
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def insert_rooms(insert_data: list[tuple] = ROOMS, db_path: str = "alif_task/office.db") -> None:
    try:
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                '''
                INSERT INTO rooms_rent (
                    room_id, room_name, status, customer, email, number, start, end
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                insert_data
            )
            conn.commit()
    except Error as e:
        print(f"Ошибка при добавлении данных: {e}")

init_database()
insert_rooms()