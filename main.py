import defs.Robot_Control.control2Robots
import defs.Robot_Control.conveyorR2
import defs.Robot_Control.conveyorSensors
import defs.Robot_Control.detect2Objects
import defs.Robot_Control.Gripper
import defs.Robot_Control.pickAndPlaceR1
import defs.states as st 
import defs.Image_Analysis.findCircle
import defs.Image_Analysis.findSquare
import defs.Classes.Position
import time

pre_sort_size = 4
with_sorting = False
conveyor_directon = "left" # "left" or "right"
# absolute speed, no direction
conveyor_speed = 0
blocks_at_belt_count = 0

def move_one_block_to_belt(side, status):
    # Move to a block
    # Pick it up
    # Move to conveyor
    # Put the block down
    # Move to ready position

def move_block_to_final_dest_from_conveyor(side):
    # Pickup block at conveyor
    # Move to an available spot in the final destination
    # Drop of the block
    # Move back to ready position

def pre_sort_one_block(side):
    # move arm to a unsorted block
    # pick up the block
    # move to a pre-sort spot
    # put the block down
    # move arm to ready position

def post_sort_one_block(side):
    # move arm to a unsorted block (that has been placed somewhere after coming form the belt)
    # pick up the block
    # move to an availible final postion
    # put the block down
    # move arm to ready position
    
# the sensor distance when there are no blocks at the sensor
max_distance = 100
def block_at_sensor(sensor):
    return sensor["distance"] < max_distance    

# Setup the arms in the correct positions dependent on the conveyor belt direction
def prepare_to_move(from_side, to_side, with_sorting):
    conveyor_directon = to_side

    set_status(to_side, "waiting_for_conveyor")
    move_to_position(to_side, "ready" if with_sorting else "pickup")
    
    set_status(from_side, "pre_sort" if with_sorting else "move_blocks_to_belt")
    move_to_position(from_side, "ready")

# Move a block the conveyor belt if there are more blocks to be sent from this side
# Else, wait for the belt
def send_block(from_side, to_side, blocks_to_be_sent):
    conveyor_speed = 1

    if blocks_to_be_sent > 0:
        move_one_block_to_belt(from_side)
        blocks_at_belt_count += 1
    else:
        set_status(from_side, "idle")

def receive_block(pickup_side):
    set_status(pickup_side, "move_block_to_final_dest")
    conveyor_speed = 0

    move_block_to_final_dest_from_conveyor(pickup_side)
    blocks_at_belt_count -= 1

    if blocks_at_belt_count == 0:
        set_status(pickup_side, "idle")



def prepare_to_recive_block(pickup_side):
    set_status(pickup_side, "waiting_for_vonveyor")
    move_to_position(pickup_side, "pickup")
    conveyor_speed = 1

def handle_sorting(
    side, 
    status,
    not_pre_sorted_count,
    pre_sorted_count,
    to_final_dest_count
    ):

    # If it can pre sort, pre sort
    if not_pre_sorted_count < pre_sort_size and not_pre_sorted_count > 0:
        pre_sort_one_block(side)
    # If done cannot pre sort any more, prepare to move blocks to belt if is sender
    elif status is "pre_sort"
        set_status(side, "move_blocks_to_belt")
        return

    # Post sort if no other task is available
    if (not_pre_sorted_count == 0 or pre_sorted_count == pre_sort_size) and to_final_dest_count > 0:
        post_sort_one_block(side)

while True:
    # --------------------
    # Get all the sensor and and positional data:

    # to_final_dest_x - NO. blocks at the current side, but needs to be moved to the the destination area
    # at_final_dest_x - NO. blocks at the final destination area
    # to_be_sent_from_x - NO. blocks at the wrong side, wanting to be moved
    # ready_to_be_sent_from_x - Same as to_be_sent_x if no pre sorting 
    #                    - else, NO. blocks that have been pre sorted and ready to send
    # at_conveyor - NO. blocks at the conveyor belt
    to_final_dest_l, at_final_dest_l, to_be_sent_from_l, ready_to_be_sent_from_l = check_block_status("left")
    to_final_dest_r, at_final_dest_r, to_be_sent_from_r, ready_to_be_sent_from_r = check_block_status("right")

    # get program status for the arm (aka not physical status)
    status_arm_l = get_status("left")
    status_arm_r = get_status("right")

    # The actual position of the arm
    pysical_arm_position_l = get_pysical_arm_position("left")
    pysical_arm_position_r = get_pysical_arm_position("right")

    # adjust this to the actual method that gives you the sensor data
    sensor_left, sensor_middle_left, sensor_middle_right, sensor_right = get_sensor_distances()

    # -----------------------
    # Deternmine what to do based on both pysical sensor data and program status:
    
    # In the start
    # Move arms either pickup location or ready position dependent on what side has more blocks
    if status_arm_l is "idle" and status_arm_r is "idle":
        if ready_to_be_sent_from_r >= ready_to_be_sent_from_l or to_be_sent_from_r >= to_be_sent_from_l:
            prepare_to_move("right", "left", with_sorting)

        elif ready_to_be_sent_from_r < ready_to_be_sent_from_l or to_be_sent_from_r < to_be_sent_from_l:
            prepare_to_move("left", "right", with_sorting)

    # Handle sending blocks to the conveyor on the left side
    if status_arm_l is "move_blocks_to_belt" and pysical_arm_position_l is "ready":
        send_block("left", "right", ready_to_be_sent_from_l)
    
    # Handle sending blocks to the conveyor on the right side
    if status_arm_r is "move_blocks_to_belt" and pysical_arm_position_r is "ready":
        send_block("right", "left", ready_to_be_sent_from_r)

    # Handle recieving blocks on the left side
    if status_arm_l is "waiting_for_conveyor" and block_at_sensor(sensor_left):
        receive_block("left")

    # Move back to pickup location when done with the last pickup
    if status_arm_l is "move_block_to_final_dest" and pysical_arm_position_l is "ready":
        prepare_to_recive_block("left")

    # Handle recieving blocks on the right side
    if status_arm_l is "waiting_for_conveyor" and block_at_sensor(sensor_left):
        receive_block("right")

    # Move back to pickup location when done with the last pickup
    if status_arm_l is "move_block_to_final_dest" and pysical_arm_position_l is "ready":
        prepare_to_recive_block("right")
    
    # If there is nothing else to do, sort!
    if with_sorting:
        if status_arm_r is in ["pre_sort", "idle", "waiting_for_vonveyor"]:
            handle_sorting("right", status_arm_r, to_be_sent_from_r, ready_to_be_sent_from_r, to_final_dest_r)
        if status_arm_l is in ["pre_sort", "idle", "waiting_for_vonveyor"]:
            handle_sorting("left", status_arm_l, to_be_sent_from_l, ready_to_be_sent_from_l, to_final_dest_l)