
import hlt

from hlt import constants

from hlt import positionals

from hlt.positionals import Direction

import random

import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is removeulated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot_v26")


logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
ship_status = {}
standing_farming_orders = {}
standing_attack_orders = {}
""" <<<Game Loop>>> """

cardinal_dir = [Direction.North, Direction.South,
                Direction.East, Direction.West]

atck_list = []


def get_safe_moves(pos):
    safe_dir = [Direction.North, Direction.South,
                Direction.East, Direction.West]

    for safe in safe_dir:
        if game_map[ship.position.directional_offset(safe)].is_occupied:
            safe_dir.remove(safe)
    return safe_dir


def get_ship_status(ship):
    if ship.id not in ship_status:
        if game.turn_number > 250 and game.turn_number < 250:
            if len(atck_list) != 0:
                return "attacking"
            else:
                return "start_exploring"
        else:
            return "start_exploring"
    elif ship.position == me.shipyard.position:
        return "start_exploring"
    elif ship_status[ship.id] == "attacking":
        return "attacking"
    elif check_return(ship):
        return "returning"
    else:
        return "exploring"


def check_return(ship):
    if ship_status[ship.id] == 'attacking':
        return False
    elif ship.is_full:
        return True
    elif ship_status[ship.id] == 'returning':
        return True
    elif game.turn_number <= 80:
        if ship.halite_amount >= 2 * constants.MAX_HALITE / 3:
            return True
    elif game.turn_number <= 180:
        if ship.halite_amount >= 3 * constants.MAX_HALITE / 4:
            return True
    elif game.turn_number <= 300:
        if ship.halite_amount >= constants.MAX_HALITE:
            return True
    elif game.turn_number <= constants.MAX_TURNS - 50:
        if ship.halite_amount >= constants.MAX_HALITE / 2:
            return True
    elif game_map.calculate_distance(ship.position, me.shipyard.position) >= constants.MAX_TURNS - game.turn_number - len(me.get_ships()) - 2:
        return True
    else:
        return False


def check_end_is_nigh():
    if game.turn_number > constants.MAX_TURNS - len(me.get_ships()) - 2 and game_map.calculate_distance(ship.position, me.shipyard.position) == 1:
        return True
    else:
        return False


def get_move_order(ship):

    if check_end_is_nigh() and ship_status[ship.id] != "attacking":
        a = game_map.get_unsafe_moves(
            ship.position, me.shipyard.position)
        next_move = a[0]
        return ship.move(next_move)

    elif ship_status[ship.id] == "attacking":
        if ship.id not in standing_attack_orders:
            standing_attack_orders[ship.id] = atck_list.pop()
            att_loc = standing_attack_orders[ship.id]
            att_pos = positionals.Position(att_loc[0], att_loc[1])
            next_move = game_map.naive_navigate(ship, att_pos)
            logging.info("target is {}.".format(att_pos))
            return ship.move(next_move)
        else:
            att_pos = positionals.Position(
                standing_attack_orders[ship.id][0], standing_attack_orders[ship.id][1])
            next_move = game_map.naive_navigate(ship, att_pos)
            return ship.move(next_move)

    elif ship_status[ship.id] == "returning" or ship.is_full:
        next_move = game_map.naive_navigate(ship, me.shipyard.position)
        if ship.id in standing_farming_orders:
            del standing_farming_orders[ship.id]

        for enemy in enemy_ships:
            if game_map.calculate_distance(ship.position, me.shipyard.position) == 1:
                if enemy.position == me.shipyard.position:
                    a = game_map.get_unsafe_moves(
                        ship.position, me.shipyard.position)
                    next_move = a[0]
                    logging.info("DEFENDING!!!")
                    return ship.move(next_move)

        if next_move == Direction.Still:
            if random.random() < 0.5:
                reroute = random.choice(cardinal_dir)

                rerouted_move = game_map.naive_navigate(
                    ship, ship.position.directional_offset(reroute))
                return ship.move(rerouted_move)
            return ship.move(next_move)
        else:
            return ship.move(next_move)

    elif ship_status[ship.id] == "exploring":
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10:
            next_move = game_map.naive_navigate(ship, get_most_halite(ship))
            if next_move == Direction.Still:
                reroute = random.choice(cardinal_dir)

                rerouted_move = game_map.naive_navigate(
                    ship, ship.position.directional_offset(reroute))
                return ship.move(rerouted_move)

            else:
                return ship.move(next_move)
        else:
            return ship.stay_still()
    elif ship_status[ship.id] == "start_exploring":
        next_move = game_map.naive_navigate(ship, get_most_halite(ship))
        if next_move == Direction.Still:
            a = get_safe_moves(ship.position)
            if len(a) != 0:
                b = random.randint(0, len(a) - 1)
                next_move = game_map.naive_navigate(
                    ship, ship.position.directional_offset(a[b]))
                return ship.move(next_move)
            else:
                next_move = random.choice(
                    [Direction.North, Direction.South, Direction.East, Direction.West])
                return ship.move(next_move)
            return ship.move(rerouted_move)
        else:
            return ship.move(next_move)
    else:
        logging.info("ERROR!!! {}.".format(
            ship_status[ship.id]))


