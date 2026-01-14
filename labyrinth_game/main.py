#!/usr/bin/env python3
from labyrinth_game.player_actions import choose_action

def main():
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }
    print("Добро пожаловать в Лабиринт сокровищ!")

    while not game_state['game_over']:
        choose_action(game_state)

if __name__ == "__main__":
    main()
