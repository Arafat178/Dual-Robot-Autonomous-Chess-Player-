from robodk.robolink import Robolink, ITEM_TYPE_ROBOT
from robodk.robomath import *
import chess
import chess.engine
import time

RDK = Robolink()

# robotic arm setup
robot_white = RDK.Item('RoboDK RDK-COBOT-1200', ITEM_TYPE_ROBOT)
robot_black = RDK.Item('AUBO-iS20', ITEM_TYPE_ROBOT)

# white robot base frame
common_frame = robot_white.Parent()

# distance between white robot to board center
BOARD_CENTER_X = 700.0
SQ_SIZE = 51.0
Z_GRAB = 15.0  # grab height
Z_SAFE = 120.0  # intern position of piece

# home position of arms
HOME_WHITE = [-167.47, -36.60, 118.11, 18.55, -90.00, 90.00]
HOME_BLACK = [-179.50, 61.17, 139.39, -15.04, 90.00, 0.00]


# square position finder
def get_square_pose(square_str):
    col_idx = ord(square_str[0]) - ord('a')
    row_idx = int(square_str[1]) - 1

    tx = BOARD_CENTER_X + (row_idx - 3.5) * SQ_SIZE
    ty = (col_idx - 3.5) * SQ_SIZE

    # postion + rotation rotx(pi) for vertical grabbing
    return transl(tx, ty, Z_GRAB) * rotx(pi)


def get_item_at(target_pose, threshold=25.0):
    #select all items
    all_items = RDK.ItemList()

    target_pos = target_pose.Pos()  # target(x,y,z)

    for item in all_items:
        # 5 means ITEM_TYPE_OBJECT ( chess pieces)
        if item.Type() == 5:
            item_pos = item.Pose().Pos()

            # Euclidean Distance: sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
            distance = norm(subs3(target_pos, item_pos))

            if distance < threshold:
                return item

    return None

# movement logic
def execute_move(robot, start_sq, end_sq, home_joints):
    robot.setPoseFrame(common_frame)
    robot_tool = robot.Childs()[0]  # Gripper

    p_start = get_square_pose(start_sq)
    p_end = get_square_pose(end_sq)

    p_start_up = transl(0, 0, Z_SAFE) * p_start
    p_end_up = transl(0, 0, Z_SAFE) * p_end

    # find square position
    piece_item = get_item_at(p_start)

    robot.MoveJ(home_joints)

    # --- PICK ---
    robot.MoveJ(p_start_up)
    robot.MoveL(p_start)

    if piece_item:
        piece_item.setParentStatic(robot_tool)
        print(f"Picked up item from {start_sq}")
    else:
        print(f"Warning: No piece found at {start_sq}!")

    time.sleep(0.5)
    robot.MoveL(p_start_up)

    # --- PLACE ---
    robot.MoveJ(p_end_up)
    robot.MoveL(p_end)

    if piece_item:
        piece_item.setParentStatic(common_frame)
        print(f"Placed item at {end_sq}")

    time.sleep(0.5)
    robot.MoveL(p_end_up)

    robot.MoveJ(home_joints)


# piece position besides board
GRAVEYARD_WHITE = [700, 300, Z_GRAB] # for white
GRAVEYARD_BLACK = [700, -300, Z_GRAB] # for black


def remove_piece(robot, target_sq, graveyard_pos, home_joints):
    robot.setPoseFrame(common_frame)
    robot_tool = robot.Childs()[0]

    p_target = get_square_pose(target_sq)
    # finding piece
    captured_piece = get_item_at(p_target)

    if captured_piece:
        print(f"Capturing piece at {target_sq}...")
        p_target_up = transl(0, 0, Z_SAFE) * p_target
        p_grave = transl(graveyard_pos[0], graveyard_pos[1], graveyard_pos[2]) * rotx(pi)
        p_grave_up = transl(0, 0, Z_SAFE) * p_grave

        # grab piece
        robot.MoveJ(p_target_up)
        robot.MoveL(p_target)
        captured_piece.setParentStatic(robot_tool)
        time.sleep(0.5)
        robot.MoveL(p_target_up)

        # remove from board
        robot.MoveJ(p_grave_up)
        robot.MoveL(p_grave)
        captured_piece.setParentStatic(common_frame)
        time.sleep(0.5)
        robot.MoveL(p_grave_up)

        # ready for next move
    else:
        print(f"No piece to capture at {target_sq}")



# stockfish chess engine
def start_game():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(r"E:/BUET 4-2/ME 447 Robotics/stockfish-10-win/Windows/stockfish_10_x64.exe")

    try:
        while not board.is_game_over():
            result = engine.play(board, chess.engine.Limit(time=0.1))
            move = result.move
            src, dst = move.uci()[:2], move.uci()[2:]

            # checking capturing...
            if board.is_capture(move):
                if board.turn == chess.WHITE:
                    # capturing black piece
                    remove_piece(robot_white, dst, GRAVEYARD_WHITE, HOME_WHITE)
                else:
                    # capturing white piece
                    remove_piece(robot_black, dst, GRAVEYARD_BLACK, HOME_BLACK)

            # own piece move
            if board.turn == chess.WHITE:
                print(f"WHITE Move: {src}->{dst}")
                execute_move(robot_white, src, dst, HOME_WHITE)
            else:
                print(f"BLACK Move: {src}->{dst}")
                execute_move(robot_black, src, dst, HOME_BLACK)

            board.push(move)
    finally:
        engine.quit()

if __name__ == "__main__":
    start_game()
