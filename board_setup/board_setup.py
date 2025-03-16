import random
 
class BoardSetup:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
 
        self.ship_shapes = {
            1: [(0, 0), (1, 0)],  
            2: [(0, 0), (1, 0), (2, 0)],  
            3: [(0, 0), (1, 0), (2, 0), (3, 0)],  
            4: [(0, 0), (1, 0), (2, 0), (1, 1)],  
            5: [(0, 0), (1, 0), (2, 0), (2, 1)],  
            6: [(0, 1), (1, 1), (1, 0), (2, 0)],  
            7: [(1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1)] 
        }
 
    def get_board(self) -> list[list[int]]:
        return self.board
 
    def get_tile(self, x: int, y: int) -> int:
        if y < 0 or y >= self.rows or x < 0 or x >= self.cols:
            raise IndexError("Coordinates out of bounds")
        return self.board[y][x]
 
    def is_adjacent_to_ship(self, shape, start_x, start_y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in shape:
            x, y = start_x + dx, start_y + dy
            for dir_x, dir_y in directions:
                adj_x, adj_y = x + dir_x, y + dir_y
                if 0 <= adj_x < self.cols and 0 <= adj_y < self.rows:
                    if self.board[adj_y][adj_x] != 0:
                        return True
        return False
 
    def can_place_ship(self, shape, start_x, start_y):
        for dx, dy in shape:
            x, y = start_x + dx, start_y + dy
            if x < 0 or x >= self.cols or y < 0 or y >= self.rows or self.board[y][x] != 0:
                return False
        return not self.is_adjacent_to_ship(shape, start_x, start_y)
 
    def place_ship(self, ship_id, shape, start_x, start_y):
        for dx, dy in shape:
            x, y = start_x + dx, start_y + dy
            self.board[y][x] = ship_id
 
    def place_ships(self) -> None:
        for ship_id, count in self.ships_dict.items():
            shape = self.ship_shapes.get(ship_id)
            if not shape:
                raise ValueError(f"Invalid ship ID: {ship_id}")
            for _ in range(count):
                placed = False
                attempts = 0
                while not placed and attempts < 100:
                    start_x = random.randint(0, self.cols - 1)
                    start_y = random.randint(0, self.rows - 1)
                    if self.can_place_ship(shape, start_x, start_y):
                        self.place_ship(ship_id, shape, start_x, start_y)
                        placed = True
                    attempts += 1
                if not placed:
                    raise ValueError("Unable to place all ships")
 
    def reset_board(self) -> None:
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
 
    def board_stats(self) -> dict:
        empty_spaces = sum(row.count(0) for row in self.board)
        occupied_spaces = self.rows * self.cols - empty_spaces
        return {"empty_spaces": empty_spaces, "occupied_spaces": occupied_spaces}
 
    def print_board(self) -> None:
        for row in self.board:
            print(" ".join(str(cell) for cell in row))