import copy
import random
import sys
WIDTH = 8
HEIGHT = 8

# 位置权重表（用于AI决策），角点最高，边次之，中央最低
WEIGHTS = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -30, 1, 1, 1, 1, -30, -20],
    [10, 1, 0, 0, 0, 0, 1, 10],
    [5, 1, 0, 0, 0, 0, 1, 5],
    [5, 1, 0, 0, 0, 0, 1, 5],
    [10, 1, 0, 0, 0, 0, 1, 10],
    [-20, -30, 1, 1, 1, 1, -30, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]


def drawBoard(board):
    """打印当前棋盘"""
    print('  1 2 3 4 5 6 7 8')
    print(' +---------------+')
    for y in range(HEIGHT):
        print(str(y + 1) + '|', end='')
        for x in range(WIDTH):
            print(board[y][x], end='')
            if x < WIDTH - 1:
                print(' ', end='')
        print('|' + str(y + 1))
    print(' +---------------+')
    print('  1 2 3 4 5 6 7 8')


def getNewBoard():
    """创建并返回一个新的空白棋盘"""
    board = []
    for y in range(HEIGHT):
        board.append([' '] * WIDTH)
    # 初始放置四颗棋子
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'
    return board


def isOnBoard(x, y):
    """判断坐标是否在棋盘内"""
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


def isValidMove(board, tile, xstart, ystart):
    """判断在(xstart, ystart)位置放置tile棋子是否合法，合法则返回要翻转的棋子列表，否则返回False"""
    if board[ystart][xstart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    # 八个方向
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x = xstart + xdirection
        y = ystart + ydirection
        # 如果这个方向上有对方的棋子，继续沿该方向走
        if isOnBoard(x, y) and board[y][x] == otherTile:
            x += xdirection
            y += ydirection
            while isOnBoard(x, y) and board[y][x] == otherTile:
                x += xdirection
                y += ydirection
            # 如果方向尽头是自己的棋子，则记录路径上的所有对方棋子
            if isOnBoard(x, y) and board[y][x] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append((x, y))
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def getValidMoves(board, tile):
    """返回当前玩家所有合法移动的列表"""
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append((x, y))
    return validMoves


def makeMove(board, tile, xstart, ystart):
    """在棋盘上放置棋子，并翻转对方棋子，返回是否成功"""
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if not tilesToFlip:
        return False
    board[ystart][xstart] = tile
    for x, y in tilesToFlip:
        board[y][x] = tile
    return True


def getBoardCopy(board):
    """复制棋盘"""
    return copy.deepcopy(board)


def getBoardWithValidMoves(board, tile):
    """返回一个棋盘副本，并在所有合法移动位置显示'.'"""
    boardCopy = getBoardCopy(board)
    validMoves = getValidMoves(board, tile)
    for x, y in validMoves:
        boardCopy[y][x] = '.'
    return boardCopy


def getScoreOfBoard(board):
    """计算双方棋子数量，返回字典{'X': 数量, 'O': 数量}"""
    xscore = 0
    oscore = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if board[y][x] == 'X':
                xscore += 1
            elif board[y][x] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    """让玩家选择棋子，返回[玩家棋子, 电脑棋子]"""
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    """随机决定谁先走"""
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def getPlayerMove(board, playerTile):
    """获取玩家输入的移动位置，增强输入提示"""
    validMoves = getValidMoves(board, playerTile)
    if not validMoves:
        return None

    # 将合法移动转换为用户坐标（行,列）方便显示
    user_valid = [(y+1, x+1) for (x, y) in validMoves]  # (行, 列)
    while True:
        print('Enter your move (row col), or "quit" to end the game:')
        if user_valid:
            print('Valid moves: ', user_valid)
        move = input().lower()
        if move == 'quit':
            sys.exit()
        try:
            # 用户输入的是“行 列”（1-8）
            row = int(move.split()[0]) - 1
            col = int(move.split()[1]) - 1
        except (IndexError, ValueError):
            print('Invalid input. Please enter row and column numbers separated by space.')
            continue
        # 内部坐标是(col, row)
        if (col, row) in validMoves:
            return (col, row)
        else:
            print('That is not a valid move. Try again.')


def getComputerMove(board, computerTile):
    """电脑的移动策略：基于位置权重选择合法移动（取第一个遇到的最高权重位置）"""
    validMoves = getValidMoves(board, computerTile)
    if not validMoves:
        return None
    bestScore = -float('inf')
    bestMove = None
    for x, y in validMoves:
        score = WEIGHTS[y][x]
        if score > bestScore:
            bestScore = score
            bestMove = (x, y)
    # 理论上validMoves非空时bestMove一定被赋值，但为安全保留随机fallback
    if bestMove is None:
        return random.choice(validMoves)
    return bestMove


def isGameOver(board):
    """检查游戏是否结束（双方均无合法移动）"""
    return not (getValidMoves(board, 'X') or getValidMoves(board, 'O'))


def main():
    print('Welcome to Othello (Reversi)!')
    playerTile, computerTile = enterPlayerTile()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    board = getNewBoard()

    while True:
        # 显示棋盘（玩家回合显示带.的辅助棋盘，电脑回合显示普通棋盘）
        if turn == 'player':
            displayBoard = getBoardWithValidMoves(board, playerTile)
            drawBoard(displayBoard)
        else:
            drawBoard(board)

        scores = getScoreOfBoard(board)
        print('X: %d  O: %d' % (scores['X'], scores['O']))

        if turn == 'player':
            move = getPlayerMove(board, playerTile)
            if move:
                makeMove(board, playerTile, move[0], move[1])
                turn = 'computer'
            else:
                print('You have no valid moves. Turn passes to computer.')
                turn = 'computer'
        else:
            print('Computer is thinking...')
            move = getComputerMove(board, computerTile)
            if move:
                print('Computer places at (%d, %d)' % (move[0] + 1, move[1] + 1))
                makeMove(board, computerTile, move[0], move[1])
                turn = 'player'
            else:
                print('Computer has no valid moves. Turn passes to you.')
                turn = 'player'

        # 检查游戏结束
        if isGameOver(board):
            break

    # 游戏结束，显示最终结果
    drawBoard(board)
    scores = getScoreOfBoard(board)
    print('Final scores: X: %d  O: %d' % (scores['X'], scores['O']))
    if scores['X'] > scores['O']:
        print('X wins!')
    elif scores['O'] > scores['X']:
        print('O wins!')
    else:
        print('It\'s a tie!')


if __name__ == '__main__':
    main()