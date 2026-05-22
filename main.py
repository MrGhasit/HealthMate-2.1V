import json
import os
import threading
import urllib.request
import urllib.parse
from datetime import datetime, date
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner

import platform
if platform.system() in ('Windows', 'Darwin', 'Linux'):
    Window.size = (400, 700)

# ──────────────────────────────────────────────────
#  ЛОКАЛИЗАЦИЯ
# ──────────────────────────────────────────────────
TRANSLATIONS = {
    'RU': {
        'app_name': 'HealthMate',
        'subtitle': 'Диетотерапия и ЛФК',
        'start': 'Начать',
        'welcome': 'Добро пожаловать!',
        'login_subtitle': 'Войдите или продолжите как гость',
        'login': 'Войти',
        'register': 'Регистрация',
        'or': '— или —',
        'guest': 'Продолжить как гость',
        'home': 'Главная',
        'diet_tab': 'Режим',
        'chat_tab': 'Чат',
        'weather_tab': 'Погода',
        'profile_tab': 'Профиль',
        'reminders': 'Напоминания',
        'diet': 'Диетотерапия',
        'lfk': 'ЛФК',
        'calendar': 'Расписание',
        'settings': 'Профиль и настройки',
        'weather': 'Погода',
        'community': 'Сообщество',
        'ai_chat': 'Ваш личный помощник',
        'support': 'Техническая поддержка',
        'language': 'Сменить язык',
        'dark_mode': 'Темная тема',
        'notifications': 'Уведомления',
        'notif_screen': 'Уведомления на экране',
        'security': 'БЕЗОПАСНОСТЬ',
        'main_section': 'ОСНОВНОЕ',
        'other': 'ДРУГОЕ',
        'invite': 'Пригласить друзей',
        'delete_profile': 'Удалить профиль',
        'pin': 'Touch ID / PIN-код',
        'set': 'Задать',
        'guest_label': 'Гость',
        'guest_account': 'Гостевой аккаунт',
        'registered': 'Зарегистрирован',
        'privacy': 'Личные данные никто не видит.\nВы можете в любой момент удалить профиль.',
        'data_safe': 'Ваши данные защищены. Личные данные никто не видит.',
        'find': 'Найти',
        'city_hint': 'Выберите город...',
        'weather_hint': 'Выберите город и нажмите Найти\nдля прогноза',
        'loading': 'Загрузка...',
        'today': 'Сегодня',
        'tomorrow': 'Завтра',
        'max': 'Макс',
        'min': 'Мин',
        'precip': 'Осадки',
        'mm': 'мм',
        'send': '>',
        'type_msg': 'Написать сообщение...',
        'back': '<',
        'close': 'Закрыть',
        'breakfast': 'Завтрак',
        'lunch': 'Обед',
        'snack': 'Полдник',
        'dinner': 'Ужин',
        'sleep': 'Сон',
        'day': 'День',
        'diet_day': 'Диета — день',
        'lfk_day': 'ЛФК — день',
        'schedule_30': 'Расписание 30 дней',
        'daily_regime': 'Ежедневный режим питания и отдыха',
        'main_meal': 'Основной приём пищи',
        'light_snack': 'Лёгкий перекус',
        'light_dinner': 'Лёгкий ужин',
        'rest_time': 'Время отдыха и восстановления',
        'meal_time': 'Время приёма пищи',
        'click_menu': 'нажмите чтобы увидеть меню',
        'save': 'Сохранить',
        'cancel': 'Отмена',
        'enter_pin': 'Введите 4-значный PIN',
        'need_4': 'Нужно ровно 4 цифры!',
        'pin_title': 'Установить PIN',
        'invite_msg': 'Приложения нет\nв открытом доступе',
        'invitation': 'Приглашение',
        'delete_title': 'Удаление профиля',
        'delete_confirm': 'Вы уверены, что хотите\nудалить профиль?',
        'delete': 'Удалить',
        'info': 'Информация',
        'ok': 'OK',
        'city_not_found': 'Город не найден',
        'conn_error': 'Ошибка соединения',
        'chat_welcome': 'Добро пожаловать в чат Сообщество!',
        'trainer': 'Тренер Алина',
        'trainer_msg': 'Привет! Добро пожаловать в чат!',
        'user1': 'Михаил',
        'user1_msg': '2 недели по программе — уже лучше!',
        'user2': 'Светлана',
        'user2_msg': 'Сегодня выполнила всё ЛФК!',
        'ai_welcome': 'Привет! Я ваш личный помощник по здоровью. Задайте любой вопрос о питании, упражнениях или самочувствии.',
        'support_welcome': 'Здравствуйте! Техническая поддержка HealthMate. Чем могу помочь?',
        'you': 'Вы',
        'reg_email': 'Введите email',
        'reg_password': 'Введите пароль',
        'reg_confirm': 'Подтвердите пароль',
        'reg_btn': 'Зарегистрироваться',
        'back_btn': 'Вернуться',
        'email_error': 'Неверный формат email',
        'pass_error': 'Пароль слишком короткий (мин. 6 символов)',
        'confirm_error': 'Пароли не совпадают',
        'register_screen': 'Создать аккаунт',
    },
    'EN': {
        'app_name': 'HealthMate',
        'subtitle': 'Diet Therapy & Physical Therapy',
        'start': 'Start',
        'welcome': 'Welcome!',
        'login_subtitle': 'Sign in or continue as guest',
        'login': 'Sign In',
        'register': 'Register',
        'or': '— or —',
        'guest': 'Continue as Guest',
        'home': 'Home',
        'diet_tab': 'Diet',
        'chat_tab': 'Chat',
        'weather_tab': 'Weather',
        'profile_tab': 'Profile',
        'reminders': 'Reminders',
        'diet': 'Diet Therapy',
        'lfk': 'Physical Therapy',
        'calendar': 'Schedule',
        'settings': 'Profile & Settings',
        'weather': 'Weather',
        'community': 'Community',
        'ai_chat': 'Your Personal Assistant',
        'support': 'Technical Support',
        'language': 'Change Language',
        'dark_mode': 'Dark Mode',
        'notifications': 'Notifications',
        'notif_screen': 'On-screen Notifications',
        'security': 'SECURITY',
        'main_section': 'GENERAL',
        'other': 'OTHER',
        'invite': 'Invite Friends',
        'delete_profile': 'Delete Profile',
        'pin': 'Touch ID / PIN',
        'set': 'Set',
        'guest_label': 'Guest',
        'guest_account': 'Guest Account',
        'registered': 'Registered',
        'privacy': 'Your data is private.\nYou can delete your profile at any time.',
        'data_safe': 'Your data is protected.',
        'find': 'Find',
        'city_hint': 'Select city...',
        'weather_hint': 'Select city and press Find\nfor forecast',
        'loading': 'Loading...',
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'max': 'Max',
        'min': 'Min',
        'precip': 'Precip',
        'mm': 'mm',
        'send': '>',
        'type_msg': 'Write a message...',
        'back': '<',
        'close': 'Close',
        'breakfast': 'Breakfast',
        'lunch': 'Lunch',
        'snack': 'Snack',
        'dinner': 'Dinner',
        'sleep': 'Sleep',
        'day': 'Day',
        'diet_day': 'Diet — day',
        'lfk_day': 'PT — day',
        'schedule_30': '30-Day Schedule',
        'daily_regime': 'Daily eating and rest schedule',
        'main_meal': 'Main meal',
        'light_snack': 'Light snack',
        'light_dinner': 'Light dinner',
        'rest_time': 'Rest and recovery time',
        'meal_time': 'Meal time',
        'click_menu': 'tap to see menu',
        'save': 'Save',
        'cancel': 'Cancel',
        'enter_pin': 'Enter 4-digit PIN',
        'need_4': 'Must be exactly 4 digits!',
        'pin_title': 'Set PIN',
        'invite_msg': 'App not\npublicly available',
        'invitation': 'Invitation',
        'delete_title': 'Delete Profile',
        'delete_confirm': 'Are you sure you want\nto delete your profile?',
        'delete': 'Delete',
        'info': 'Information',
        'ok': 'OK',
        'city_not_found': 'City not found',
        'conn_error': 'Connection error',
        'chat_welcome': 'Welcome to Community chat!',
        'trainer': 'Coach Alina',
        'trainer_msg': 'Hello! Welcome to the chat!',
        'user1': 'Michael',
        'user1_msg': '2 weeks on the program — already feeling better!',
        'user2': 'Svetlana',
        'user2_msg': 'Completed all PT exercises today!',
        'ai_welcome': 'Hi! I am your personal health assistant.',
        'support_welcome': 'Hello! HealthMate Technical Support.',
        'you': 'You',
        'reg_email': 'Enter email',
        'reg_password': 'Enter password',
        'reg_confirm': 'Confirm password',
        'reg_btn': 'Create Account',
        'back_btn': 'Go Back',
        'email_error': 'Invalid email format',
        'pass_error': 'Password too short (min. 6 characters)',
        'confirm_error': 'Passwords do not match',
        'register_screen': 'Create Account',
    },
    'KZ': {
        'app_name': 'HealthMate',
        'subtitle': 'Диеттерапия және ЕДШ',
        'start': 'Бастау',
        'welcome': 'Қош келдіңіз!',
        'login_subtitle': 'Кіріңіз немесе қонақ ретінде жалғастырыңыз',
        'login': 'Кіру',
        'register': 'Тіркелу',
        'or': '— немесе —',
        'guest': 'Қонақ ретінде жалғастыру',
        'home': 'Басты',
        'diet_tab': 'Режим',
        'chat_tab': 'Чат',
        'weather_tab': 'Ауа-райы',
        'profile_tab': 'Профиль',
        'reminders': 'Еске салғыштар',
        'diet': 'Диеттерапия',
        'lfk': 'ЕДШ',
        'calendar': 'Кесте',
        'settings': 'Профиль және параметрлер',
        'weather': 'Ауа-райы',
        'community': 'Қауымдастық',
        'ai_chat': 'Жеке көмекшіңіз',
        'support': 'Техникалық қолдау',
        'language': 'Тілді өзгерту',
        'dark_mode': 'Күңгірт тақырып',
        'notifications': 'Хабарландырулар',
        'notif_screen': 'Экрандағы хабарландырулар',
        'security': 'ҚАУІПСІЗДІК',
        'main_section': 'НЕГІЗГІ',
        'other': 'БАСҚА',
        'invite': 'Достарды шақыру',
        'delete_profile': 'Профильді жою',
        'pin': 'Touch ID / PIN-код',
        'set': 'Орнату',
        'guest_label': 'Қонақ',
        'guest_account': 'Қонақ аккаунты',
        'registered': 'Тіркелген',
        'privacy': 'Жеке деректеріңіз жасырын.\nКез келген уақытта профильді жоюға болады.',
        'data_safe': 'Деректеріңіз қорғалған.',
        'find': 'Іздеу',
        'city_hint': 'Қаланы таңдаңыз...',
        'weather_hint': 'Қаланы таңдап, Іздеу басыңыз\nболжам үшін',
        'loading': 'Жүктелуде...',
        'today': 'Бүгін',
        'tomorrow': 'Ертең',
        'max': 'Макс',
        'min': 'Мин',
        'precip': 'Жауын-шашын',
        'mm': 'мм',
        'send': '>',
        'type_msg': 'Хабар жазыңыз...',
        'back': '<',
        'close': 'Жабу',
        'breakfast': 'Таңғы ас',
        'lunch': 'Түскі ас',
        'snack': 'Аралық тамақ',
        'dinner': 'Кешкі ас',
        'sleep': 'Ұйқы',
        'day': 'Күн',
        'diet_day': 'Диета — күн',
        'lfk_day': 'ЕДШ — күн',
        'schedule_30': '30 күндік кесте',
        'daily_regime': 'Күнделікті тамақтану және демалыс режимі',
        'main_meal': 'Негізгі тамақтану',
        'light_snack': 'Жеңіл тағам',
        'light_dinner': 'Жеңіл кешкі ас',
        'rest_time': 'Демалыс және қалпына келу уақыты',
        'meal_time': 'Тамақтану уақыты',
        'click_menu': 'мәзірді көру үшін басыңыз',
        'save': 'Сақтау',
        'cancel': 'Болдырмау',
        'enter_pin': '4 санды PIN енгізіңіз',
        'need_4': 'Дәл 4 сан болуы керек!',
        'pin_title': 'PIN орнату',
        'invite_msg': 'Қолданба\nашық қолжетімді емес',
        'invitation': 'Шақыру',
        'delete_title': 'Профильді жою',
        'delete_confirm': 'Профильді жойғыңыз\nкелетіні сенімдісіз бе?',
        'delete': 'Жою',
        'info': 'Ақпарат',
        'ok': 'OK',
        'city_not_found': 'Қала табылмады',
        'conn_error': 'Қосылу қатесі',
        'chat_welcome': 'Қауымдастық чатына қош келдіңіз!',
        'trainer': 'Жаттықтырушы Алина',
        'trainer_msg': 'Сәлем! Чатқа қош келдіңіз!',
        'user1': 'Михаил',
        'user1_msg': 'Бағдарлама бойынша 2 апта — жақсы нәтиже!',
        'user2': 'Светлана',
        'user2_msg': 'Бүгін барлық ЕДШ жаттығуларын орындадым!',
        'ai_welcome': 'Сәлем! Мен сіздің жеке денсаулық көмекшіңізбін.',
        'support_welcome': 'Сәлем! HealthMate техникалық қолдауы.',
        'you': 'Сіз',
        'reg_email': 'Email енгізіңіз',
        'reg_password': 'Құпиясөз енгізіңіз',
        'reg_confirm': 'Құпиясөзді растаңыз',
        'reg_btn': 'Тіркелу',
        'back_btn': 'Артқа',
        'email_error': 'Email форматы дұрыс емес',
        'pass_error': 'Құпиясөз тым қысқа (мин. 6 таңба)',
        'confirm_error': 'Құпиясөздер сәйкес келмейді',
        'register_screen': 'Аккаунт жасау',
    }
}

