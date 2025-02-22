import psycopg2
from os import getenv
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем параметры подключения к базе данных
db_params = {
    'host': getenv('DB_HOST'),
    'port': getenv('DB_PORT'),
    'dbname': getenv('DB_NAME'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD')
}

# SELECT
# Функция для проверки буллинга
def get_reaction_event():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("SELECT chat_id, user_id, emoji, event_duration, event_start FROM reaction_events;")
    reaction_events_cursor = cursor.fetchall()

    cursor.close()
    conn.close()

    return reaction_events_cursor


# INSERT
# Функция для вставки данных в таблицу булинга реакциями
def insert_reaction_event(chat_id, user_id, emoji, event_duration, event_start):
    query = """
        INSERT INTO reaction_events (chat_id, user_id, emoji, event_duration, event_start)
        VALUES (%s, %s, %s, %s, %s) RETURNING user_id;
    """
    return execute_insert(query, (chat_id, user_id, emoji, event_duration, event_start))


# DELETE
# Функция для удаления данных в таблице булинга реакциями
def delete_reaction_event(chat_id, user_id):
    query = f"""
            DELETE FROM reaction_events
            WHERE chat_id = %s AND user_id = %s;
            """
    execute_delete(query, (chat_id, user_id))


# Универсальная функция для выполнения вставки
def execute_insert(query, params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        result = cursor.fetchone()  # Получаем результат
        if result:  # Проверяем, есть ли данные
            return result[0]  # Возвращаем первый элемент
        else:
            print("Запрос выполнен, но не возвращает данных.")
            return 1  # Если результат пустой
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
        return None  # Возвращаем None в случае ошибки
    finally:
        cursor.close()
        conn.close()


# Универсальная функция для выполнения удаления
def execute_delete(query, params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return 1

    except Exception as e:
        print(f"Ошибка при удаление данных: {e}")
        return None

    finally:
        cursor.close()
        conn.close()
