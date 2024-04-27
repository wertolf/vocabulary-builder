"""
核心层(core)主模块。
"""
from typing import List
from typing import MutableSet

from .player import Player
from .vector import Vector2D

from . import board

# 本局游戏的基本信息
n_player: int = 0 # 本局游戏的玩家个数
player_list: List[Player] = []
pid: int  # 用于标记当前回合的玩家

# 游戏进行过程中的信息
piece: Vector2D = None # 当前被拿起的棋子
q_set: MutableSet[Vector2D] = set()  # 从piece出发的所有合法落子点所构成的集合

def start_game_2p():
    global n_player
    global pid
    global player_list

    n_player = 2
    player_list.clear()
    for _ in range(n_player):
        player_list.append(Player())

    # 初始化玩家的棋子
    player_list[0].occupied_location_set = set(board.xii)
    player_list[1].occupied_location_set = set(board.vi)

    # 目标，也就是为了获得胜利而需要到达的所有点的位置
    player_list[0].goal_location_set = set(board.vi)
    player_list[1].goal_location_set = set(board.xii)

    pid = 0


def calculate_q_set():
    """
    既然我们把起点叫做p，不妨把落点叫做q，所有可能落点构成的集合叫做q_set
    """
    global q_set

    q_set.clear()
    add_valid_neighbors()
    add_valid_images()


def next_turn():
    global pid

    pid += 1
    pid %= n_player


"""
calculate_q_set()分解后的步骤。

目前采用的是一阶逻辑，即，禁用递归跳跃。

当年写这个游戏时，也是从一阶逻辑开始的。
事实上，高阶逻辑涉及递归，
如果不先从数学上给出一个优雅的答案，那么代码的实现注定是基于暴力求解的一团糟。
"""
def add_valid_neighbors():
    """
    从6个邻位中物色落点。

    落点需要满足如下条件：
    * 在棋盘上
    * 其上没有棋子
    """
    global q_set
    for v in board.neighbors:
        q = Vector2D(piece.x + v.x, piece.y + v.y)
        if is_inside_board(q) and not is_occupied_at(q):
            q_set.add(q)
            

def add_valid_images():

    f_set = get_fulcrum_set()

    # 利用 p与q关于f对称 这一关系，在所有可能的q中物色落点

    for f in f_set:
        dx, dy = (f.x - piece.x, f.y - piece.y)
        q = Vector2D(f.x + dx, f.y + dy)
        q_set.add(q)  # q的合法性已经由get_fulcrum_set保证，无需再次检查


def get_fulcrum_set():

    fulcrum_set = set()

    # 沿x轴正向寻找f
    found, f = look_for_fulcrum(direction=Vector2D(1, 0))
    if found:
        fulcrum_set.add(f)
    # 沿x轴负向寻找f
    found, f = look_for_fulcrum(direction=Vector2D(-1, 0))
    if found:
        fulcrum_set.add(f)
    # 沿y轴正向寻找f
    found, f = look_for_fulcrum(direction=Vector2D(0, 1))
    if found:
        fulcrum_set.add(f)
    # 沿y轴负向寻找f
    found, f = look_for_fulcrum(direction=Vector2D(0, -1))
    if found:
        fulcrum_set.add(f)
    # 沿y=x正向寻找f
    found, f = look_for_fulcrum(direction=Vector2D(1, 1))
    if found:
        fulcrum_set.add(f)
    # 沿y=x负向寻找f
    found, f = look_for_fulcrum(direction=Vector2D(-1, -1))
    if found:
        fulcrum_set.add(f)

    return fulcrum_set    


def look_for_fulcrum(direction: Vector2D):

    found = False
    hit = False
    x, y = piece
    i = 0  # 用于记录迭代次数，从而记录移动的距离
    d = -1  # p到f的距离
    
    while not found:

        # 更新循环变量（沿给定方向移动一个单位所到达的下一个点）
        x += direction.x
        y += direction.y
        i += 1

        if not is_inside_board(Vector2D(x, y)):  # 如果已超出棋盘
            # 如果还没找到潜在的f，说明该方向不存在潜在的f
            # 如果已经找到潜在的f，说明空间不够，即从p出发经过f跳到q时，q会超出棋盘
            return (found, None)

        if not hit:  # 如果还没找到潜在的f
            if is_occupied_at(Vector2D(x, y)):  # 如果这个位置有棋子
                f = Vector2D(x, y)  # 将这个位置标记为潜在的f

                # 更新相关变量
                d = i
                hit = True
        elif i <= abs(2 * d):  # 如果已经找到潜在的f，需要进一步确认f与q之间（含q）没有其他棋子
            if is_occupied_at(Vector2D(x, y)):  # 如果当前位置有棋子
                return (found, None)  # 说明潜在的f不满足成为f的充分条件
        else:
            found = True
            return (found, f)


"""
布尔函数。
"""
def is_inside_board(v: Vector2D):
    """
    布尔函数，判断(v.x, v.y)所在位置是否在棋盘内。
    """
    return v in board.board

def is_occupied_at(v: Vector2D):
    """
    布尔函数，判断(v.x, v.y)所在位置是否有棋子。
    """
    for player in player_list:
        if v in player.occupied_location_set:
            return True
    return False


def is_valid_pick(v: Vector2D):
    """
    布尔函数，判断玩家能否拿起位置v处的棋子。
    """
    return v in get_current_player().occupied_location_set


def is_valid_move(v: Vector2D):
    """
    布尔函数，判断玩家能否在位置v处落子。
    """
    return v in q_set


"""
Wrappers.
"""
def get_current_color():
    return get_current_player().color

def get_current_player() -> Player:
    return player_list[pid]


def get_current_piece() -> Vector2D:
    return piece

def set_current_piece(v: Vector2D):
    global piece
    
    piece = v
