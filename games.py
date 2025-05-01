import random

SIZE = 20
Ant_count = 100 
Bug_count = 5
Bug_breed = 8
Ant_breed = 3
Bug_death = 3

EMPTY = '.'
ANT = 'o'
BUG = 'X'

ant_moves = {}
bug_moves = {}
bug_starves = {}


def create_grid():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def display_grid(grid):
    for row in grid:
        print(''.join(row))
    print()


def place_ants(grid):
    placed = 0
    while placed < Ant_count:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if grid[x][y] == EMPTY:
            grid[x][y] = ANT
            ant_moves[(x, y)] = 0
            placed += 1


def place_bugs(grid):
    placed = 0
    while placed < Bug_count:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if grid[x][y] == EMPTY:
            grid[x][y] = BUG
            bug_moves[(x, y)] = 0
            bug_starves[(x, y)] = 0
            placed += 1


def set_direction(x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            neighbors.append((nx, ny))
    return neighbors


def move_ants(grid):
    global ant_moves
    updated_ant_moves = {}
    ants = list(ant_moves.keys())
    random.shuffle(ants)

    for x, y in ants:
        if grid[x][y] != ANT:
            continue

        neighbors = set_direction(x, y)
        random.shuffle(neighbors)
        moved = False

        for nx, ny in neighbors:
            if grid[nx][ny] == EMPTY:
                grid[nx][ny] = ANT
                grid[x][y] = EMPTY
                updated_ant_moves[(nx, ny)] = ant_moves[(x, y)] + 1
                moved = True
                break

        if not moved:
            updated_ant_moves[(x, y)] = ant_moves[(x, y)] + 1

    ant_moves = updated_ant_moves


def breed_ants(grid):
    global ant_moves
    new_ants = {}
    for (x, y), moves in ant_moves.items():
        if moves >= Ant_breed:
            neighbors = set_direction(x, y)
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if grid[nx][ny] == EMPTY:
                    grid[nx][ny] = ANT
                    new_ants[(nx, ny)] = 0
                    ant_moves[(x, y)] = 0
                    break
    ant_moves.update(new_ants)


def move_doodlebugs(grid):
    global bug_moves, bug_starves
    updated_bug_moves = {}
    updated_starves = {}
    bugs = list(bug_moves.keys())
    random.shuffle(bugs)

    for x, y in bugs:
        if grid[x][y] != BUG:
            continue

        neighbors = set_direction(x, y)
        random.shuffle(neighbors)
        moved = False

        
        for nx, ny in neighbors:
            if grid[nx][ny] == ANT:
                grid[nx][ny] = BUG
                grid[x][y] = EMPTY
                updated_bug_moves[(nx, ny)] = bug_moves[(x, y)] + 1
                updated_starves[(nx, ny)] = 0
                moved = True
                break

        
        if not moved:
            for nx, ny in neighbors:
                if grid[nx][ny] == EMPTY:
                    grid[nx][ny] = BUG
                    grid[x][y] = EMPTY
                    updated_bug_moves[(nx, ny)] = bug_moves[(x, y)] + 1
                    updated_starves[(nx, ny)] = bug_starves[(x, y)] + 1
                    moved = True
                    break

        
        if not moved:
            updated_bug_moves[(x, y)] = bug_moves[(x, y)] + 1
            updated_starves[(x, y)] = bug_starves[(x, y)] + 1

    bug_moves = updated_bug_moves
    bug_starves = updated_starves


def breed_doodlebugs(grid):
    global bug_moves, bug_starves
    new_bugs = {}
    for (x, y), moves in bug_moves.items():
        if moves >= Bug_breed:
            neighbors = set_direction(x, y)
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if grid[nx][ny] == EMPTY:
                    grid[nx][ny] = BUG
                    new_bugs[(nx, ny)] = 0
                    bug_moves[(x, y)] = 0
                    bug_starves[(nx, ny)] = 0
                    break
    bug_moves.update(new_bugs)


def death_doodlebugs(grid):
    global bug_moves, bug_starves
    to_remove = []
    for (x, y), starve_count in bug_starves.items():
        if starve_count >= Bug_death:
            grid[x][y] = EMPTY
            to_remove.append((x, y))

    for pos in to_remove:
        bug_moves.pop(pos, None)
        bug_starves.pop(pos, None)


def main():
    grid = create_grid()
    place_ants(grid)
    place_bugs(grid)

    while True:
        display_grid(grid)
        input("Press Enter for next step...")

        move_doodlebugs(grid)
        death_doodlebugs(grid)
        breed_doodlebugs(grid)

        move_ants(grid)
        breed_ants(grid)

main()