current_lang = ['RU']

def t(key):
    lang = current_lang[0]
    return TRANSLATIONS.get(lang, TRANSLATIONS['RU']).get(key, TRANSLATIONS['RU'].get(key, key))

# ──────────────────────────────────────────────────
#  ГОРОДА КАЗАХСТАНА
# ──────────────────────────────────────────────────
KZ_CITIES = [
    'Алматы', 'Астана', 'Шымкент', 'Актобе', 'Тараз',
    'Павлодар', 'Усть-Каменогорск', 'Семей', 'Атырау', 'Костанай',
    'Кызылорда', 'Уральск', 'Петропавловск', 'Актау', 'Темиртау',
    'Туркестан', 'Балхаш', 'Жезказган', 'Экибастуз', 'Рудный',
    'Жанаозен', 'Талдыкорган', 'Кокшетау', 'Щучинск', 'Жаркент',
    'Риддер', 'Степногорск', 'Байконыр', 'Аральск', 'Каратау',
]

# ──────────────────────────────────────────────────
#  ДАННЫЕ: Диета №15 на 30 дней
# ──────────────────────────────────────────────────
DIET_PLAN = [
    {"breakfast":"Овсяная каша с яблоком","lunch":"Куриный суп с овощами","snack":"Кефир + груша","dinner":"Куриная грудка + брокколи"},
    {"breakfast":"Творог с медом и орехами","lunch":"Суп-пюре из тыквы + индейка","snack":"Запеченное яблоко","dinner":"Рыба на пару + бурый рис"},
    {"breakfast":"Яйца всмятку + тост","lunch":"Борщ без зажарки + курица","snack":"Смузи банан+кефир","dinner":"Тушеные овощи + индейка"},
    {"breakfast":"Манная каша + ягоды","lunch":"Щи из капусты + говядина","snack":"Кефир + хлебец","dinner":"Запеченный минтай + гречка"},
    {"breakfast":"Гречневая каша молочная","lunch":"Уха из горбуши","snack":"Творог с ягодами","dinner":"Паровые котлеты + цветная капуста"},
    {"breakfast":"Омлет 2 яйца + огурец","lunch":"Рисовый суп с курицей","snack":"Банан + орехи","dinner":"Куриное филе + картофель"},
    {"breakfast":"Пшённая каша с тыквой","lunch":"Суп-минестроне + телятина","snack":"Натуральный йогурт","dinner":"Треска запеченная + горошек"},
    {"breakfast":"Мюсли без сахара + молоко","lunch":"Гороховый суп + котлета","snack":"Кефир + хлебец","dinner":"Тушеная капуста + куриное филе"},
    {"breakfast":"Творожная запеканка","lunch":"Куриный бульон + вермишель","snack":"Яблоко + миндаль","dinner":"Запеченный лосось + рис"},
    {"breakfast":"Геркулес с изюмом","lunch":"Суп из чечевицы + индейка","snack":"Смузи шпинат+яблоко","dinner":"Паровые рыбные котлеты + брокколи"},
    {"breakfast":"Яичница + помидор + тост","lunch":"Суп с фрикадельками","snack":"Творог с медом","dinner":"Тушеная говядина + гречка"},
    {"breakfast":"Рисовая каша молочная","lunch":"Окрошка на кефире","snack":"Грейпфрут + кешью","dinner":"Запеченная треска + бурый рис"},
    {"breakfast":"Овсянка с бананом","lunch":"Суп-лапша куриная","snack":"Кефир + хлебец","dinner":"Куриное филе с грибами + пшено"},
    {"breakfast":"Гречка + яйцо","lunch":"Рассольник + говядина","snack":"Натуральный йогурт + груша","dinner":"Паровой хек + цветная капуста"},
    {"breakfast":"Творог + банан + корица","lunch":"Суп из кабачков + котлета","snack":"Яблоко + фундук","dinner":"Запеченная индейка + картофель"},
    {"breakfast":"Пшённая каша молочная","lunch":"Борщ постный + курица","snack":"Смузи клубника+кефир","dinner":"Запеченный минтай + гречка"},
    {"breakfast":"Омлет с овощами","lunch":"Уха из трески","snack":"Кефир + хлебец","dinner":"Тушеные кабачки + индейка + рис"},
    {"breakfast":"Геркулес с черникой","lunch":"Суп гречневый с курицей","snack":"Банан + миндаль","dinner":"Паровые котлеты говяжьи + брокколи"},
    {"breakfast":"Яйца всмятку + тост","lunch":"Суп-пюре из горошка","snack":"Творог с киви","dinner":"Запеченный лосось + картофель"},
    {"breakfast":"Манная каша молочная","lunch":"Щи с грибами + курица","snack":"Кефир + груша","dinner":"Тушеная рыба с морковью + пшено"},
    {"breakfast":"Гречка молочная","lunch":"Рисовый суп с курицей","snack":"Смузи шпинат+банан","dinner":"Куриное филе запеченное + гречка"},
    {"breakfast":"Творожная запеканка","lunch":"Суп с чечевицей + котлета","snack":"Запеченное яблоко + орехи","dinner":"Треска на пару + бурый рис"},
    {"breakfast":"Овсянка с яблоком","lunch":"Борщ с телятиной","snack":"Натуральный йогурт + киви","dinner":"Запеченная индейка + брокколи"},
    {"breakfast":"Мюсли + молоко","lunch":"Куриный суп с рисом","snack":"Кефир + хлебец","dinner":"Паровой минтай + цветная капуста"},
    {"breakfast":"Яичница + помидор + тост","lunch":"Суп с фрикадельками","snack":"Смузи малина+творог","dinner":"Тушеная говядина с овощами + гречка"},
    {"breakfast":"Пшённая каша с тыквой","lunch":"Гороховый суп + курица","snack":"Банан + миндаль","dinner":"Запеченный хек с морковью + рис"},
    {"breakfast":"Геркулес с изюмом","lunch":"Суп-лапша с индейкой","snack":"Творог с медом + груша","dinner":"Куриное филе с кабачком + гречка"},
    {"breakfast":"Омлет + зелень + огурец","lunch":"Рассольник + телятина","snack":"Кефир + хлебец","dinner":"Лосось запеченный + брокколи"},
    {"breakfast":"Гречка + яйцо вкрутую","lunch":"Суп из кабачков с рисом + котлета","snack":"Смузи яблоко+кефир","dinner":"Запеченная индейка + пшено"},
    {"breakfast":"Творог с ягодами","lunch":"Борщ с говядиной","snack":"Натуральный йогурт + киви","dinner":"Рыба на пару + гречка + салат"},
]

