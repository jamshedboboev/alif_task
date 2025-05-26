from datetime import datetime
from loguru import logger
from routers import get_room, add_room


def notify_customer(customer: str, email: str, phone: str,
                    room_name: str, start: str, end: str):
    """Симулирует отправку уведомления заказчику"""

    logger.info(f"Уведомление отправлено:")
    logger.info(f"Кабинет: {room_name}")
    logger.info(f"Имя: {customer}, Email: {email}, Телефон: {phone}")
    logger.info(f"Забронирован с {start} до {end}\n")


def check_and_book():
    room_name = input("Введите название комнаты: ").strip()
    query_time = input("Начало бронирования (ГГГГ-ММ-ДД ЧЧ:ММ): ").strip()

    # cross-check
    try:
        query_dt = datetime.strptime(query_time, "%Y-%m-%d %H:%M")
    except ValueError:
        logger.error("Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ")
        return

    df = get_room(room_name)

    if df is None or df.empty:
        logger.error("Комната не найдена.")
        return

    for _, row in df.iterrows():
        if row["status"] == 1:
            start_dt = datetime.strptime(row["start"], "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(row["end"], "%Y-%m-%d %H:%M")
            if start_dt <= query_dt <= end_dt:
                logger.info(f"Комната занята заказчиком {row['customer']} с {row['start']} до {row['end']}")
                return

    logger.info("Комната доступна. Пожалуйста, введите данные для бронирования:")

    customer = input("Имя заказчика: ").strip()
    email = input("Email: ").strip()
    phone = input("Телефон: ").strip()
    end = input("Окончание бронирования (ГГГГ-ММ-ДД ЧЧ:ММ): ").strip()

    success = add_room(room_name, customer, email, phone, query_time, end)

    if success:
        notify_customer(customer, email, phone, room_name, query_time, end)


if __name__ == "__main__":
    print("Добро пожаловать в систему бронирования кабинетов")
    check_and_book()