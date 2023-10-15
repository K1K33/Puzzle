import heapq
import copy

class PuzzleState:
    def __init__(self, board, g, h, parent=None, move=""):
        self.board = board
        self.g = g  
        self.h = h  
        self.parent = parent
        self.move = move

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def is_goal(state, goal):
    return state.board == goal

def generate_moves(state):
    moves = []
    directions = [(0, 1, 'derecha'), (0, -1, 'izquierda'), (1, 0, 'abajo'), (-1, 0, 'arriba')]
    for dx, dy, move_type in directions:
        for i in range(3):
            for j in range(3):
                if state.board[i][j] == "*":
                    new_x, new_y = i + dx, j + dy
                    if 0 <= new_x < 3 and 0 <= new_y < 3:
                        new_board = copy.deepcopy(state.board)
                        new_board[i][j], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[i][j]
                        moves.append((new_board, move_type))
    return moves

def calculate_manhattan_distance(board, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != goal[i][j] and board[i][j] != '*':
                val = int(board[i][j])
                target_i, target_j = divmod(val - 1, 3)
                distance += abs(i - target_i) + abs(j - target_j)
    return distance

def solve_puzzle(initial_state, goal_state):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, initial_state)
    while open_list:
        current_state = heapq.heappop(open_list)
        if is_goal(current_state, goal_state):
            return current_state
        closed_list.add(tuple(map(tuple, current_state.board)))
        for move, move_type in generate_moves(current_state):
            if tuple(map(tuple, move)) not in closed_list:
                g = current_state.g + 1
                h = calculate_manhattan_distance(move, goal_state)
                new_state = PuzzleState(move, g, h, current_state, move_type)
                heapq.heappush(open_list, new_state)
    return None

# Estado inicial y objetivo original
initial_state = [['7', '2', '4'], ['5', '*', '6'], ['8', '3', '1']]
goal_state = [['*', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]

initial_state = PuzzleState(initial_state, 0, calculate_manhattan_distance(initial_state, goal_state), None, "")
goal_state = goal_state

solution = solve_puzzle(initial_state, goal_state)

if solution:
    path = []
    moves_cost = 0
    while solution:
        path.append(solution)
        solution = solution.parent
    path.reverse()
    for i, p in enumerate(path):
        if p.move:
            print(f"Move {i}: {p.move}")
            moves_cost += 1
            print("State:")
            for row in p.board:
                print(row)
            print()
    print(f"Total cost of moves: {moves_cost}")
else:
    print("No solution found for the puzzle.")