# ──────────────────────────────────────────────────
#  ДАННЫЕ: ЛФК на 30 дней
# ──────────────────────────────────────────────────
LFK_PLAN = [
    {"title":"Дыхательная гимнастика","exercises":["Диафрагмальное дыхание — 10 мин","Медленные вдохи через нос — 15 раз","Выдох трубочкой — 15 раз","Подъём рук на вдохе лёжа — 10 раз"]},
    {"title":"Суставная разминка","exercises":["Вращение кистями — 10 раз","Вращение локтями — 10 раз","Вращение плечами — 10 раз","Наклоны головы — 8 раз"]},
    {"title":"Упражнения лёжа","exercises":["Сжимание пальцев — 15 раз","Подъём ноги лёжа — 10 раз","Велосипед лёжа — 30 сек","Мост (ягодицы вверх) — 10 раз"]},
    {"title":"Упражнения сидя","exercises":["Подъём на носки сидя — 15 раз","Разгибание колена — 10 раз","Наклоны туловища — 8 раз","Повороты корпуса — 8 раз"]},
    {"title":"Лёгкая растяжка","exercises":["Растяжка плеч — 2 мин","Наклон к ногам сидя — 10 раз","Растяжка икр — 1 мин","Кошка-корова — 10 раз"]},
    {"title":"Дыхание и релаксация","exercises":["Брюшное дыхание — 5 мин","Мышечная релаксация — 10 мин","Медитация лёжа — 5 мин"]},
    {"title":"Ходьба и равновесие","exercises":["Медленная ходьба — 10 мин","Стойка на одной ноге — 30 сек","Ходьба пятками — 2 мин","Ходьба на носках — 2 мин"]},
    {"title":"Упражнения для рук","exercises":["Сжимание мячика — 15 раз","Подъём рук вперёд — 10 раз","Разведение рук — 10 раз","Растяжка пальцев — 2 мин"]},
    {"title":"Укрепление спины","exercises":["Лодочка лёжа — 10 раз","Кошка-корова — 10 раз","Боковые наклоны — 10 раз","Повороты шеи — 8 раз"]},
    {"title":"Упражнения для ног","exercises":["Подъём ног лёжа — 10 раз","Сгибание колен стоя — 15 раз","Отведение ноги — 10 раз","Тяга пятки к ягодице — 10 раз"]},
    {"title":"Координация","exercises":["Ходьба по линии — 2 мин","Перешагивание — 5 мин","Марш на месте — 3 мин","Восьмёрки ногой — 10 раз"]},
    {"title":"Укрепление пресса","exercises":["Подъём головы лёжа — 10 раз","Втягивание живота — 10 раз","Подъём согнутых ног — 10 раз","Боковые скручивания — 8 раз"]},
    {"title":"Дыхание и суставы","exercises":["Полное дыхание — 5 мин","Вращение голеностопом — 10 раз","Вращение тазом — 10 раз","Потягивание — 2 мин"]},
    {"title":"Активный день","exercises":["Ходьба на улице — 20 мин","Приседания с опорой — 10 раз","Подъём на носки — 15 раз","Растяжка — 5 мин"]},
    {"title":"День восстановления","exercises":["Массаж кистей — 5 мин","Тёплая ванна для ног — 10 мин","Глубокое дыхание — 5 мин","Растяжка перед сном — 5 мин"]},
    {"title":"Равновесие","exercises":["Стойка у стены на носках — 1 мин","Перекаты с пятки на носок — 15 раз","Покачивание стоя — 2 мин","Ходьба с поворотами — 5 мин"]},
    {"title":"Комплекс для плеч","exercises":["Пожимание плечами — 15 раз","Вращение плечами — 10 раз","Разведение лопаток — 10 раз","Наклоны головы — 8 раз"]},
    {"title":"Лёжа и дыхание","exercises":["Мост — 10 раз","Велосипед — 30 сек","Дыхательные упражнения — 5 мин","Расслабление тела — 5 мин"]},
    {"title":"Мягкая нагрузка","exercises":["Ходьба — 15 мин","Подъём на носки — 15 раз","Марш с подъёмом колен — 2 мин","Растяжка икр — 2 мин"]},
    {"title":"Укрепление кора","exercises":["Планка на локтях — 20 сек","Боковая планка — 15 сек","Рука+нога противоположные — 10 раз","Скручивания мягкие — 10 раз"]},
    {"title":"День растяжки","exercises":["Растяжка тела лёжа — 5 мин","Растяжка бёдер — 2 мин","Растяжка плеч — 2 мин","Поза ребёнка — 3 мин"]},
    {"title":"Активация","exercises":["Мягкие прыжки — 30 сек","Приседания — 10 раз","Выпады вперёд — 8 раз","Ходьба на месте — 5 мин"]},
    {"title":"Суставы и дыхание","exercises":["Вращение суставов — 10 мин","Полное дыхание — 5 мин","Потягивание — 2 мин"]},
    {"title":"С эспандером","exercises":["Сгибание руки — 10 раз","Разгибание — 10 раз","Подъём ноги — 10 раз","Растяжка — 2 мин"]},
    {"title":"Осанка и дыхание","exercises":["Дыхание у стены — 5 мин","Прогиб назад — 10 раз","Стойка с ровной спиной — 3 мин","Растяжка груди — 2 мин"]},
    {"title":"Лёгкое кардио","exercises":["Ходьба — 25 мин","Подъём по ступеням — 5 мин","Растяжка после ходьбы — 5 мин"]},
    {"title":"Полное расслабление","exercises":["Глубокое дыхание — 10 мин","Шавасана — 10 мин","Самомассаж — 10 мин"]},
    {"title":"Укрепление ног","exercises":["Приседания у стены — 10 раз","Шаги в сторону — 15 раз","Подъём на носки — 20 раз","Растяжка бёдер — 2 мин"]},
    {"title":"Руки и плечи","exercises":["Отжимания от стены — 10 раз","Разведение рук — 10 раз","Подъём рук вперёд — 10 раз","Растяжка плеч — 3 мин"]},
    {"title":"Итоговая тренировка","exercises":["Дыхательная разминка — 3 мин","Суставная гимнастика — 5 мин","Ходьба — 15 мин","Упражнения на кор — 5 мин","Растяжка тела — 5 мин","Релаксация — 5 мин"]},
]

