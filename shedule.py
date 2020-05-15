import requests
from bs4 import BeautifulSoup
import datetime

# URL запроса
URL = 'http://schedule.sumdu.edu.ua/index/htmlschedule';

# Кастомный юзер агент
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 SSU_BOT'

# Инициализация сессии
s = requests.session();

s.headers['User-Agent'] = UA;



TIMES = ["08:15-09:35","09:50-11:10","11:25-12:45","13:25-14:45","15:00-16:20","16:35-17:55",
        "18:00-19:20","19:25-20:45"]



def GetShedule(time,group):

    if time == None or group == None:
        return 'Time is null!'
    LESSONS = []

    # Шаблон данных для запроса
    data = {'data[DATE_BEG]': time,
            'data[DATE_END]': time,
            'data[KOD_GROUP]': group,
            'data[ID_FIO]': '0',
            'data[ID_AUD]': '0',
            'data[PUB_DATE]': 'false',
            'data[PARAM]': '0'}

    # POST запрос на сервер SSU
    try:
        r = s.post(URL, data=data);
    except:
        print('Ошибка получения данных с сервера!')
        GetShedule(time,group)


    print("request data: " + r.text);

    if len(r.text) == 0:
        return LESSONS;

    # Инициализация html парсера BS
    soup = BeautifulSoup(r.text, 'html.parser')

    # Поиск всех элементов td
    shed_blocks = soup.find('tbody').find_all('td');

    i = 0;
    for block in shed_blocks:
        # Получаем все дочерние div тэги
        elements = block.find_all('div');

        # Проверка на наличие урока в блоке
        if len(elements[0].text) > 1:
            print(TIMES[i] + ": " + elements[0].text)
            lesson = {'Time': TIMES[i], 'Name': elements[0].text}

            # Если элемент перподавателя и аудитории определён
            if len(elements) > 3:
                lesson['teacher'] = elements[3].text;
                lesson['classroom'] = elements[2].text;

            LESSONS.append(lesson)

        i += 1;

    return LESSONS;

#GetShedule('04.03.2020','1001053');

def GetGroups():
    try:
        r = s.post('http://schedule.sumdu.edu.ua/');
    except:
        print("Ошибка получения списка групп!")
        GetGroups()

    soup = BeautifulSoup(r.text, 'html.parser')
    Groups = []
    options = soup.find('select', {'id': 'group'}).find_all('option')
    for option in options:
        opt = {'value': option.get('value'), 'group': option.text.upper()}
        Groups.append(opt);

    return Groups;

def GetTime():
    time = str(datetime.datetime.now().time()).split('.')[0]

    return '[' + time + ']'


