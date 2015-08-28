# Tic Tac Toe using nested lists (simple matrix.)


board = []
turn = 0
def make_board():
    global board
    board = []
    h = [' ', '1', '2', '3']
    a = ['a', '.','.','.']
    b = ['b', '.','.','.']
    c = ['c', '.','.','.']
    board.append(h)
    board.append(a)
    board.append(b)
    board.append(c)

def draw_board():
    for x in board:
        print " ".join(x)
    print ' '

def start():
    make_board()
    draw_board()

def first():
    if board[2][2] is not 'X':
        board[2][2] = 'O'
    else:
        board[1][1]  = 'O'

def play_offense():
    moves = [ diag, horizontal, vertical ]
    for i in moves:
        if i('O', play_offense=True):
            return True
    for i in range(1, len(board)):
        if '.' in board[i]:
            board[i][board[i].index('.')] = 'O'
            return True

def win_message(a):
    print ' '
    draw_board()
    print ' '
    print("'%s' Wins" % a)
    print 'Play again!'
    global turn
    turn = 0
    make_board()
    return True

def check_win():
    vertical_board = _vertical()
    left  =  _diag('leftTop')
    right =  _diag('rightTop')
    for i in ['X', 'O',]:
        for x in range(1, len(board)):
            if board[x].count(i) == 3:
                win_message(i)
                return True
        for v in range(len(vertical_board)):
            if vertical_board[v].count(i) == 3:
                win_message(i)
                return True
        if left.count(i) == 3:
            win_message(i)
            return True
        if right.count(i) == 3:
            win_message(i)
            return True
    return False

def check_draw():
    b = [x for y in board for x in y]
    if '.' not in b:
        print ' '
        print 'A strange game.'
        print 'The only winning move is not to play.'
        global turn
        turn = 0
    return False

def horizontal(a, play_offense=False):
    for i in range(1, len(board)):
        if play_offense is False:
            if board[i].count(a) == 2 and '.' in board[i]:
                board[i] = [b.replace('.', 'O') for b in board[i]]
                return True
        else:
            if board[i].count('.') == 2 and 'O' in board[i]:
                board[i][board[i].index('.')] = 'O'
                return True
    return False

def _vertical():
    t1 = []
    for x in range(len(board[0])):
        t2 = []
        for i in range(len(board[0])):
            t2.append(board[i][x])
        t1.append(t2)
    return t1

def vertical(a, play_offense=False):
    t1 = _vertical()
    if play_offense is False:
        for i in range(len(t1)):
            if t1[i].count(a) == 2:
                if '.' in t1[i]:
                    index1 = t1[i].index('.')
                    index2 = int(t1[i][0])
                    board[index1][index2] = 'O'
                    return True
                else:
                    return False
    else:
        for i in range(len(t1)):
            if t1[i].count('.') == 2 and 'O' in board[i]:
                board[i][board[i].index('.')] = 'O'
                return True
            else:
                return False

def _diag(direction):
    diag_moves = []
    if 'leftTop' in direction:
        for i in range(len(board)):
            diag_moves.append(board[i][i])
        return diag_moves
    else:
        c = len(board) - 1
        for i in range(1, len(board)):
            diag_moves.append(board[i][c])
            c -= 1
        return diag_moves

def diag(a, play_offense=False):
    left  = _diag('leftTop')
    right = _diag('rightTop')
    c = len(board) - 1
    if play_offense is False:
        if left.count(a) == 2 and '.' in left:
            for i in range(len(board)):
                if board[i][i] == '.':
                    board[i][i] = 'O'
            return True
        elif right.count(a) == 2 and '.' in right:
            for i in range(1, len(board)):
                if board[i][c] == '.':
                    board[i][c] = 'O'
                c -= 1
            return True
    else:
        if left.count('.') == 2 and 'O' in left:
            board[left.index('.')][left.index('.')] = 'O'
            return True
        if right.count('.') == 2 and 'O' in right:
            for x in range(1, len(board)):
                y = len(right) - right.index('.')
                print board[right.index('.')][y]
                board[right.index('.') + 1][y] = 'O'
            return True
    return False

def is_game_over():
    check_win()
    check_draw()

def play():
    global turn
    turn += 1
    if turn == 1:
        first()
        return
    is_game_over()
    if horizontal('O') is True:
        return
    if horizontal('X') is True:
        return
    if vertical('O') is True:
        return
    if vertical('X') is True:
        return
    if diag('O') is True:
        return
    if diag('X') is True:
        return
    else:
        play_offense()
        return

if __name__ == "__main__":
    while True:
        if turn == 0:
            print ' '
            print "Enter a1, b2, c3, etc"
            start()
        else:
            is_game_over()
            draw_board()
        choice = raw_input('Your Move: ')
        index = {'a': 1, 'b': 2, 'c': 3}
        row = choice[0].lower()
        col = int(choice[1])
        if board[index[row]][col] == 'X' \
            or board[index[row]][col] == 'O':
            print "That spot is taken. Try again."
            next
        else:
            board[index[row]][col] = 'X'
            play()
