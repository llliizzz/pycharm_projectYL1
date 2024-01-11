import sqlite3


def show_result():
    connection = sqlite3.connect('starry_rain1.sqlite')
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS 'top' (id INTEGER, Username TEXT, Balls INTEGER)")

    result = cursor.execute("""SELECT id, Username, Balls FROM top ORDER BY balls DESC limit 3""").fetchall()
    # cursor.execute(f'UPDATE pupils SET balls_test2={self.balls_2} WHERE id={id}')
    connection.commit()
    result_id = cursor.execute("""SELECT id FROM top ORDER BY id DESC limit 1""").fetchall()
    id_last = result_id[0][0]
    print(result_id)
    connection.commit()
    connection.close()

    fl = True
    for triple in result:
        if triple[0] == id_last:
            # вывести эти три тройки на акран(result)
            fl = False  # т е последний юзер встречается в тройке лидеров, отдельно не выводим
            break
    if fl:
        # вывести это 3 тройки на экран(result) + последний результат(last_result)
        connection = sqlite3.connect('starry_rain1.sqlite')
        cursor = connection.cursor()
        print(result)
        last_result = cursor.execute(f"SELECT id, Username, Balls FROM top WHERE id = {id_last}").fetchall()
        print(last_result)
        connection.commit()
        connection.close()
    else:
        print(result)

show_result()