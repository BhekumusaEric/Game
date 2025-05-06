import sys
import argparse

"""This will read the Sudoku puzzle from a file and returns it as a 2D list."""

def read_puzzle(file_path):
    board= []
    with open(file_path,'r') as file:
       puzzle = file.readlines()
       for line in puzzle :
           board.append(list(map(int,line.strip().split())))
    return board

def write_puzzle(file_path, puzzle):
    """ This will be a helper function to print the puzzle in a readable format. """
    with open(file_path, 'w') as f:
        for row in puzzle:
            f.write(' '.join(str(cell) for cell in row) + '\n')

def print_puzzle(puzzle):
    """
    Print the Sudoku puzzle in a readable format.

    Args:
        puzzle (list): 2D list representing the Sudoku puzzle
    """
    horizontal_line = "+-------+-------+-------+"

    for i in range(9):
        if i % 3 == 0:
            print(horizontal_line)

        for j in range(9):
            if j % 3 == 0:
                print("| ", end="")

            # Print the number or a dot for empty cells (0)
            if puzzle[i][j] == 0:
                print(". ", end="")
            else:
                print(f"{puzzle[i][j]} ", end="")

            if j == 8:
                print("|")

    print(horizontal_line)

def is_valid_move(puzzle, row, col, num):
    """
    Check if placing 'num' at position (row, col) is valid.

    Args:
        puzzle (list): 2D list representing the Sudoku puzzle
        row (int): Row index
        col (int): Column index
        num (int): Number to place

    Returns:
        bool: True if the move is valid, False otherwise
    """
    # Check row
    for j in range(9):
        if puzzle[row][j] == num:
            return False

    # Check column
    for i in range(9):
        if puzzle[i][col] == num:
            return False

    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if puzzle[i][j] == num:
                return False

    return True

def find_empty_cell(puzzle):
    #This will returns the row and column of the first empty cell (represented by 0).
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return i, j  # Return the first empty cell found
    return None

def get_row(puzzle, row):
    return puzzle[row]


def get_col(puzzle, col):
    return [puzzle[r][col] for r in range(9)]


def get_box(puzzle, row, col):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    return [
        puzzle[r][c]
        for r in range(start_row, start_row + 3)
        for c in range(start_col, start_col + 3)
    ]


def find_candidates(puzzle, row, col):
    if puzzle[row][col] != 0:
        return []
    used = set(get_row(puzzle, row)) | set(get_col(puzzle, col)) | set(get_box(puzzle, row, col))
    return [n for n in range(1, 10) if n not in used]

def naked_single(puzzle):
    """Apply Naked Single technique to fill in obvious cells."""
    made_progress = False
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                candidates = find_candidates(puzzle, row, col)
                if len(candidates) == 1:
                    puzzle[row][col] = candidates[0]
                    print(f"Naked Single: Cell ({row + 1}, {col + 1}) can only be {candidates[0]}")
                    print_puzzle(puzzle)
                    made_progress = True
    return made_progress

def solve(puzzle):
    """
    Solve the puzzle using naked singles technique first.
    If that doesn't fully solve it, we'll need backtracking.

    Args:
        puzzle (list): 2D list representing the Sudoku puzzle
    """
    print("Initial puzzle:")
    print_puzzle(puzzle)

    while True:
        progress = naked_single(puzzle)
        if not progress:
            break

    if any(0 in row for row in puzzle):
        print("Puzzle is not fully solved. Using backtracking to complete...")
        solve_sudoku(puzzle)
    else:
        print("Sudoku solved successfully!")

def solve_sudoku(puzzle):
    """
    Solve the Sudoku puzzle using backtracking algorithm.

    Args:
        puzzle (list): 2D list representing the Sudoku puzzle

    Returns:
        bool: True if the puzzle is solved, False if no solution exists
    """
    # Find an empty cell
    empty_cell = find_empty_cell(puzzle)

    # If no empty cell is found, the puzzle is solved
    if empty_cell is None:
        return True

    row, col = empty_cell

    # Try placing digits 1-9
    for num in range(1, 10):
        # Check if placing the number is valid
        if is_valid_move(puzzle, row, col, num):
            # Place the number
            puzzle[row][col] = num

            # Recursively try to solve the rest of the puzzle
            if solve_sudoku(puzzle):
                return True

            # If placing the number doesn't lead to a solution, backtrack
            puzzle[row][col] = 0

    # No solution found
    return False


def print_step_explanation(puzzle):
    """
    Print an explanation of the solving steps.

    This function identifies and explains solving techniques like:
    - Naked Singles: Only one possible value for a cell
    - Hidden Singles: Only one possible position for a value in a row/column/box

    Args:
        puzzle (list): 2D list representing the Sudoku puzzle
    """
    # Find all empty cells
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                empty_cells.append((i, j))

    if not empty_cells:
        print("The puzzle is already solved!")
        return

    # Check for naked singles (cells with only one possible value)
    for row, col in empty_cells:
        candidates = find_candidates(puzzle, row, col)

        if len(candidates) == 1:
            print(f"Naked Single: Cell ({row+1},{col+1}) can only be {candidates[0]}")

    # Check for hidden singles in rows
    for row in range(9):
        for num in range(1, 10):
            positions = []
            for col in range(9):
                if puzzle[row][col] == 0 and num in find_candidates(puzzle, row, col):
                    positions.append(col)

            if len(positions) == 1:
                print(f"Hidden Single: {num} can only go in cell ({row+1},{positions[0]+1}) in row {row+1}")

    # Check for hidden singles in columns
    for col in range(9):
        for num in range(1, 10):
            positions = []
            for row in range(9):
                if puzzle[row][col] == 0 and num in find_candidates(puzzle, row, col):
                    positions.append(row)

            if len(positions) == 1:
                print(f"Hidden Single: {num} can only go in cell ({positions[0]+1},{col+1}) in column {col+1}")

    # Check for hidden singles in boxes
    for box_row in range(3):
        for box_col in range(3):
            for num in range(1, 10):
                positions = []
                for r in range(3):
                    for c in range(3):
                        row, col = box_row * 3 + r, box_col * 3 + c
                        if puzzle[row][col] == 0 and num in find_candidates(puzzle, row, col):
                            positions.append((row, col))

                if len(positions) == 1:
                    row, col = positions[0]
                    print(f"Hidden Single: {num} can only go in cell ({row+1},{col+1}) in box {box_row*3+box_col+1}")

def main():
    """
    Main function to handle input/output and solving the puzzle.
    """
    # Check if command line arguments are provided
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        # Use argparse for more flexible command line options
        parser = argparse.ArgumentParser(description="Sudoku Solver with Explanations")
        parser.add_argument("input_file", help="Path to puzzle.txt")
        parser.add_argument("-o", "--output", help="Path to save solved puzzle", required=True)
        args = parser.parse_args()

        input_file = args.input_file
        output_file = args.output

    print(f"Solving puzzle from {input_file}")

    # Read the puzzle
    puzzle = read_puzzle(input_file)

    # Print the original puzzle
    print("Original Puzzle:")
    print_puzzle(puzzle)

    # Print solving steps explanation
    print("\nSolving Steps:")
    print_step_explanation(puzzle)

    # Try to solve with naked singles first, then backtracking if needed
    print("\nSolving...")
    solve(puzzle)

    # Print the solved puzzle
    print("\nSolved Puzzle:")
    print_puzzle(puzzle)

    # Write the solution to the output file
    write_puzzle(output_file, puzzle)
    print(f"Solved puzzle written to {output_file}")

if __name__ == "__main__":
    main()