# ──────────────────────────────────────────────────
#  ХРАНИЛИЩЕ
# ──────────────────────────────────────────────────
store = JsonStore('healthmate_data.json')

def get_setting(key, default=None):
    try:
        if store.exists('settings'):
            return store.get('settings').get(key, default)
    except Exception:
        pass
    return default

def set_setting(key, value):
    try:
        d = dict(store.get('settings')) if store.exists('settings') else {}
        d[key] = value
        store.put('settings', **d)
    except Exception:
        pass

def get_day_index():
    """Возвращает день от 0 до 29"""
    return (date.today().timetuple().tm_yday - 1) % 30

def get_lfk_day_for_user(is_guest):
    """
    МИН 11: для гостя — всегда день 1 (без сохранения).
    Для зарегистрированных — сохраняем прогресс.
    """
    if is_guest:
        return 0  # всегда день 1
    saved = get_setting('lfk_day_index', None)
    if saved is None:
        return get_day_index()
    return saved % 30

# ──────────────────────────────────────────────────
#  POPUP HELPER
# ──────────────────────────────────────────────────
def show_popup(title, text, btn_text='OK'):
    content = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(10))
    content.add_widget(Label(
        text=text, halign='center', valign='middle',
        color=get_color_from_hex('#FFFFFF'),
        font_size=dp(14), text_size=(dp(260), None)
    ))
    btn = Button(
        text=btn_text, size_hint_y=None, height=dp(44),
        background_normal='', background_color=get_color_from_hex('#6BCB77'),
        color=get_color_from_hex('#FFFFFF'), font_size=dp(15)
    )
    content.add_widget(btn)
    popup = Popup(
        title=title, content=content,
        size_hint=(0.85, None), height=dp(200),
        background_color=get_color_from_hex('#1E2E3E'),
        title_color=get_color_from_hex('#FFD93D'),
        separator_color=get_color_from_hex('#6BCB77')
    )
    btn.bind(on_release=popup.dismiss)
    popup.open()
    return popup

# ──────────────────────────────────────────────────
#  ЭКРАНЫ
# ──────────────────────────────────────────────────
class MainScreen(Screen):
    date_text = StringProperty('')
    def on_enter(self):
        self.update_date()
    def update_date(self):
        now = datetime.now()
        months = ['января','февраля','марта','апреля','мая','июня',
                  'июля','августа','сентября','октября','ноября','декабря']
        self.date_text = f"{now.day} {months[now.month-1]} {now.year}"


