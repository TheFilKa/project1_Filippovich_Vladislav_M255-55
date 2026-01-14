import math
from labyrinth_game.constants import ROOMS

def pseudo_random(seed: int, modulo: int) -> int:
    x = math.sin(seed * 12.9898) * 43758.5453
    return int((x - math.floor(x)) * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inv = game_state['player_inventory']
    if inv:
        idx = pseudo_random(game_state['steps_taken'], len(inv))
        lost_item = inv.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        dmg = pseudo_random(game_state['steps_taken'], 10)
        if dmg < 3:
            print("Ловушка смертельна! Вы проиграли.")
            game_state['game_over'] = True
        else:
            print("Вы уцелели, но были напуганы!")

def random_event(game_state):
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return
    event = pseudo_random(game_state['steps_taken'] + 1, 3)
    room = ROOMS[game_state['current_room']]
    if event == 0:
        print("Вы находите монетку на полу!")
        room['items'].append('coin')
    elif event == 1:
        print("Вы слышите странный шорох...")
        if 'sword' in game_state['player_inventory']:
            print("Ваш меч отпугнул существо.")
    elif event == 2:
        if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
            print("Опасность! Ловушка рядом!")
            trigger_trap(game_state)
