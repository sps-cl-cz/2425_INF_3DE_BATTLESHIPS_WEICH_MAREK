"""
strategy.py

This module contains the Strategy class responsible for:
 - Tracking the known state of the enemy board.
 - Deciding which (x, y) cell to attack next.
 - Registering the result of each attack (hit/miss, sunk).
 - Keeping track of remaining enemy ships in a ships_dict.
"""

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        """
        Initializes the Strategy.

        :param rows: Number of rows in the enemy board.
        :param cols: Number of columns in the enemy board.
        :param ships_dict: Dictionary mapping ship_id -> count for enemy ships.
                           e.g. {1: 2, 2: 1, 3: 1, ...}

        The enemy board is initially unknown.
        """
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        
        # Tady vytvoříme 2D seznam otazníků '?', znamenající "neznámé pole"
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]

        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.hit_stack = []

    def get_next_attack(self) -> tuple[int, int]:
        """
        Returns the next (x, y) coordinates to attack.
        x = column, y = row.
        Must be within [0 .. cols-1], [0 .. rows-1].
        Assume we will never call this function if all ships are sunk.
        """
        
        if self.hit_stack: 
            x, y = self.hit_stack.pop()
            if self.enemy_board[y][x] == '?':
                return x, y
            
        for y in range(self.rows):
            for x in range(self.cols):
                if self.enemy_board[y][x] == '?' and (x + y) % 2 == 0:
                    return x, y
            
        for y in range(self.rows):
            for x in range(self.cols):
                if self.enemy_board[y][x] == '?':
                    return x, y

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        """
        Called by the main simulation AFTER each shot, informing of the result:
          - is_hit: True if it's a hit
          - is_sunk: True if this shot sank a ship

        If is_sunk == True, we should decrement the count of one ship in ships_dict (you need to find out which ID).
        You should update the enemy board appropriately too.
        """
        # Tady zaznamenáme výsledek útoku (hit or miss, I guess they never miss, huh), případně potopení

        if is_hit:
            self.enemy_board[y][x] = 'H'
            if is_sunk:
                self.enemy_board[y][x] = 'S'
                self._update_ships_dict()
                self._mark_surrounding_impossible(x, y)
            else:
                self._add_adjacent_targets(x, y)
        else:
            self.enemy_board[y][x] = 'M'
    
    def _add_adjacent_targets(self, x: int, y: int) -> None:
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.enemy_board[ny][nx] == '?':
                self.hit_stack.append((nx, ny))

    def _mark_surrounding_impossible(self, x: int, y: int) -> None:
        ship_tiles = set()
        to_check = [(x, y)]

        while to_check:
            x, y = to_check.pop()
            if (x, y) in ship_tiles:
                continue
            if self.enemy_board[y][x] in {'H', 'S'}:
                ship_tiles.add((x, y))
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in ship_tiles:
                        to_check.append((nx, ny))

        for sx, sy in ship_tiles:
            for dx, dy in self.directions:
                nx, ny = sx + dx, sy + dy
                while 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in ship_tiles:
                    self.enemy_board[ny][nx] = 'X'
                    nx, ny = nx + dx, ny
                    break

    def _update_ships_dict(self) -> None:
        for ship_id in sorted(self.ships_dict.keys()):
            if self.ships_dict[ship_id] > 0:
                self.ships_dict[ship_id] -= 1
                break

    def get_enemy_board(self) -> list[list[str]]:
        """
        Returns the current 2D state (knowledge) of the enemy board.
        '?' = unknown, 'H' = hit, 'M' = miss.
        You may optionally use 'S' for sunk ships (not required).
        You may optionally use 'X' for tiles that are impossible to contain a ship (not required).
        """

        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        """
        Returns the dictionary of ship_id -> count for ships we believe remain afloat.
        """
        return self.ships_dict

    def all_ships_sunk(self) -> bool:
        """
        Returns True if all enemy ships are sunk (ships_dict counts are all zero).
        """
        return all(count == 0 for count in self.ships_dict.values())
