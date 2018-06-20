import copy
import random
# CARD = list of 2, card[0] = value, card[1] = suit
# HAND = list of cards aka list of lists

#selector
# hand[x][y] x = which card      y = value or suit

###ALL METHODS:
# cardsFromDictToNumeric(self, cards):
# best_five(self, hand, table):
# compare_hands(self,hand1,hand2):
# check_highest_card(self, hand1, hand2):
# check_for_pair(self, hand):
# check_for_two_pair(self, hand):
# check_for_three_of_a_kind(self, hand):
# check_for_straight(self, hand):
# check_for_flush(self, hand):
# check_for_full_house(self, hand):
# check_for_four_of_a_kind(self, hand):
# check_for_straight_flush(self, hand):
# check_for_royal_flush(self, hand):
# winner_straight(self, hand1, hand2):
# calculate_chance(self, amount):


# Class to simulate a number of games to get a reasonable winning chance for each hand
class Simulator:
    def __init__(self,hand,table,amount):
        self.chance = 0
        self.hand = copy.deepcopy(hand)
        self.table = copy.deepcopy(table)
        self.amount = amount
        self.cards = {
            1: 'CA', 2: 'DA', 3: 'HA', 4: 'SA',
            5: 'C2', 6: 'D2', 7: 'H2', 8: 'S2',
            9: 'C3', 10: 'D3', 11: 'H3', 12: 'S3',
            13: 'C4', 14: 'D4', 15: 'H4', 16: 'S4',
            17: 'C5', 18: 'D5', 19: 'H5', 20: 'S5',
            21: 'C6', 22: 'D6', 23: 'H6', 24: 'S6',
            25: 'C7', 26: 'D7', 27: 'H7', 28: 'S7',
            29: 'C8', 30: 'D8', 31: 'H8', 32: 'S8',
            33: 'C9', 34: 'D9', 35: 'H9', 36: 'S9',
            37: 'CT', 38: 'DT', 39: 'HT', 40: 'ST',
            41: 'CJ', 42: 'DJ', 43: 'HJ', 44: 'SJ',
            45: 'CQ', 46: 'DQ', 47: 'HQ', 48: 'SQ',
            49: 'CK', 50: 'DK', 51: 'HK', 52: 'SK'
        }



        # hand is a list of lists containing a list of the rank and a list of the suit

        # check for correct input for hand
        '''    niet nodig want de input zal altijd uit een hardgecodeerde dict komen dus kan niet fout zijn
        def correct_input(self):
        for i in self.hand:
            if self.hand.count(i) > 1:
                return False
        return True
        '''

        ''' VERLOOP VAN CODEREN?:
        eerst moet hij de handen kunnen omzetten naar numerieke waarden
        dan kan je beginnen met random handen/kaarten mee te geven om te testen
        dan testen en methode per methode proberen te maken
        '''

    # Aangepast en afgewerkt
    # converts hand to numeric values and sorts based on rank
    # important to also sort the hands for for example checking for royal flush
    # INPUT: 1: 'CA', 30: 'D8'
    # OUTPUT  [12,0], [6,1]     [NUMBER, SUIT]
    def addValuesToTable(self):
        while len(self.table) < 5:
            lengthtable = len(self.table)
            extraC = 5 - lengthtable
            for i in range(extraC):
                r = random.randint(1,52)
                while self.cards[r] in self.table or self.cards[r] in self.hand:
                    r = random.randint(1, 52)
                self.table[i+lengthtable] = self.cards[r]

    def cardsFromDictToNumeric(self, cards):
        # cards is a dict
        numeric_cards = []

        card_number = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6,
                       "9": 7, "10": 8, "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12, "X": -1}
        card_suit = {"C": 0, "D": 1, "H": 2, "S": 3, "X": -1}

        for el in cards.values():
            # suits fixen
            for key, val in card_suit.items():
                if el[0] == key:
                    suitResult = val
                    break

            # number fixen
            number = el[1:]
            for key, val in card_number.items():
                if number == key:
                    numberResult = val
                    break

            numeric_cards.append([numberResult, suitResult])

        numeric_cards.sort()
        numeric_cards.reverse()
        return numeric_cards



    # gives the best combination of five cards out of a max of 7
    # needs a method that compares hands

    def best_five(self, hand, table):
        #
        # Copy of the table and sort it
        #
        currentbest = copy.deepcopy(table)
        currentbest.sort()
        currentbest.reverse()
        #
        # Compare current best to five cards including only one player card
        # All possible options with the table cards and one specific card from the hand
        #
        for playerCard in range(2):
            for tableCard in range(5):
                comparehand = copy.deepcopy(table)
                comparehand[tableCard] = hand[playerCard]
                comparehand.sort()
                comparehand.reverse()
                if self.compare_hands(currentbest, comparehand) == -1:
                    currentbest = copy.deepcopy(comparehand)
        #
        # Compare current best to five cards including both player cards
        # All possible options with the table cards and both cards from the hand
        #
        for firstCard in range(5):
            for secondCard in range(firstCard + 1, 5):
                #
                # Make copy of the table cards and make a hand with 5 cards including both cards
                # Starting from replacing the first card with one player card, and then consecutively replacing
                # all other cards with the second card. Afterwards moving the first card in that players hand to the
                # second spot on the table.
                #
                comparehand = copy.deepcopy(table)
                comparehand[firstCard] = hand[0]
                comparehand[secondCard] = hand[1]
                comparehand.sort()
                comparehand.reverse()
                if self.compare_hands(currentbest, comparehand) == -1:
                    currentbest = copy.deepcopy(comparehand)
        return currentbest


    # compares two hands
    # needs multiple comparing methods
    def compare_hands(self,hand1,hand2):
        # Royal flush is so unlikely that it is irrelevant to check, can also be checked with combination of winner_straight(hand1,hand2) and check_for_straight_flush

        # straight flush

        if self.check_for_straight_flush(hand1):
            if self.check_for_straight_flush(hand2):
                return (self.winner_straight(hand1, hand2))
            else:
                return 1
        elif self.check_for_straight_flush(hand2):
            return -1

        # four of a kind

        result1 = self.check_for_four_of_a_kind(hand1)
        result2 = self.check_for_four_of_a_kind(hand2)
        if result1[0] == 1:
            if result2[0] == 1:
                if result1[1] > result2[1]:
                    return 1
                elif result1[1] < result2[1]:
                    return -1
                elif result1[2] > result2[2]:
                    return 1
                elif result1[2] < result2[2]:
                    return -1
                else:
                    return 0
            else:
                return 1
        elif result2[0] == 1:
            return -1

        # full house

        result1 = self.check_for_full_house(hand1)
        result2 = self.check_for_full_house(hand2)
        if result1[0] == 1:
            if result2[0] == 1:
                if result1[1] > result2[1]:
                    return 1
                elif result1[1] < result2[1]:
                    return -1
                elif result1[2] > result2[2]:
                    return 1
                elif result1[2] < result2[2]:
                    return -1
                else:
                    return 0
            else:
                return 1
        elif result2[0] == 1:
            return -1

        # flush

        if self.check_for_flush(hand1):
            if self.check_for_flush(hand2):
                return (self.check_highest_card(hand1, hand2))
            else:
                return 1
        elif self.check_for_flush(hand2):
            return -1

        # straight

        if self.check_for_straight(hand1):
            if self.check_for_straight(hand2):
                temp = self.winner_straight(hand1, hand2)
                return temp
            else:
                return 1
        elif self.check_for_straight(hand2):
            return -1

        # three of a kind


        result1 = self.check_for_three_of_a_kind(hand1)
        result2 = self.check_for_three_of_a_kind(hand2)
        if result1[0] == 1:
            if result2[0] == 1:
                if result1[1] > result2[1]:
                    return 1
                elif result1[1] < result2[1]:
                    return -1
                elif result1[2] > result2[2]:
                    return 1
                elif result1[2] < result2[2]:
                    return -1
                else:
                    return 0
            else:
                return 1
        elif result2[0] == 1:
            return -1

        # two pair

        result1 = self.check_for_two_pair(hand1)
        result2 = self.check_for_two_pair(hand2)
        if result1[0] == 1:
            if result2[0] == 1:
                if result1[1] > result2[1]:
                    return 1
                elif result1[1] < result2[1]:
                    return -1
                elif result1[2] > result2[2]:
                    return 1
                elif result1[2] < result2[2]:
                    return -1
                else:
                    return 0
            else:
                return 1
        elif result2[0] == 1:
            return -1

        # pair

        result1 = self.check_for_pair(hand1)
        result2 = self.check_for_pair(hand2)
        if result1[0] == 1:
            if result2[0] == 1:
                if result1[1] > result2[1]:
                    return 1
                elif result1[1] < result2[1]:
                    return -1
                elif result1[2] > result2[2]:
                    return 1
                elif result1[2] < result2[2]:
                    return -1
                else:
                    return 0
            else:
                return 1
        elif result2[0] == 1:
            return -1
        return (self.check_highest_card(hand1, hand2))



    #afgewerkt en uitgetest
    #hand1 en hand2 zijn dictionaries
    #werkt zoals een compareTo in java
    # This should take a numeric version of the hand as input, the first two lines are unnecessary
    def check_highest_card(self, hand1, hand2):

        #hand1Numeric = self.cardsFromDictToNumeric(hand1)
        #hand2Numeric = self.cardsFromDictToNumeric(hand2)

        #hand1Highest = max(hand1)
        #hand2Highest = max(hand2)

        #if hand1Highest > hand2Highest:
        #    return 1
        #elif hand1Highest < hand2Highest:
        #    return -1
        #else:
        #    return 0
        hand1_rank = [hand1[0][0],hand1[1][0],hand1[2][0],hand1[3][0],hand1[4][0]]
        hand2_rank = [hand2[0][0],hand2[1][0],hand2[2][0],hand2[3][0],hand2[4][0]]
        #
        # Compare
        #
        if hand1_rank > hand2_rank:
            return 1
        elif hand1_rank < hand2_rank:
            return -1
        return 0

    # Checks for a pair
    #
    # Check if there's two cards that have the same number, and the rest doesn't
    #
    #### SCRATCHED: Should return rank of the paired card and the rest of the cards, True/False might be necessary but atm i think it's useless
    #
    # Returns True/False to signify if a pair was found + value of the pair and a list of the values of the other cards
    #
    ####SCRATCHED: 13 stands for not found (12 is highest value for a card) --> if 13 is returned means its False, all other variables means True
    # 13 is a garbage value
    # True and False are relevant, makes the implementation of the compare_hands method a lot easier.
    #
    # Don't know if the garbage values are relevant, pretty sure they aren't
    #
    def check_for_pair(self, hand):
        hand_numbers = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
        for pair_card in range(13):
            if hand_numbers.count(pair_card) == 2:
                for irrelevant1 in range(13):
                    if hand_numbers.count(irrelevant1) == 1:
                        for irrelevant2 in range(irrelevant1 + 1, 13):
                            if hand_numbers.count(irrelevant2) == 1:
                                for irrelevant3 in range(irrelevant2 + 1, 13):
                                    if hand_numbers.count(irrelevant3) == 1:
                                        return True, pair_card, [irrelevant3, irrelevant2, irrelevant1]
        return False,   13, [13, 13, 13]

    # checks for two pair
    #
    # Check if there's two times two cards that have the same number, and the rest doesn't
    #
    # Returns True/False to signify if two pair were found + a list of the pair numbers and the irrelevant card
    #
    # True and False are relevant, makes the implementation of the compare_hands method a lot easier.
    #
    # Don't know if the garbage values are relevant, pretty sure they aren't
    #
    def check_for_two_pair(self, hand):
        hand_numbers = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
        for lowest_pair_card in range(13):
            if hand_numbers.count(lowest_pair_card) == 2:
                for highest_pair_card in range(lowest_pair_card + 1,13):
                    if hand_numbers.count(highest_pair_card) == 2:
                        for irrelevant in range(13):
                            if hand_numbers.count(irrelevant) == 1:
                                return True, [lowest_pair_card, highest_pair_card], irrelevant
        return False,   [13, 13],13

    # checks for three of a kind
    #
    # Check if there's three cards with the same number and the other two are not the same
    #
    # Returns True/False to signify if a pair was found + value of the pair and a list of the values of the other cards
    #
    # True and False are relevant, makes the implementation of the compare_hands method a lot easier.
    #
    # Don't know if the garbage values are relevant, pretty sure they aren't
    #
    def check_for_three_of_a_kind(self, hand):
        hand_numbers = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
        for triple_card in range(13):
            if hand_numbers.count(triple_card) == 3:
                for lowest_irrelevant in range(13):
                    if hand_numbers.count(lowest_irrelevant) == 1:
                        for highest_irrelevant in range(lowest_irrelevant + 1, 13):
                            if hand_numbers.count(highest_irrelevant) == 1:
                                return True, triple_card, [lowest_irrelevant, highest_irrelevant]
        return False,   13, [13, 13]

    # checks for straight
    #
    # Returns True if hand is straight, otherwise returns False
    # Here, the suits are irrelevant so only test for card numbers
    # In the elif statement, we test for an Ace Low Straight
    #

    #hand zijn 5 kaarten
    def check_for_straight(self, hand):
        if hand[0][0] == (hand[1][0] + 1) == (hand[2][0] + 2) == (hand[3][0] + 3) == (hand[4][0] + 4):
            return True
        elif (hand[0][0] == 12) and (hand[1][0] == 3) and (hand[2][0] == 2) and (hand[3][0] == 1) and (hand[4][0] == 0):
            return True
        return False

    # checks for flush
    #
    # Returns True if hand is flush, otherwise returns False
    # Here, the card numbers are irrelevant so only test for suit of the cards
    #cc
    def check_for_flush(self, hand):
        hand_suit = [hand[0][1], hand[1][1], hand[2][1], hand[3][1], hand[4][1]]
        for suited_card in range(4):
            if hand_suit.count(suited_card) == 5:
                return True
        return False

    # checks for full house
    #
    # Returns True if there is a fullhouse + first the triple card and then the double card
    #
    def check_for_full_house(self, hand):
        hand_numbers = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
        for triple_card in range(13):
            if hand_numbers.count(triple_card) == 3:
                for double_card in range(13):
                    if hand_numbers.count(double_card) == 2:
                        return True, triple_card, double_card
        return False,   13, 13

    # checks for four of a kind
    #
    # Looks a lot like the three_of_a_kind method
    # True if there is a four of a kind + number of the quad card and the number of the irrelevant card
    #
    def check_for_four_of_a_kind(self, hand):
        hand_numbers = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
        for quad_card in range(13):
            if hand_numbers.count(quad_card) == 4:
                for irrelevant in range(13):
                    if hand_numbers.count(irrelevant) == 1:
                        return True, quad_card, irrelevant
        return False,   13, 13

    # checks for straight flush
    #
    # Checking for a straight flush is just checking for a flush and a straight.
    #
    def check_for_straight_flush(self, hand):
        if self.check_for_flush(hand) and self.check_for_straight(hand):
            return True
        return False

    # checks for royal flush
    #
    # This checks for a royal flush
    # Might be pretty useless because the chance of this happening is 0.000154%	or 1 in 649 739
    # And in essence, this is a form of a straight flush
    #
    def check_for_royal_flush(self, hand):
        hand_numbers = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
        if self.check_for_straight_flush(hand):
            if hand_numbers[0] == 12:
                return True
        return False

    # checks winner in case of two straights
    # Return 1 if hand1 is higher
    # Return -1 if hand2 is higher
    # Return 0 if equal
    #
    # Compare second card first (to account for Ace low straights)
    # Example: Ace low straight (1) and a 8 high straight(2) --> second card for (1) will be 5 and for (2) 7 thus meaning that the second one wins
    # If equal, we could have Ace low straight, so compare first card.
    # If first card is Ace, that is the lower straight
    #

    def winner_straight(self, hand1, hand2):

        if hand1[1][0] > hand2[1][0]:
            return 1
        elif hand1[1][0] < hand2[1][0]:
            return -1
        elif hand1[0][0] > hand2[0][0]:
            return -1
        elif hand1[0][0] < hand2[0][0]:
            return 1
        return 0

    def calculate_chance(self):
        self.addValuesToTable()
        numericHand = self.cardsFromDictToNumeric(self.hand)
        numericTable = self.cardsFromDictToNumeric(self.table)
        bestNumericHand = self.best_five(numericHand,numericTable)
        wins = 0
        ties = 0
        losses = 0
        for i in range(self.amount):
            r1 = random.randint(1,52)
            r2 = random.randint(1,52)
            while r2 == r1:
                r2 = random.randint(1, 52)
            randomHand = {0 : self.cards[r1],1 : self.cards[r2]}
            randomNumericHand = self.cardsFromDictToNumeric(randomHand)
            bestRandomNumericHand = self.best_five(randomNumericHand,numericTable)
            if self.compare_hands(bestNumericHand, bestRandomNumericHand) == 1:
                wins += 1
            elif self.compare_hands(bestNumericHand, bestRandomNumericHand) == 0:
                ties += 1
                wins += 0.5
            elif self.compare_hands(bestNumericHand, bestRandomNumericHand) == -1:
                losses += 1

        self.chance = wins/self.amount

        return self.chance




# This is the form the hand and table dicts should have
'''testhand = {0: "ST", 1: "CQ"}
testtable = {0: "C7", 1: "D5", 2: "DQ", 3: "H7", 4: "C5"}
dealer = Simulator(testhand, testtable, 5000)
testhand = dealer.cardsFromDictToNumeric(testhand)
testtable = dealer.cardsFromDictToNumeric(testtable)
print(dealer.check_for_two_pair(testtable))
print(dealer.best_five(testhand,testtable))'''

#print(dealer.cardsFromDictToNumeric(testhand))