def get_most_halite(ship):
    if ship.id in standing_farming_orders:
        if ship.position == positionals.Position(standing_farming_orders[ship.id][0], standing_farming_orders[ship.id][1]) and game_map[ship.position].halite_amount < constants.MAX_HALITE / 10:
            del standing_farming_orders[ship.id]
    if ship.id in standing_farming_orders:
        return positionals.Position(standing_farming_orders[ship.id][0], standing_farming_orders[ship.id][1],)
    else:
        a = get_efficient_halite()
        ord = True
        while ord:
            b = max(a, key=a.get)
            if b in standing_farming_orders.values():
                del a[b]
            else:
                ord = False
    pos = positionals.Position(b[0], b[1])
    standing_farming_orders[ship.id] = b
    return pos

    '''
    cardinal_dir = [Direction.North, Direction.South,
                    Direction.East, Direction.West]
    next_cardinal = Direction.West
    for car in cardinal_dir:
        if game_map[ship.position.directional_offset(car)].halite_amount > game_map[ship.position.directional_offset(next_cardinal)].halite_amount:
            next_cardinal = car
    return next_cardinal
'''


def get_efficient_halite():
    a = get_halite_dictionary()
    b = get_distance_dictionary()
    eff_dict = {}
    for key in a:
        if b[key] == 0:
            eff_dict[key] = 0
        else:
            eff_dict[key] = a[key]**2 / b[key]
    return eff_dict


def check_spawn():
    if game.turn_number <= 5 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        return command_queue.append(me.shipyard.spawn())

    elif me.halite_amount < len(me.get_ships()) * 0:
        pass

    # elif len(me.get_ships()) > 9:
        # pass

    elif game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST:
        if not game_map[me.shipyard].is_occupied:
            return command_queue.append(me.shipyard.spawn())
        else:
            a = 0
            for i in me.get_ships():
                if i.position == me.shipyard.position:
                    a += 1
                    break
            if a == 0:
                logging.info("destroying attacker.".format())
                return command_queue.append(me.shipyard.spawn())


def get_halite_dictionary():
    halite_dict = {}
    for i in range(game_map.width):
        for j in range(game_map.height):
            pos = positionals.Position(i, j)
            halite_dict[(i, j)] = game_map[pos].halite_amount
    return halite_dict


def get_attack_list():
    atck_list = []
    for i in range(game_map.width):
        for j in range(game_map.height):
            pos = positionals.Position(i, j)
            if game_map[pos].has_structure and pos != me.shipyard.position:
                atck_list.append((i, j))
    return atck_list


def get_distance_dictionary():
    dist_dict = {}
    for i in range(game_map.width):
        for j in range(game_map.height):
            pos = positionals.Position(i, j)
            dist_dict[(i, j)] = game_map.calculate_distance(
                me.shipyard.position, positionals.Position(i, j))
    return dist_dict


while True:

    game.update_frame()

    me = game.me
    game_map = game.game_map

    command_queue = []
    enemy_ships = []
    all_ships = []
    for i in range(4):
        if i == me.id:
            pass
        else:
            enemy_ships.append(game.players[i].get_ships())

    enemy_ships = [item for sublist in enemy_ships for item in sublist]

    if game.turn_number == 1:
        atck_list = get_attack_list()

    for ship in me.get_ships():
        game_map[ship].mark_unsafe(ship)

        ship_status[ship.id] = get_ship_status(ship)

        logging.info("Ship {} is {}. {} halite".format(
            ship.id, ship_status[ship.id], ship.halite_amount))
        logging.info("targets are {}.".format(
            atck_list))

        command_queue.append(get_move_order(ship))

    check_spawn()

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)


# game.players[id].get_ships()
