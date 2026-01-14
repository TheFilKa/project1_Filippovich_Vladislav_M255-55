# labyrinth_game/constants.py
# Константы: карта комнат и команды игры

ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит старый факел.',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число после девяти".', '10')
    },
    'trap_room': {
        'description': 'Комната с хитрой плиточной поломкой. На стене надпись: "Осторожно — ловушка".',
        'exits': {'west': 'entrance'},
        'items': ['rusty_key'],
        'puzzle': ('Система плит активна. Введите "шаг" три раза подряд.', 'шаг шаг шаг')
    },
    'library': {
        'description': 'Пыльная библиотека. На полках старые свитки.',
        'exits': {'east': 'hall', 'north': 'armory'},
        'items': ['ancient_book'],
        'puzzle': ('Что растет, когда его съедают? (одно слово)', 'резонанс')
    },
    'armory': {
        'description': 'Старая оружейная комната. На стене висит меч, рядом — бронзовая шкатулка.',
        'exits': {'south': 'library'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None
    },
    'treasure_room': {
        'description': 'Комната, на столе большой сундук. Дверь заперта — нужен ключ.',
        'exits': {'south': 'hall'},
        'items': ['treasure_chest'],
        'puzzle': ('Введите код (подсказка: 2*5=?)', '10')
    }
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}
