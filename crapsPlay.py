import random
import os

TYPE_EVEN_WAGER = "Even wager"
TYPE_MARTINGALE = "Martingale system"
TYPE_REVERSE_MARTINGALE = "Reverse Martingale system"

net_amount = 1000
prev_bet = 100
first_roll_value = 0

win_outcomes = [7, 11]
lose_outcomes = [2, 3, 12]
point_outcomes = [4, 5, 6, 8, 9, 10]


def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)


def play_game(_type):
    global first_roll_value
    global prev_bet
    global net_amount
    global TYPE_EVEN_WAGER
    global TYPE_MARTINGALE
    global TYPE_REVERSE_MARTINGALE
    global win_outcomes
    global lose_outcomes
    global point_outcomes

    r = roll_dice()
    if r in win_outcomes:
        if first_roll_value:
            # Expecting a point value. Game lost.
            if type is TYPE_MARTINGALE:
                bet_amount = 2*prev_bet
            else:
                bet_amount = 100
            net_amount = net_amount - bet_amount
        else:
            # Come-out role is a win. Game won.
            if type is TYPE_REVERSE_MARTINGALE:
                bet_amount = 2*prev_bet
            else:
                bet_amount = 100
            net_amount = net_amount + bet_amount
        return
    elif r in lose_outcomes:
        if not first_roll_value:
            # Come-out roll is in losing set. Game lost.
            if type is TYPE_MARTINGALE:
                    bet_amount = 2*prev_bet
            else:
                bet_amount = 100
            net_amount = net_amount-bet_amount
            return
        else:
            # Roll dice again for point roll
            play_game(_type)
    else:
        # Come-out role is a point value. Check if point is rolled again.
        if r is first_roll_value:
            # Point repeated. Game won.
            if _type is TYPE_REVERSE_MARTINGALE:
                bet_amount = 2*prev_bet
            else:
                bet_amount = 100
            net_amount = net_amount + bet_amount
            first_roll_value = 0
            return
        else:
            # Frist role is a point value. Keep track of it for the next roll.
            if not first_roll_value:
                first_roll_value = r
            play_game(_type)


def play_round(_type):

    global first_roll_value
    global prev_bet
    global net_amount
    global fp

    # Reset the first roll value to 0 before playing the next round.
    first_roll_value = 0
    prev_bet = 100
    net_amount = 1000

    cnt = 0
    while cnt < 20 and net_amount:
        cnt = cnt+1
        first_roll_value = 0
        play_game(_type)

    if net_amount:
        """ count would be 21 when exiting the loop due
        to max game limit. Re assign it back to 20 for display. """
        cnt = 20

    fp.write(
        "Strategy : %s  |  Games played : %s  | Ending balance : %s \n\n"
        % (_type, cnt, net_amount)
    )

if __name__ == "__main__":
    fp = open(os.path.join(os.getcwd() + '/output1.txt'), 'w+')
    for i in range(5):
        fp.write("Round %d  \n" % (i+1))
        play_round(TYPE_EVEN_WAGER)
        play_round(TYPE_MARTINGALE)
        play_round(TYPE_REVERSE_MARTINGALE)
