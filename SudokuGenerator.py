from random import randint
import time
class square():
    def __init__(self):
        self.fixed = False
        self.num = " "
        self.exceptions = []

class board():

    def __init__(self):
        self.nums = []
        for x in range(9):
            row = []
            for y in range(9):
                row.append(square())
            self.nums.append(row)
        
        self.digits = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    
    def available_numbers(self, row, col):
        available = []
        for num in self.digits:
            if self.is_legal(row, col, num) and num not in self.nums[row][col].exceptions:
                available.append(num)
        return available

    def is_legal(self, row, col, num):
        return self.legal_in_box(row, col, num) and self.legal_in_col(col, num) and self.legal_in_row(row, num)

    def legal_in_box(self, row, col, num):
        row_start = int(row / 3) * 3
        col_start = int(col / 3) * 3
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if self.nums[r][c].num == num:
                    return False
        return True

    def legal_in_row(self, row, num):
        for c in range(9):
            if self.nums[row][c].num == num:
                return False
        return True

    def legal_in_col(self, col, num):
        for r in range(9):
            if self.nums[r][col].num == num:
                return False
        return True

    def fill_box(self, row, col):
        digits = self.available_numbers(row, col)
        if len(digits) == 0:
            return False
        self.nums[row][col].num = digits[randint(0, len(digits)-1)]
        return True

    def fill_board(self):
        row = col = 0
        while(row < 9):
            while(col < 9):
                if not self.fill_box(row, col):
                    self.nums[row][col].exceptions = []
                    self.nums[row][col].num = " "
                    col -= 1
                    if col < 0:
                        col = 8
                        row -= 1
                    self.nums[row][col].exceptions.append(self.nums[row][col].num)
                else:
                    col += 1
            row += 1
            col = 0
    
    def print_board(self):
        for row in range(9):
            for col in range(9):
                print(self.nums[row][col].num, end=' ')
            print()

    def to_string(self):
        str = ""
        for row in self.nums:
            for sqr in row:
                str += sqr.num
        return str

    def set(self, str):
        for row in range(9):
            for col in range(9):
                self.nums[row][col].num = str[row*9 + col]
                if str[row*9 + col] != " ":
                    self.nums[row][col].fixed = True

    equal = True
    def can_solve(self, str):
        global equal
        equal = True
        broken = board()
        broken.set(str)
        return self.solve(broken, 0, 0)

    def solve(self, broken, row, col):
        global equal
        if equal:
            if not " " in broken.to_string() and not self.to_string() == broken.to_string():
                equal = False
            elif row < 9 and not broken.nums[row][col].fixed:
                nums = broken.available_numbers(row, col)
                for num in nums:
                    broken.nums[row][col].num = num
                    if col == 8:
                        self.solve(broken, row+1, 0)
                    else:
                        self.solve(broken, row, col+1)
                    broken.nums[row][col].num = " "
                    if not equal:
                        break
            elif row < 9:
                if col == 8:
                    self.solve(broken, row+1, 0)
                else:
                    self.solve(broken, row, col+1)
        return equal

    def clues(self, n):
        chars = list(self.to_string())
        for x in range(81-n):
            done = False
            while not done:
                rand = randint(0, 80)
                if chars[rand] != ' ':
                    chars[rand] = ' '
                    done = True
        string = ""
        for x in range(81):
            string += chars[x]
        return string

    def generate(self,  n):
        go = True;
        input = "";
        count = 0
        while go:
            count += 1
            elapsed = time.time()
            input = self.clues(n);
            go = not self.can_solve(input);
            print(count, " took ", time.time() - elapsed, " seconds")
        return input

    cont = True
    def solve_board(self):
        global cont
        cont = True
        self.solve_incomplete(0, 0)

    def solve_incomplete(self, row, col):
        global cont
        if cont:
            if not " " in self.to_string():
                cont = False
            elif row < 9 and not self.nums[row][col].fixed:
                nums = self.available_numbers(row, col)
                for num in nums:
                    self.nums[row][col].num = num
                    if col == 8:
                        self.solve_incomplete(row+1, 0)
                    else:
                        self.solve_incomplete(row, col+1)
                    if not cont:
                        break
                    self.nums[row][col].num = " "
            elif row < 9:
                if col == 8:
                    self.solve_incomplete(row+1, 0)
                else:
                    self.solve_incomplete(row, col+1)



thing = board()
thing.fill_board()
thing.print_board()

print()

thing2 = board()
thing2.set(thing.generate(20))
thing2.print_board()

print()

thing2.solve_board()
thing2.print_board()

