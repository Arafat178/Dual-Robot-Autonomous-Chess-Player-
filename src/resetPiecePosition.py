from robodk.robolink import Robolink, ITEM_TYPE_OBJECT
from robodk.robomath import *

RDK = Robolink()

# ১. ক্যালিব্রেশন ডাটা (তোমার আগের কোড অনুযায়ী)
BOARD_CENTER_X = 700.0
SQ_SIZE = 51.0
Z_GRAB = 10.0  # টেবিলের ওপর পিসের উচ্চতা

# ২. শুরুর পজিশন ম্যাপিং (White: Rank 1 & 2, Black: Rank 7 & 8)
initial_positions = {
    # সাদা পিস (White)
    'R': ['a1', 'h1'], 'N': ['b1', 'g1'], 'B': ['c1', 'f1'],
    'Q': ['d1'], 'K': ['e1'], 'P': ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],

    # কালো পিস (Black)
    'rr': ['a8', 'h8'], 'nn': ['b8', 'g8'], 'bb': ['c8', 'f8'],
    'qq': ['d8'], 'kk': ['e8'], 'pp': ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
}


# ৩. স্কোয়ার থেকে স্থানাঙ্ক বের করার ফাংশন
def get_square_pose(square_str):
    col_idx = ord(square_str[0]) - ord('a')  # a=0, b=1...
    row_idx = int(square_str[1]) - 1  # 1=0, 2=1...

    # সেন্টার থেকে হিসাব
    tx = BOARD_CENTER_X + (row_idx - 3.5) * SQ_SIZE
    ty = (col_idx - 3.5) * SQ_SIZE

    return transl(tx, ty, Z_GRAB)


# ৪. বোর্ড রিসেট লজিক
def reset_board():
    # স্টেশনের সব অবজেক্টের লিস্ট নেওয়া
    all_objects = RDK.ItemList(ITEM_TYPE_OBJECT)

    # কোন পিস কয়বার ব্যবহার হলো তার ট্র্যাক রাখা (যেমন: Pawn ১ থেকে ৮)
    used_counts = {name: 0 for name in initial_positions.keys()}

    print("Board Resetting...")

    for item in all_objects:
        # পিসের নাম থেকে মেইন কি-ওয়ার্ড নেওয়া (যেমন: 'P 2' থেকে 'P')
        full_name = item.Name()
        base_name = full_name.split(' ')[0]

        if base_name in initial_positions:
            count = used_counts[base_name]
            # যদি ওই টাইপের পিস এখনো সাজানোর বাকি থাকে
            if count < len(initial_positions[base_name]):
                target_sq = initial_positions[base_name][count]
                new_pose = get_square_pose(target_sq)

                # পিসটিকে সরাসরি ওই ঘরে সেট করা
                item.setPose(new_pose)

                used_counts[base_name] += 1
                print(f"Moved {full_name} to {target_sq}")

    print("Done! All pieces are in initial positions.")


if __name__ == "__main__":
    reset_board()