class LoginScreen(Screen):
    def show_register(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'register'

    def show_unavailable(self):
        show_popup(t('info'), 'Вход будет доступен в следующем обновлении')

    def guest_login(self):
        set_setting('is_guest', True)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'app_screen'


class RegisterScreen(Screen):
    email_error = StringProperty('')
    pass_error = StringProperty('')
    confirm_error = StringProperty('')

    def try_register(self, email, password, confirm):
        import re
        has_error = False
        email_pat = r'^[^\@\s]+@[^\@\s]+\.[^\@\s]+$'
        if not re.match(email_pat, email):
            self.email_error = t('email_error')
            has_error = True
        else:
            self.email_error = ''
        if len(password) < 6:
            self.pass_error = t('pass_error')
            has_error = True
        else:
            self.pass_error = ''
        if password != confirm and not has_error:
            self.confirm_error = t('confirm_error')
            has_error = True
        elif password == confirm:
            self.confirm_error = ''
        if not has_error:
            self.email_error = 'Эта почта не найдена в системе'

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


class AppScreen(Screen):
    date_text = StringProperty('')

    def on_enter(self):
        self.update_date()

    def update_date(self):
        now = datetime.now()
        months = ['января','февраля','марта','апреля','мая','июня',
                  'июля','августа','сентября','октября','ноября','декабря']
        self.date_text = f"{now.day} {months[now.month-1]} {now.year}"

    def open_diet_today(self):
        idx = get_day_index()
        day = DIET_PLAN[idx]
        content = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(14),
                        size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        rows = [
            (t('breakfast'), day["breakfast"]),
            (t('lunch'),     day["lunch"]),
            (t('snack'),     day["snack"]),
            (t('dinner'),    day["dinner"]),
        ]
        for lbl, val in rows:
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(74),
                             padding=[dp(12), dp(8)], spacing=dp(4))
            with item.canvas.before:
                Color(rgba=get_color_from_hex('#1B4D3E'))
                item._bg = RoundedRectangle(size=item.size, pos=item.pos, radius=[dp(10)])
            item.bind(size=lambda w,v: setattr(w._bg,'size',v))
            item.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            item.add_widget(Label(text=lbl, font_size=dp(12), bold=True,
                                  color=get_color_from_hex('#6BCB77'),
                                  halign='left', text_size=(dp(280), None),
                                  size_hint_y=None, height=dp(20)))
            item.add_widget(Label(text=val, font_size=dp(13),
                                  color=get_color_from_hex('#FFFFFF'),
                                  halign='left', text_size=(dp(280), None),
                                  size_hint_y=None, height=dp(38)))
            box.add_widget(item)
        content.add_widget(box)
        close_btn = Button(text=t('close'), size_hint_y=None, height=dp(44),
                           background_normal='',
                           background_color=get_color_from_hex('#6BCB77'))
        wrap = BoxLayout(orientation='vertical')
        wrap.add_widget(content)
        wrap.add_widget(close_btn)
        popup = Popup(title=f'{t("diet_day")} {idx+1}', content=wrap,
                      size_hint=(0.93, 0.82),
                      background_color=get_color_from_hex('#1A2535'),
                      title_color=get_color_from_hex('#FFD93D'),
                      separator_color=get_color_from_hex('#6BCB77'))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def open_lfk_today(self):
        # МИН 11: для гостя всегда день 1
        is_guest = get_setting('is_guest', True)
        idx = get_lfk_day_for_user(is_guest)
        day = LFK_PLAN[idx]
        content = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(14),
                        size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(Label(text=day['title'], font_size=dp(15), bold=True,
                             color=get_color_from_hex('#FFD93D'),
                             halign='left', text_size=(dp(280), None),
                             size_hint_y=None, height=dp(30)))
        for ex in day['exercises']:
            lbl = Label(text=f"  • {ex}", font_size=dp(13),
                        color=get_color_from_hex('#FFFFFF'),
                        halign='left', text_size=(dp(280), None),
                        size_hint_y=None, height=dp(32))
            box.add_widget(lbl)
        content.add_widget(box)
        close_btn = Button(text=t('close'), size_hint_y=None, height=dp(44),
                           background_normal='',
                           background_color=get_color_from_hex('#6BCB77'))
        wrap = BoxLayout(orientation='vertical')
        wrap.add_widget(content)
        wrap.add_widget(close_btn)
        popup = Popup(title=f'{t("lfk_day")} {idx+1}', content=wrap,
                      size_hint=(0.93, 0.75),
                      background_color=get_color_from_hex('#1A2535'),
                      title_color=get_color_from_hex('#FFD93D'),
                      separator_color=get_color_from_hex('#6BCB77'))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


