import sqlite3


# старт БД
def sql_start():
    global base, cur
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    if base:
        print("DB connected")
    else:
        print(" DB Connection problem")
    base.execute(
        "CREATE TABLE IF NOT EXISTS settings(user_id TEXT PRIMARY KEY, sites TEXT, categories TEXT, "
        "mode TEXT, keywords TEXT, price_range TEXT, number_of_responses TEXT, message_frequency TEXT)")
    base.commit()


# Регистрация/обновление данных
async def sql_add(state):
    async with state.proxy() as data:
        try:
            cur.execute('INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
            base.commit()
        except sqlite3.IntegrityError:
            cur.execute('DELETE FROM settings WHERE user_id == ?', (data["user_id"],))
            base.commit()
            cur.execute('INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
            base.commit()


# Получение значений. Если пользователя нет в БД, возвращает False
def sql_get(user_id):
    data = cur.execute("SELECT * FROM settings WHERE user_id == ?", (str(user_id),)).fetchone()

    # Данные не получены
    if not data:
        return False

    info = {
        "user_id": data[0],
        "sites": data[1].split(";"),
        "categories": data[2].split(";"),
        "mode": data[3],
        "keywords": data[4].split(";"),
        "price_range": data[5].split(";"),
        "number_of_responses": data[6],
        "message_frequency": data[7]
    }
    return info
