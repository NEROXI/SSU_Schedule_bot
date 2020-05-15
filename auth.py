import sqlite3
import shedule
import telebot.types as types
import datetime



conn = sqlite3.connect("users.db", check_same_thread = False)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
try:
    cursor.execute("""CREATE TABLE users
                  (login text, grp text, grp_id text)
               """)
    print("Database created!")
except:
    print("Database loaded!")

def AuthUser(message,bot):
    sql = "SELECT * FROM users WHERE login='{0}'".format(message.from_user.username)
    cursor.execute(sql)
    conn.commit()

    data_len = len(cursor.fetchall())
    # Проверяем наличие студента в БД
    if data_len == 0:
        print("User not found!")

        # Добавляем в БД логин
        insert_sql = "INSERT INTO users (login) VALUES ('{0}')".format(message.from_user.username)

        cursor.execute(insert_sql)
        conn.commit()
        print(cursor.fetchall())
        bot.send_message(message.chat.id, 'Напишите название своей группы')
    else:
        sql = "SELECT * FROM users WHERE login='{0}'".format(message.from_user.username)
        cursor.execute(sql)
        conn.commit()

        user_data = cursor.fetchall()[0]

        # Группа стедента == None
        if user_data[1] == None:
            print('Start get group')
            Groups = shedule.GetGroups()

            selected_group = None

            for group in Groups:
                if message.text.upper() == group['group']:
                    print('Selected ' + group['group'])
                    selected_group = group

            if selected_group == None:
                bot.send_message(message.chat.id, 'Неверно указано название группы!')
            else:
                sql = "UPDATE users SET grp = '{0}', grp_id = {1} WHERE login = '{2}'".format(selected_group['group'], selected_group['value'], message.from_user.username)
                cursor.execute(sql)
                conn.commit()

                date = str(datetime.datetime.today().date()).split('-')
                date = date[2] + '.' + date[1] + '.' + date[0]



                Lessons = shedule.GetShedule(date,selected_group['value'])

                lessons_msg = ''
                for lesson in Lessons:
                    lessons_msg += '*{0}*\n{1}\n{2}\n{3}\n\n'.format(lesson['Time'], lesson['Name'], lesson['teacher'],
                                                                     lesson['classroom'])

                markup = types.InlineKeyboardMarkup()
                switch_button = types.InlineKeyboardButton(text=date, switch_inline_query="*")
                markup.add(switch_button)
                shedule_button = types.InlineKeyboardButton(text='Расписание')
                markup.add(shedule_button)

                bot.send_message(message.chat.id, text=lessons_msg, parse_mode="Markdown", reply_markup=markup)



        # Если у стедента выбрана его группа
        else:
            date = str(datetime.datetime.today().date()).split('-')
            date = date[2] + '.' + date[1] + '.' + date[0]


            Lessons = shedule.GetShedule(date, user_data[2])

            lessons_msg = ''
            for lesson in Lessons:
                lessons_msg += '*{0}*\n{1}\n{2}\n{3}\n\n'.format(lesson['Time'], lesson['Name'], lesson['teacher'],
                                                                 lesson['classroom'])

            markup = types.InlineKeyboardMarkup()
            switch_button = types.InlineKeyboardButton(text=date, switch_inline_query="*")
            markup.add(switch_button)

            bot.send_message(message.chat.id, text=lessons_msg, parse_mode="Markdown", reply_markup=markup)