class CalendarScreen(Screen):
    def on_enter(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()
        today_idx = get_day_index()
        for i in range(30):
            diet = DIET_PLAN[i]
            lfk  = LFK_PLAN[i]
            is_today = (i == today_idx)
            row = BoxLayout(orientation='horizontal', size_hint_y=None,
                            height=dp(54), spacing=dp(6), padding=[dp(10), dp(4)])
            bg = get_color_from_hex('#1B4D3E') if is_today else get_color_from_hex('#1E2E3E')
            with row.canvas.before:
                Color(rgba=bg)
                row._bg = RoundedRectangle(size=row.size, pos=row.pos, radius=[dp(8)])
            row.bind(size=lambda w,v: setattr(w._bg,'size',v))
            row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            prefix = ">> " if is_today else ""
            row.add_widget(Label(
                text=f"{prefix}{t('day')} {i+1}",
                font_size=dp(12), bold=is_today,
                color=get_color_from_hex('#FFD93D' if is_today else '#FFFFFF'),
                size_hint_x=0.22, halign='left', text_size=(dp(80), None)))
            row.add_widget(Label(
                text=diet['breakfast'][:26],
                font_size=dp(11), color=get_color_from_hex('#A8C5DA'),
                size_hint_x=0.45, halign='left', text_size=(dp(160), None)))
            row.add_widget(Label(
                text=lfk['title'][:18],
                font_size=dp(11), color=get_color_from_hex('#D8A8F0'),
                size_hint_x=0.33, halign='right', text_size=(dp(110), None)))
            grid.add_widget(row)


class ReminderScreen(Screen):

    TIME_BLOCKS = {
        'breakfast': {
            'time': '08:00',
            'title': 'Завтрак',
            'food_key': 'breakfast',
            'exercises': [
                'Выпейте стакан воды сразу после пробуждения',
                'Легкая растяжка — 5 мин',
                'Дыхательная гимнастика — 3 мин',
            ]
        },
        'morning_ex': {
            'time': '10:00',
            'title': 'Утренние упражнения',
            'food_key': None,
            'exercises': None,
        },
        'lunch': {
            'time': '12:00',
            'title': 'Обед',
            'food_key': 'lunch',
            'exercises': [
                'После обеда: спокойная прогулка 10-15 мин',
                'Не ложитесь сразу — посидите спокойно',
                'Выпейте воду через 30 минут после еды',
            ]
        },
        'walk': {
            'time': '14:00',
            'title': 'Прогулка',
            'food_key': None,
            'exercises': [
                'Спокойная ходьба на свежем воздухе — 20-30 мин',
                'Дыхание через нос, ритмичный шаг',
                'Избегайте резкого темпа и подъёмов',
                'Лёгкая разминка суставов перед выходом',
            ]
        },
        'snack': {
            'time': '16:00',
            'title': 'Полдник',
            'food_key': 'snack',
            'exercises': [
                'Лёгкие упражнения сидя — 5 мин',
                'Гимнастика для рук и плеч — 3 мин',
                'Дыхательные упражнения — 2 мин',
            ]
        },
        'dinner': {
            'time': '18:00',
            'title': 'Ужин',
            'food_key': 'dinner',
            'exercises': [
                'Лёгкая растяжка после ужина — 5 мин',
                'Небольшая прогулка по квартире',
                'Стакан воды или травяного чая',
            ]
        },
        'evening_ex': {
            'time': '20:00',
            'title': 'Вечерняя гимнастика',
            'food_key': None,
            'exercises': [
                'Поза ребёнка — 2 мин',
                'Растяжка спины лёжа — 3 мин',
                'Медленное дыхание животом — 5 мин',
                'Мышечная релаксация — 5 мин',
                'Подготовка ко сну — отложите телефон',
            ]
        },
        'sleep': {
            'time': '22:00',
            'title': 'Время сна',
            'food_key': None,
            'exercises': [
                'Уберите телефон и выключите яркий свет',
                'Проветрите комнату 10 мин',
                'Лягте удобно, расслабьте тело',
                'Дышите медленно: вдох 4с — выдох 6с',
                'Старайтесь спать не менее 8 часов',
            ]
        },
    }

    def show_time_detail(self, block_key):
        block = self.TIME_BLOCKS.get(block_key)
        if not block:
            return
        idx = get_day_index()
        diet_day = DIET_PLAN[idx]
        lfk_day  = LFK_PLAN[idx]

        content = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16),
                        size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        # Заголовок — МИН 4: убраны эмодзи
        box.add_widget(Label(
            text=f"{block['time']} — {block['title']}",
            font_size=dp(18), bold=True,
            color=get_color_from_hex('#FFD93D'),
            halign='left', text_size=(dp(310), None),
            size_hint_y=None, height=dp(34)
        ))

        food_key = block.get('food_key')
        if food_key and food_key in diet_day:
            food_card = BoxLayout(orientation='vertical', size_hint_y=None,
                                  height=dp(72), padding=[dp(14), dp(10)], spacing=dp(4))
            with food_card.canvas.before:
                Color(rgba=get_color_from_hex('#1B4D3E'))
                food_card._bg = RoundedRectangle(size=food_card.size, pos=food_card.pos, radius=[dp(12)])
            food_card.bind(size=lambda w,v: setattr(w._bg,'size',v))
            food_card.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            food_card.add_widget(Label(
                text='Меню на сегодня:', font_size=dp(12), bold=True,
                color=get_color_from_hex('#6BCB77'),
                halign='left', text_size=(dp(290), None),
                size_hint_y=None, height=dp(22)
            ))
            food_card.add_widget(Label(
                text=diet_day[food_key], font_size=dp(14),
                color=get_color_from_hex('#FFFFFF'),
                halign='left', text_size=(dp(290), None),
                size_hint_y=None, height=dp(30)
            ))
            box.add_widget(food_card)

        exercises = block.get('exercises')
        if exercises is None:
            lfk_title_lbl = Label(
                text=lfk_day['title'],
                font_size=dp(14), bold=True,
                color=get_color_from_hex('#D8A8F0'),
                halign='left', text_size=(dp(310), None),
                size_hint_y=None, height=dp(28)
            )
            box.add_widget(lfk_title_lbl)
            exercises = [f"• {ex}" for ex in lfk_day['exercises']]

        if exercises:
            header = Label(
                text='Упражнения:', font_size=dp(12), bold=True,
                color=get_color_from_hex('#A8C5DA'),
                halign='left', text_size=(dp(310), None),
                size_hint_y=None, height=dp(24)
            )
            box.add_widget(header)
            for ex in exercises:
                ex_card = BoxLayout(size_hint_y=None, height=dp(42),
                                    padding=[dp(14), dp(8)])
                with ex_card.canvas.before:
                    Color(rgba=get_color_from_hex('#1E3A5F'))
                    ex_card._bg = RoundedRectangle(size=ex_card.size, pos=ex_card.pos, radius=[dp(10)])
                ex_card.bind(size=lambda w,v: setattr(w._bg,'size',v))
                ex_card.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
                ex_card.add_widget(Label(
                    text=ex, font_size=dp(13),
                    color=get_color_from_hex('#FFFFFF'),
                    halign='left', text_size=(dp(290), None),
                    size_hint_y=None, height=dp(26)
                ))
                box.add_widget(ex_card)

        box.add_widget(Label(
            text=f'День программы: {idx + 1} из 30',
            font_size=dp(11), color=get_color_from_hex('#3A4A5A'),
            halign='center', size_hint_y=None, height=dp(28)
        ))

        content.add_widget(box)

        close_btn = Button(
            text='Закрыть', size_hint_y=None, height=dp(48),
            background_normal='',
            background_color=get_color_from_hex('#6BCB77'),
            color=get_color_from_hex('#FFFFFF'),
            font_size=dp(15), bold=True
        )
        wrap = BoxLayout(orientation='vertical')
        wrap.add_widget(content)
        wrap.add_widget(close_btn)

        popup = Popup(
            title=f"{block['time']} — {block['title']}",
            content=wrap,
            size_hint=(0.95, 0.82),
            background_color=get_color_from_hex('#1A2535'),
            title_color=get_color_from_hex('#FFD93D'),
            separator_color=get_color_from_hex('#6BCB77')
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


# ──────────────────────────────────────────────────
#  ЧАТ ЭКРАНЫ
# ──────────────────────────────────────────────────
class ChatHubScreen(Screen):
    pass


class CommunityScreen(Screen):
    def on_enter(self):
        pass

    def send_message(self, text_input):
        text = text_input.text.strip()
        if not text:
            return
        box = self.ids.chat_box
        msg_row = BoxLayout(orientation='vertical', size_hint_y=None,
                            height=dp(60), padding=[dp(10), dp(6)], spacing=dp(2))
        with msg_row.canvas.before:
            Color(rgba=get_color_from_hex('#1E3A5F'))
            msg_row._bg = RoundedRectangle(size=msg_row.size, pos=msg_row.pos,
                                           radius=[dp(10), dp(10), dp(2), dp(10)])
        msg_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        msg_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        msg_row.add_widget(Label(text=t('you'), font_size=dp(11),
                                 color=get_color_from_hex('#6BCB77'),
                                 halign='left', text_size=(dp(300), None),
                                 size_hint_y=None, height=dp(18)))
        msg_row.add_widget(Label(text=text, font_size=dp(13),
                                 color=get_color_from_hex('#FFFFFF'),
                                 halign='left', text_size=(dp(300), None),
                                 size_hint_y=None, height=dp(26)))
        box.add_widget(msg_row)
        text_input.text = ''
        Clock.schedule_once(lambda dt: setattr(self.ids.chat_scroll, 'scroll_y', 0), 0.1)


class AIChatScreen(Screen):
    def on_enter(self):
        pass

    def send_message(self, text_input):
        text = text_input.text.strip()
        if not text:
            return
        box = self.ids.ai_chat_box
        user_row = BoxLayout(orientation='vertical', size_hint_y=None,
                             height=dp(60), padding=[dp(10), dp(6)], spacing=dp(2))
        with user_row.canvas.before:
            Color(rgba=get_color_from_hex('#1E3A5F'))
            user_row._bg = RoundedRectangle(size=user_row.size, pos=user_row.pos,
                                            radius=[dp(10), dp(10), dp(2), dp(10)])
        user_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        user_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        user_row.add_widget(Label(text=t('you'), font_size=dp(11),
                                  color=get_color_from_hex('#6BCB77'),
                                  halign='left', text_size=(dp(300), None),
                                  size_hint_y=None, height=dp(18)))
        user_row.add_widget(Label(text=text, font_size=dp(13),
                                  color=get_color_from_hex('#FFFFFF'),
                                  halign='left', text_size=(dp(300), None),
                                  size_hint_y=None, height=dp(26)))
        box.add_widget(user_row)
        text_input.text = ''
        Clock.schedule_once(lambda dt: setattr(self.ids.ai_scroll, 'scroll_y', 0), 0.1)
        Clock.schedule_once(lambda dt: self._auto_reply(box, text), 1.0)

    def _auto_reply(self, box, user_text):
        replies = [
            "Я рекомендую проконсультироваться с вашим врачом по этому вопросу.",
            "Это отличный вопрос! Старайтесь пить 8 стаканов воды в день.",
            "Следите за режимом питания по вашей программе диеты.",
            "Регулярные упражнения ЛФК помогут улучшить самочувствие.",
            "Помните: здоровый сон не менее 8 часов — важная часть выздоровления.",
        ]
        import random
        reply = random.choice(replies)
        ai_row = BoxLayout(orientation='vertical', size_hint_y=None,
                           height=dp(70), padding=[dp(10), dp(6)], spacing=dp(2))
        with ai_row.canvas.before:
            Color(rgba=get_color_from_hex('#1B4D3E'))
            ai_row._bg = RoundedRectangle(size=ai_row.size, pos=ai_row.pos,
                                          radius=[dp(2), dp(10), dp(10), dp(10)])
        ai_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        ai_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        ai_row.add_widget(Label(text='HealthMate AI', font_size=dp(11),
                                color=get_color_from_hex('#FFD93D'),
                                halign='left', text_size=(dp(300), None),
                                size_hint_y=None, height=dp(18)))
        ai_row.add_widget(Label(text=reply, font_size=dp(12),
                                color=get_color_from_hex('#FFFFFF'),
                                halign='left', text_size=(dp(290), None),
                                size_hint_y=None, height=dp(36)))
        box.add_widget(ai_row)
        Clock.schedule_once(lambda dt: setattr(self.ids.ai_scroll, 'scroll_y', 0), 0.1)


class SupportScreen(Screen):
    def send_message(self, text_input):
        text = text_input.text.strip()
        if not text:
            return
        box = self.ids.support_chat_box
        user_row = BoxLayout(orientation='vertical', size_hint_y=None,
                             height=dp(60), padding=[dp(10), dp(6)], spacing=dp(2))
        with user_row.canvas.before:
            Color(rgba=get_color_from_hex('#1E3A5F'))
            user_row._bg = RoundedRectangle(size=user_row.size, pos=user_row.pos,
                                            radius=[dp(10), dp(10), dp(2), dp(10)])
        user_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        user_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        user_row.add_widget(Label(text=t('you'), font_size=dp(11),
                                  color=get_color_from_hex('#6BCB77'),
                                  halign='left', text_size=(dp(300), None),
                                  size_hint_y=None, height=dp(18)))
        user_row.add_widget(Label(text=text, font_size=dp(13),
                                  color=get_color_from_hex('#FFFFFF'),
                                  halign='left', text_size=(dp(300), None),
                                  size_hint_y=None, height=dp(26)))
        box.add_widget(user_row)
        text_input.text = ''
        Clock.schedule_once(lambda dt: setattr(self.ids.support_scroll, 'scroll_y', 0), 0.1)
        Clock.schedule_once(lambda dt: self._auto_reply(box), 1.5)

    def _auto_reply(self, box):
        reply = "Спасибо за обращение! Мы постараемся ответить в ближайшее время. Среднее время ответа — 24 часа."
        sup_row = BoxLayout(orientation='vertical', size_hint_y=None,
                            height=dp(70), padding=[dp(10), dp(6)], spacing=dp(2))
        with sup_row.canvas.before:
            Color(rgba=get_color_from_hex('#3D1F5C'))
            sup_row._bg = RoundedRectangle(size=sup_row.size, pos=sup_row.pos,
                                           radius=[dp(2), dp(10), dp(10), dp(10)])
        sup_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        sup_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        sup_row.add_widget(Label(text='Поддержка', font_size=dp(11),
                                 color=get_color_from_hex('#D8A8F0'),
                                 halign='left', text_size=(dp(300), None),
                                 size_hint_y=None, height=dp(18)))
        sup_row.add_widget(Label(text=reply, font_size=dp(12),
                                 color=get_color_from_hex('#FFFFFF'),
                                 halign='left', text_size=(dp(290), None),
                                 size_hint_y=None, height=dp(36)))
        box.add_widget(sup_row)
        Clock.schedule_once(lambda dt: setattr(self.ids.support_scroll, 'scroll_y', 0), 0.1)


# ──────────────────────────────────────────────────
#  ПОГОДА
# ──────────────────────────────────────────────────
class WeatherScreen(Screen):
    loading    = BooleanProperty(False)
    error_text = StringProperty('')
    selected_city = StringProperty('Алматы')

    WEATHER_CODES = {
        0:'Ясно', 1:'Преим. ясно', 2:'Переменная облачность',
        3:'Пасмурно', 45:'Туман', 48:'Иней',
        51:'Легкая морось', 61:'Дождь', 63:'Умеренный дождь',
        65:'Сильный дождь', 71:'Снег', 80:'Ливень', 95:'Гроза',
    }

    def on_enter(self):
        self._build_city_bar()
        if not self.ids.weather_cards.children:
            self.select_city('Алматы')

    def _build_city_bar(self):
        try:
            bar = self.ids.city_bar
            bar.clear_widgets()
            bar.width = dp(10)
            for city in KZ_CITIES:
                is_sel = (city == self.selected_city)
                btn = Button(
                    text=city,
                    size_hint=(None, None),
                    size=(dp(max(80, len(city) * 10 + 20)), dp(36)),
                    background_normal='',
                    background_color=get_color_from_hex('#6BCB77') if is_sel else get_color_from_hex('#1E2E3E'),
                    color=get_color_from_hex('#FFFFFF'),
                    font_size=dp(13),
                    bold=is_sel
                )
                btn.city_name = city
                btn.bind(on_release=lambda b: self.select_city(b.city_name))
                with btn.canvas.before:
                    Color(rgba=get_color_from_hex('#6BCB77') if is_sel else get_color_from_hex('#1E2E3E'))
                    btn._bg = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[dp(18)])
                btn.bind(size=lambda w,v: setattr(w._bg,'size',v))
                btn.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
                bar.add_widget(btn)
                bar.width += btn.width + dp(8)
        except Exception:
            pass

    def select_city(self, city):
        self.selected_city = city
        self._build_city_bar()
        self.fetch_weather(city)

    def fetch_weather(self, city):
        if not city:
            city = 'Алматы'
        self.loading = True
        self.error_text = ''
        self.ids.weather_cards.clear_widgets()
        threading.Thread(target=self._fetch_thread, args=(city.strip(),), daemon=True).start()

    def _fetch_thread(self, city_name):
        try:
            geo_url = (f"https://geocoding-api.open-meteo.com/v1/search"
                       f"?name={urllib.parse.quote(city_name)}&count=1&language=ru&format=json")
            with urllib.request.urlopen(geo_url, timeout=10) as r:
                geo = json.loads(r.read())
            results = geo.get('results', [])
            if not results:
                Clock.schedule_once(lambda dt: setattr(self, 'error_text', t('city_not_found')))
                Clock.schedule_once(lambda dt: setattr(self, 'loading', False))
                return
            lat  = results[0]['latitude']
            lon  = results[0]['longitude']
            name = results[0].get('name', city_name)
            wx_url = (f"https://api.open-meteo.com/v1/forecast"
                      f"?latitude={lat}&longitude={lon}"
                      f"&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum"
                      f"&timezone=auto&forecast_days=3")
            with urllib.request.urlopen(wx_url, timeout=10) as r:
                wx = json.loads(r.read())
            daily = wx['daily']
            data = []
            day_labels = [t('today'), t('tomorrow'), 'Послезавтра']
            for i in range(min(3, len(daily['time']))):
                data.append({
                    'day':    day_labels[i],
                    'date':   daily['time'][i],
                    'desc':   self.WEATHER_CODES.get(daily['weathercode'][i], 'Данные получены'),
                    'tmax':   f"{daily['temperature_2m_max'][i]:.0f}",
                    'tmin':   f"{daily['temperature_2m_min'][i]:.0f}",
                    'precip': f"{daily['precipitation_sum'][i]:.1f}",
                    'city':   name,
                })
            Clock.schedule_once(lambda dt: self._build_cards(data))
        except Exception as e:
            msg = f'{t("conn_error")}\n{str(e)[:50]}'
            Clock.schedule_once(lambda dt: setattr(self, 'error_text', msg))
            Clock.schedule_once(lambda dt: setattr(self, 'loading', False))

    def _build_cards(self, data):
        self.loading = False
        box = self.ids.weather_cards
        box.clear_widgets()
        colors = ['#1E3A5F', '#1B4D3E', '#3D1F5C']
        for i, d in enumerate(data):
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140),
                             padding=[dp(16), dp(12)], spacing=dp(6))
            with card.canvas.before:
                Color(rgba=get_color_from_hex(colors[i % len(colors)]))
                card._bg = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(14)])
            card.bind(size=lambda w,v: setattr(w._bg,'size',v))
            card.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            card.add_widget(Label(
                text=f"{d['day']}  {d['date']}  •  {d['city']}",
                font_size=dp(13), bold=True, color=get_color_from_hex('#FFD93D'),
                halign='left', text_size=(dp(340), None), size_hint_y=None, height=dp(24)))
            card.add_widget(Label(
                text=d['desc'], font_size=dp(17), bold=True,
                color=get_color_from_hex('#FFFFFF'),
                halign='left', text_size=(dp(340), None), size_hint_y=None, height=dp(32)))
            card.add_widget(Label(
                text=f"{t('max')}: {d['tmax']}C  •  {t('min')}: {d['tmin']}C",
                font_size=dp(14), color=get_color_from_hex('#FFFFFF'),
                halign='left', text_size=(dp(340), None), size_hint_y=None, height=dp(24)))
            card.add_widget(Label(
                text=f"{t('precip')}: {d['precip']} {t('mm')}",
                font_size=dp(12), color=get_color_from_hex('#A8C5DA'),
                halign='left', text_size=(dp(340), None), size_hint_y=None, height=dp(22)))
            box.add_widget(card)


