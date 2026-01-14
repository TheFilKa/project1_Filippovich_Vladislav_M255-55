from labyrinth_game.constants import ROOMS, COMMANDS
from labyrinth_game.utils import pseudo_random, trigger_trap, random_event

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    inv = game_state['player_inventory']
    if inv:
        print("Инвентарь:", ', '.join(inv))
    else:
        print("Инвентарь пуст.")

def take_item(game_state, item_name):
    room = ROOMS[game_state['current_room']]
    if item_name in room['items']:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    if item_name == 'torch':
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы держите меч. Чувствуете себя уверенно.")
    elif item_name == 'bronze_box':
        print("Вы открыли бронзовую шкатулку.")
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            print("Вы получили rusty_key!")
    else:
        print("Вы не знаете, как использовать этот предмет.")

def move_player(game_state, direction):
    room = ROOMS[game_state['current_room']]
    if direction in room['exits']:
        next_room = room['exits'][direction]
        if next_room == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def solve_puzzle(game_state):
    room = ROOMS[game_state['current_room']]
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return
    question, answer = room['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ").strip().lower()
    if user_answer in (answer, answer.lower()):
        print("Правильно! Загадка решена.")
        room['puzzle'] = None
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            print("Вы получили rusty_key!")
    else:
        print("Неверно. Попробуйте снова.")
        if game_state['current_room'] == 'trap_room':
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    room = ROOMS[game_state['current_room']]
    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт.")
        return
    if 'rusty_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        ans = get_input("Сундук заперт. Ввести код? (да/нет) ").lower()
        if ans == 'да':
            code = get_input("Введите код: ").strip()
            if room['puzzle'] and code == room['puzzle'][1]:
                print("Код верный! Сундук открыт. Вы победили!")
                room['items'].remove('treasure_chest')
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")

# ======= Меню с цифрами =======
def choose_action(game_state):
    room = ROOMS[game_state['current_room']]
    actions = []

    # Предметы
    for item in room['items']:
        if item != 'treasure_chest':
            actions.append(("take", item))

    # Загадка
    if room['puzzle']:
        actions.append(("solve", None))

    # Сундук
    if game_state['current_room'] == 'treasure_room' and 'treasure_chest' in room['items']:
        actions.append(("treasure", None))

    # Направления
    for direction in room['exits']:
        actions.append(("go", direction))

    # Общие
    actions.extend([
        ("inventory", None),
        ("use", None),
        ("help", None),
        ("quit", None)
    ])

    # Печать меню
    print(f"\n== {game_state['current_room'].upper()} ==")
    print(room['description'])
    if room['items']:
        print("Заметные предметы:", ', '.join(room['items']))
    print("Выходы:", ', '.join(room['exits'].keys()))
    print("\nВыберите действие (введите цифру):")
    for idx, (cmd, arg) in enumerate(actions, start=1):
        if cmd == "take":
            text = f"Взять предмет '{arg}'"
        elif cmd == "go":
            text = f"Перейти {arg}"
        elif cmd == "solve":
            text = "Попробовать решить загадку"
        elif cmd == "treasure":
            text = "Попытаться открыть сундук"
        elif cmd == "inventory":
            text = "Проверить инвентарь"
        elif cmd == "use":
            text = "Использовать предмет"
        elif cmd == "help":
            text = "Показать команды"
        elif cmd == "quit":
            text = "Выйти из игры"
        print(f"  {idx}. {text}")

    # Выбор действия
    while True:
        choice = get_input("> ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(actions)):
            print("Введите корректную цифру из списка.")
            continue
        idx = int(choice) - 1
        cmd, arg = actions[idx]
        if cmd == "take":
            take_item(game_state, arg)
        elif cmd == "go":
            move_player(game_state, arg)
        elif cmd == "solve":
            solve_puzzle(game_state)
        elif cmd == "treasure":
            attempt_open_treasure(game_state)
        elif cmd == "inventory":
            show_inventory(game_state)
        elif cmd == "use":
            item_name = get_input("Введите название предмета для использования: ").strip()
            use_item(game_state, item_name)
        elif cmd == "help":
            show_help()
        elif cmd == "quit":
            game_state['game_over'] = True
        break
