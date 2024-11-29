import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.configure(bg="#F0F8FF")  # Light pastel background
        self.sudoku = Sudoku()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.original_grid = None
        self.create_widgets()
        self.color_index = 0
        self.colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8A2BE2"]
        self.fade_step = 0
        self.start_color_animation()

    def create_widgets(self):
        menu_frame = tk.Frame(self.root, bg="#F0F8FF")
        menu_frame.grid(row=0, column=0, columnspan=9, pady=10)

        tk.Label(menu_frame, text="Select Difficulty:", bg="#F0F8FF", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        for difficulty in ["Easy", "Medium", "Hard"]:
            tk.Button(
                menu_frame,
                text=difficulty,
                command=lambda d=difficulty: self.start_game(d.lower()),
                bg="#87CEEB",
                activebackground="#4682B4",
                fg="white",
                font=("Arial", 12),
                relief="groove",
            ).pack(side=tk.LEFT, padx=5)

        tk.Button(menu_frame, text="Validate", command=self.validate_progress, bg="#32CD32", fg="white",
                  font=("Arial", 12), activebackground="#228B22").pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text="New Game", command=self.new_game, bg="#FFD700", fg="black",
                  font=("Arial", 12), activebackground="#DAA520").pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text="Solve", command=self.solve_puzzle, bg="#FF6347", fg="white",
                  font=("Arial", 12), activebackground="#CD5C5C").pack(side=tk.LEFT, padx=10)

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(
                    self.root,
                    width=2,
                    font=("Arial", 18),
                    justify="center",
                    validate="key",
                    validatecommand=(self.root.register(self.validate_entry), "%P"),
                )
                entry.grid(row=row + 1, column=col, padx=5, pady=5)

                entry.configure(bg="#FAFAD2")
                self.entries[row][col] = entry

    def validate_entry(self, value):
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False

    def start_game(self, difficulty):
        self.sudoku.fill_grid()
        self.sudoku.remove_cells(difficulty=difficulty)
        self.original_grid = [row[:] for row in self.sudoku.grid]
        self.update_grid()

    def update_grid(self):
        for row in range(9):
            for col in range(9):
                value = self.sudoku.grid[row][col]
                entry = self.entries[row][col]
                entry.delete(0, tk.END)
                if value != 0:
                    entry.insert(0, str(value))
                    entry.configure(state="disabled", fg="#4169E1")
                else:
                    entry.configure(state="normal", fg="black")

    def validate_progress(self):
        player_grid = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                value = self.entries[row][col].get()
                player_grid[row][col] = int(value) if value.isdigit() else 0

        for row in range(9):
            for col in range(9):
                if player_grid[row][col] != 0 and not self.sudoku.is_valid(row, col, player_grid[row][col]):
                    self.entries[row][col].configure(bg="#FF7F7F")
                else:
                    self.entries[row][col].configure(bg="#FAFAD2" if (row // 3 + col // 3) % 2 == 0 else "#FFFACD")

        if player_grid == self.sudoku.grid:
            messagebox.showinfo("Congratulations", "You solved the Sudoku puzzle!")

    def clear_grid(self):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)
                entry.configure(state="normal", bg="#FAFAD2" if (row // 3 + col // 3) % 2 == 0 else "#FFFACD")

    def new_game(self):
        self.clear_grid()

    def solve_puzzle(self):
        self.sudoku.solve_sudoku()
        self.update_grid()
        messagebox.showinfo("Solution", "The Sudoku puzzle has been solved!")

    def start_color_animation(self):
        """Initiates the color fading animation."""
        self.fade_step = 0
        self.fade_color()

    def fade_color(self):
        """Handles the fading effect between two colors."""
        start_color = self.colors[self.color_index]
        next_color_index = (self.color_index + 1) % len(self.colors)
        end_color = self.colors[next_color_index]

        r1, g1, b1 = self.hex_to_rgb(start_color)
        r2, g2, b2 = self.hex_to_rgb(end_color)

        r = int(r1 + (r2 - r1) * (self.fade_step / 100))
        g = int(g1 + (g2 - g1) * (self.fade_step / 100))
        b = int(b1 + (b2 - b1) * (self.fade_step / 100))

        color = self.rgb_to_hex((r, g, b))
        for row in range(9):
            for col in range(9):
                self.entries[row][col].configure(bg=color)

        self.fade_step += 2
        if self.fade_step > 100:
            self.fade_step = 0
            self.color_index = (self.color_index + 1) % len(self.colors)

        self.root.after(50, self.fade_color)

    @staticmethod
    def hex_to_rgb(hex_color):
        return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb_to_hex(rgb):
        return "#{:02X}{:02X}{:02X}".format(*rgb)


class Sudoku:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num, grid=None):
        grid = grid or self.grid
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False

        return True

    def fill_grid(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(row, col, num):
                            self.grid[row][col] = num
                            if self.fill_grid():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True

    def remove_cells(self, difficulty):
        attempts = {"easy": 30, "medium": 40, "hard": 50}.get(difficulty, 40)
        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.grid[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            backup = self.grid[row][col]
            self.grid[row][col] = 0

            copy_grid = [row[:] for row in self.grid]
            if not self.solve_sudoku(copy_grid):
                self.grid[row][col] = backup
            else:
                attempts -= 1

    def solve_sudoku(self, grid=None):
        grid = grid or self.grid
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num, grid):
                            grid[row][col] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()