# ──────────────────────────────────────────────────
#  НАСТРОЙКИ
# ──────────────────────────────────────────────────
class SettingsScreen(Screen):
    dark_mode      = BooleanProperty(False)
    notif_screen   = BooleanProperty(True)
    notif_enabled  = BooleanProperty(True)
    pin_enabled    = BooleanProperty(False)
    is_guest       = BooleanProperty(True)
    current_lang_label = StringProperty('RU')

    def on_enter(self):
        self.dark_mode     = get_setting('dark_mode',     False)
        self.notif_screen  = get_setting('notif_screen',  True)
        self.notif_enabled = get_setting('notif_enabled', True)
        self.pin_enabled   = get_setting('pin_enabled',   False)
        self.is_guest      = get_setting('is_guest',      True)
        self.current_lang_label = current_lang[0]

    def toggle_dark(self, value):
        self.dark_mode = value
        set_setting('dark_mode', value)

    def toggle_notif_screen(self, value):
        self.notif_screen = value
        set_setting('notif_screen', value)

    def toggle_notif(self, value):
        self.notif_enabled = value
        set_setting('notif_enabled', value)

    def open_language_picker(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        content.add_widget(Label(
            text='Выберите язык / Select language / Тілді таңдаңыз',
            font_size=dp(13), color=get_color_from_hex('#A8C5DA'),
            halign='center', size_hint_y=None, height=dp(40),
            text_size=(dp(280), None)
        ))
        popup_ref = [None]

        def make_lang_btn(lang_code, lang_label, is_current):
            bg = get_color_from_hex('#1B4D3E') if is_current else get_color_from_hex('#1E2E3E')
            btn = Button(
                text=lang_label,
                size_hint_y=None, height=dp(52),
                background_normal='',
                background_color=bg,
                color=get_color_from_hex('#FFD93D' if is_current else '#FFFFFF'),
                font_size=dp(15), bold=is_current
            )
            def select_lang(instance, lc=lang_code):
                current_lang[0] = lc
                set_setting('language', lc)
                self.current_lang_label = lc
                if popup_ref[0]:
                    popup_ref[0].dismiss()
                self.on_enter()
            btn.bind(on_release=select_lang)
            return btn

        cur = current_lang[0]
        for code, label in [('RU', 'RU — Русский'), ('EN', 'EN — English'), ('KZ', 'KZ — Казакша')]:
            content.add_widget(make_lang_btn(code, label, code == cur))

        cancel_btn = Button(
            text='Закрыть / Close / Жабу',
            size_hint_y=None, height=dp(44),
            background_normal='',
            background_color=get_color_from_hex('#333'),
            color=get_color_from_hex('#FFFFFF'),
            font_size=dp(13)
        )
        content.add_widget(cancel_btn)

        popup = Popup(
            title='Язык / Language / Тіл',
            content=content,
            size_hint=(0.88, None), height=dp(320),
            background_color=get_color_from_hex('#1A2535'),
            title_color=get_color_from_hex('#FFD93D'),
            separator_color=get_color_from_hex('#6BCB77')
        )
        popup_ref[0] = popup
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()

    def set_pin(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(14))
        inp = TextInput(hint_text=t('enter_pin'), input_filter='int',
                        multiline=False, password=True,
                        background_color=get_color_from_hex('#1E2E3E'),
                        foreground_color=get_color_from_hex('#FFFFFF'),
                        hint_text_color=get_color_from_hex('#A8C5DA'),
                        font_size=dp(16), size_hint_y=None, height=dp(44))
        content.add_widget(inp)
        row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
        popup = Popup(title=t('pin_title'), content=content,
                      size_hint=(0.85, None), height=dp(180),
                      background_color=get_color_from_hex('#1A2535'),
                      title_color=get_color_from_hex('#FFD93D'))
        ok = Button(text=t('save'), background_normal='',
                    background_color=get_color_from_hex('#6BCB77'))
        cancel = Button(text=t('cancel'), background_normal='',
                        background_color=get_color_from_hex('#555'))
        def save(*a):
            if len(inp.text) == 4:
                set_setting('pin_code', inp.text)
                set_setting('pin_enabled', True)
                self.pin_enabled = True
                popup.dismiss()
            else:
                inp.hint_text = t('need_4')
        ok.bind(on_release=save)
        cancel.bind(on_release=popup.dismiss)
        row.add_widget(cancel)
        row.add_widget(ok)
        content.add_widget(row)
        popup.open()

    def invite_friends(self):
        show_popup(t('invitation'), t('invite_msg'))

    def delete_profile(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(14))
        content.add_widget(Label(text=t('delete_confirm'),
                                 halign='center', color=get_color_from_hex('#FFFFFF'),
                                 font_size=dp(14)))
        row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
        popup = Popup(title=t('delete_title'), content=content,
                      size_hint=(0.85, None), height=dp(180),
                      background_color=get_color_from_hex('#1A2535'),
                      title_color=get_color_from_hex('#FFD93D'))
        yes = Button(text=t('delete'), background_normal='',
                     background_color=get_color_from_hex('#E74C3C'))
        no  = Button(text=t('cancel'), background_normal='',
                     background_color=get_color_from_hex('#555'))
        def confirm(*a):
            try:
                store.delete('settings')
            except Exception:
                pass
            popup.dismiss()
            self.manager.current = 'main'
        yes.bind(on_release=confirm)
        no.bind(on_release=popup.dismiss)
        row.add_widget(no)
        row.add_widget(yes)
        content.add_widget(row)
        popup.open()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'app_screen'


# ──────────────────────────────────────────────────
#  APP
# ──────────────────────────────────────────────────
class HealthMateApp(App):
    def build(self):
        self.title = 'HealthMate 2.2'
        saved_lang = get_setting('language', 'RU')
        if saved_lang in TRANSLATIONS:
            current_lang[0] = saved_lang

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(AppScreen(name='app_screen'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(ReminderScreen(name='reminder'))
        sm.add_widget(ChatHubScreen(name='chat_hub'))
        sm.add_widget(CommunityScreen(name='community'))
        sm.add_widget(AIChatScreen(name='ai_chat'))
        sm.add_widget(SupportScreen(name='support'))
        sm.add_widget(WeatherScreen(name='weather'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    HealthMateApp().run()
