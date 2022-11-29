import socket
import random

headerSize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 6666))

playerIn = True
dealerIn = True
Msg = ''
# deck of cards/ player dealer hand
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
        2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
        2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
playerHand = []
dealerHand = []


# deal the cards
def dealCard(turn):
    card = random.choice(deck)  # assigns a random card from the deck
    turn.append(card)  # allows for card to go into whichever players hand is up
    deck.remove(card)  # remove drawn card from active deck


# calculate total of each hand
def total(hand):
    total = 0
    ace_11s = 0
    for card in hand:
        if card in range(11):
            total += card
        elif card in ['J', 'K', 'Q']:
            total += 10
        else:
            total += 11
            ace_11s += 1
    while ace_11s and total > 21:
        total -= 10
        ace_11s -= 1
    return total


# check for winner
def revealDealerhand():
    if len(dealerHand) == 2:
        return dealerHand[0]
    elif len(dealerHand) > 2:
        return dealerHand[0], dealerHand[1]


# game loop
Quit = False
while not Quit:
    playerHand = []
    dealerHand = []
    playerIn = True
    dealerIn = True

    for i in range(2):
        dealCard(dealerHand)
        dealCard(playerHand)
    i = 0
    while playerIn or dealerIn:
        print(f"Dealer has {revealDealerhand()} and X")
        print(f"You have {playerHand} for a total of {total(playerHand)}\n")
        if playerIn:
            standOrHit = input("1: Stand\n2:Hit\n")
        if total(dealerHand) > 16:
            dealerIn = False
        else:
            dealCard(dealerHand)
        if standOrHit == '1':
            playerIn = False
        else:
            dealCard(playerHand)
        if total(playerHand) >= 21:
            break
        elif total(dealerHand) >= 21:
            break
    if total(playerHand) == 21:
        print(f"\nYou have {playerHand} for a total of {total(playerHand)} resulting in blackjack, Player Wins")
    elif total(dealerHand) == 21:
        print(f"\nThe dealer has {dealerHand} for a total of {total(dealerHand)} resulting in blackjack, Dealer Wins")
    elif total(playerHand) > 21:
        print(f"\nYou have {playerHand} for a total of {total(playerHand)} resulting in a bust, Dealer wins")
    elif total(dealerHand) > 21:
        print(f"\nThe Dealer has {dealerHand} for a total of {total(dealerHand)} resulting in a bust, Player wins")
    elif 21 - total(dealerHand) < 21 - total(playerHand):
        print(
            f"\nYou have {playerHand} for a total of {total(playerHand)} and the dealer has {dealerHand} for a total "
            f"of {total(dealerHand)}, Dealer Wins")
    elif 21 - total(dealerHand) > 21 - total(playerHand):
        print(
            f"\nYou have {playerHand} for a total of {total(playerHand)} and the dealer has {dealerHand} for a total "
            f"of {total(dealerHand)}, Player Wins")
    elif playerHand == dealerHand:
        print(f"\nYou have {playerHand} for a total of {total(playerHand)} and the dealer has {dealerHand} for a total "
              f"of {total(dealerHand)}, this results in a push hand, no one wins!")

    s.send(str(total(playerHand)).encode())
    oppHand = s.recv(2048).decode()
    print("\nOther player's hand: " + oppHand)

    while Msg != "Goodluck":
        Msg = s.recv(2048).decode()
        print("\nUser message: " + Msg)

        Msg = input("\nYour message(type Goodluck to end): ")
        s.send(Msg.encode())
    Msg = ''

    Choice = input("Do you want to Quit? Y/N")
    if Choice == "Y":
        Quit = True
    elif Choice == "N":
        Quit = False
# msg = input("->")
#
# while msg.lower().strip() != "bye":
#     s.send(msg.encode())
#     msg = s.recv(2048).decode()
#
#     print("Received from server: " + msg)
#
#     msg = input("->")
#
# s.close()
