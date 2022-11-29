import socket
import random

headerSize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6666))
s.listen(4)
newMsg = ''

clientSocket, address = s.accept()

playerIn = True
dealerIn = True
# deck of cards/ player dealer hand
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
        2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
        2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
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
        print(f"\nYou have {playerHand} for a total of {total(playerHand)} resulting in blackjack, Player Wins\n")
    elif total(dealerHand) == 21:
        print(f"\nThe dealer has {dealerHand} for a total of {total(dealerHand)} resulting in blackjack, Dealer Wins\n")
    elif total(playerHand) > 21:
        print(f"\nYou have {playerHand} for a total of {total(playerHand)} resulting in a bust, Dealer wins\n")
    elif total(dealerHand) > 21:
        print(f"\nThe Dealer has {dealerHand} for a total of {total(dealerHand)} resulting in a bust, Player wins\n")
    elif 21 - total(dealerHand) < 21 - total(playerHand):
        print(
            f"\nYou have {playerHand} for a total of {total(playerHand)} and the dealer has {dealerHand} for a total "
            f"of {total(dealerHand)}, Dealer Wins\n")
    elif 21 - total(dealerHand) > 21 - total(playerHand):
        print(
            f"\nYou have {playerHand} for a total of {total(playerHand)} and the dealer has {dealerHand} for a total "
            f"of {total(dealerHand)}, Player Wins\n")
    elif playerHand == dealerHand:
        print(f"\nYou have {playerHand} for a total of {total(playerHand)} and the dealer has {dealerHand} for a total "
              f"of {total(dealerHand)}, this results in a push hand, no onw wins!")


    clientSocket.send(str(total(playerHand)).encode())
    oppHand = clientSocket.recv(2048).decode()
    print("\nOther players hand: " + oppHand)

    while newMsg != "Goodluck":
        newMsg = input("\nYour message(type Goodluck to end): ")
        clientSocket.send(newMsg.encode())

        newMsg = clientSocket.recv(2048).decode()
        print("\nUser message: " + newMsg)
    newMsg = ''

    Choice = input("\nDo you want to Quit? Y/N")
    if Choice == "Y":
        Quit = True
    elif Choice == "N":
        Quit = False
# while newMsg.lower().strip() != "bye":
#     newMsg = clientSocket.recv(2048).decode()
#
#     print("From connected user: " + str(newMsg))
#     newMsg = input("->")
#     clientSocket.send(newMsg.encode())
#     if newMsg == 'bye':
#         print("bye")
#         s.close()
# s.close()
