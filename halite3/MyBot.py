#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is removeulated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot_v14")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
ship_status = {}
""" <<<Game Loop>>> """


def get_safe_moves(pos):
    cardinal_dir = [Direction.North, Direction.South,
                    Direction.East, Direction.West]

    for car in cardinal_dir:
        if game_map[ship.position.directional_offset(car)].is_occupied:
            cardinal_dir.remove(car)
    return cardinal_dir


while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    for ship in me.get_ships():
        cardinal_dir = [Direction.North, Direction.South,
                        Direction.East, Direction.West]
        game_map[ship].mark_unsafe(ship)
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"

        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
                i = 0
                for car in cardinal_dir:
                    i += int(game_map[ship.position.directional_offset(car)].is_occupied)
                if i >= 4:
                    command_queue.append(ship.move(random.choice(
                        [Direction.North, Direction.South, Direction.East, Direction.West])))
                    continue
                else:
                    a = get_safe_moves(ship.position)
                    move = game_map.naive_navigate(
                        ship, ship.position.directional_offset(a[0]))
                    command_queue.append(ship.move(move))
                    continue
            elif game.turn_number > constants.MAX_TURNS - len(me.get_ships()) and game_map.calculate_distance(ship.position, me.shipyard.position) <= 1:
                move = game_map.get_unsafe_moves(
                    ship.position, me.shipyard.position)
                command_queue.append(ship.move(move[0]))
                continue
            else:
                move = game_map.naive_navigate(ship, me.shipyard.position)
                if move == Direction.Still:
                    reroute = random.choice(cardinal_dir)

                    move = game_map.naive_navigate(
                        ship, ship.position.directional_offset(reroute))
                    command_queue.append(ship.move(move))
                else:
                    command_queue.append(ship.move(move))
                continue
        elif game.turn_number <= 80:
            if ship.halite_amount >= constants.MAX_HALITE / 3:
                ship_status[ship.id] = "returning"
        elif game.turn_number <= 180:
            if ship.halite_amount >= constants.MAX_HALITE / 2:
                ship_status[ship.id] = "returning"
        elif game.turn_number <= 300:
            if ship.halite_amount >= constants.MAX_HALITE:
                ship_status[ship.id] = "returning"
        elif game.turn_number <= constants.MAX_TURNS - 50:
            if ship.halite_amount >= constants.MAX_HALITE / 2:
                ship_status[ship.id] = "returning"
        elif game_map.calculate_distance(ship.position, me.shipyard.position) >= constants.MAX_TURNS - game.turn_number - len(me.get_ships()):
            ship_status[ship.id] = "returning"
        else:
            ship_status[ship.id] = "returning"

        logging.info("Ship {} has {} halite.".format(
            ship.id, ship.halite_amount))
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        cardinal_dir = [Direction.North, Direction.South,
                        Direction.East, Direction.West]

        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:

            next_cardinal = Direction.West
            for car in cardinal_dir:
                if game_map[ship.position.directional_offset(car)].halite_amount > game_map[ship.position.directional_offset(next_cardinal)].halite_amount:
                    next_cardinal = car
            # command_queue.append(
                # ship.move(next_cardinal))
            next_move = game_map.naive_navigate(
                ship, ship.position.directional_offset(next_cardinal))
            command_queue.append(ship.move(next_move))
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 5 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    elif me.halite_amount < len(me.get_ships()) * 100:
        pass

    # elif len(me.get_ships()) > 9:
        # pass

    elif game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
