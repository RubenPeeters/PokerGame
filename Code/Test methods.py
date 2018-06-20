import unittest
from PokerAI import Simulator

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.testhand = {0: "CJ", 1: "SQ"}
        self.testtable = {0: "C2", 1: "S5", 2: "C8", 3: "S7", 4: "C3"}
        self.sim = Simulator(self.testhand, self.testtable, 1000)
        self.handhighcard = [[0,0],[2,1],[4,2],[6,3],[12,0]]
        self.handhighcard2 = [[0, 0], [2, 1], [4, 2], [6, 3], [11, 0]]
        self.handpair = [[2, 0], [2, 1], [4, 2], [6, 3], [12, 0]]
        self.handpair.sort()
        self.handpair.reverse()
        self.handtwopair = [[2,0],[2,1],[6,2],[6,3],[12,0]]
        self.handtwopair.sort()
        self.handtwopair.reverse()
        self.handthreeofakind = [[2, 0], [2, 1], [2, 2], [6, 3], [12, 0]]
        self.handthreeofakind.sort()
        self.handthreeofakind.reverse()
        self.handstraight = [[1, 0], [2, 1], [3, 2], [4, 3], [5, 0]]
        self.handstraightacelow = [[0, 1], [1, 2], [2, 3], [3, 0], [12, 0]]
        self.handstraight.sort()
        self.handstraight.reverse()
        self.handstraightacelow.sort()
        self.handstraightacelow.reverse()
        self.handflush = [[0, 1], [1, 1], [2, 1], [3, 1], [7, 1]]
        self.handflush.sort()
        self.handflush.reverse()
        self.handfullhouse = [[1, 0], [1, 1], [1, 2], [3, 1], [3, 5]]
        self.handfullhouse.sort()
        self.handfullhouse.reverse()
        self.handfourofakind = [[0, 0], [0, 1], [0, 2], [0, 3], [7, 1]]
        self.handfourofakind.sort()
        self.handfourofakind.reverse()
        self.handstraightflush = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
        self.handstraightflush.sort()
        self.handstraightflush.reverse()
        self.handstraightexception = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 2]]
        self.handstraightexception.sort()
        self.handstraightexception.reverse()
        self.handstraightflushacelow = [[0, 0],[1, 0], [2, 0], [3, 0], [4, 0]]
        self.handstraightflushacelow.sort()
        self.handstraightflushacelow.reverse()
        self.handroyalflush = [[8, 0], [9, 0], [10, 0], [11, 0], [12, 0]]
        self.handroyalflush.sort()
        self.handroyalflush.reverse()
    def test_highest_card(self):
        self.assertEqual(self.sim.check_highest_card(self.handhighcard,self.handhighcard2),1)

    def test_pair(self):
        self.assertEqual(self.sim.check_for_pair(self.handpair), (True , 2, [12, 6, 4]))
        self.assertEqual(self.sim.check_for_pair(self.handhighcard), (False,   13, [13, 13, 13]))

    def test_two_pair(self):
        self.assertEqual(self.sim.check_for_two_pair(self.handtwopair), (True, [2, 2], 12))
        self.assertEqual(self.sim.check_for_two_pair(self.handhighcard), (False,   [13, 13],13))

    def test_three_of_a_kind(self):
        self.assertEqual(self.sim.check_for_three_of_a_kind(self.handthreeofakind), (True, 2, [6, 12]))
        self.assertEqual(self.sim.check_for_three_of_a_kind(self.handhighcard), (False,   13, [13, 13]))

    def test_straight(self):
        self.assertEqual(self.sim.check_for_straight(self.handstraightacelow), True)
        self.assertEqual(self.sim.check_for_straight(self.handstraight), True)
        self.assertEqual(self.sim.check_for_straight(self.handhighcard), False)

    def test_flush(self):
        self.assertEqual(self.sim.check_for_flush(self.handflush), True)
        self.assertEqual(self.sim.check_for_flush(self.handhighcard), False)

    def test_full_house(self):
        self.assertEqual(self.sim.check_for_full_house(self.handfullhouse), (True, 1, 3))
        self.assertEqual(self.sim.check_for_full_house(self.handhighcard), (False,13,13))

    def test_four_of_a_kind(self):
        self.assertEqual(self.sim.check_for_four_of_a_kind(self.handfourofakind), (True, 0, 7))
        self.assertEqual(self.sim.check_for_four_of_a_kind(self.handhighcard), (False,   13, 13))

    def test_straight_flush(self):
        self.assertEqual(self.sim.check_for_straight_flush(self.handstraightflush), True)
        self.assertEqual(self.sim.check_for_straight_flush(self.handhighcard), False)

    def test_royal_flush(self):
        self.assertEqual(self.sim.check_for_royal_flush(self.handroyalflush), True)
        self.assertEqual(self.sim.check_for_royal_flush(self.handhighcard), False)

    def test_hand_to_numeric(self):
        self.assertEqual(self.sim.cardsFromDictToNumeric(self.testtable),[[6, 0], [5, 3], [3, 3], [1, 0], [0, 0]])
        self.assertEqual(self.sim.cardsFromDictToNumeric(self.testhand),[[10, 3], [9, 0]])

    def test_compare_hands(self):
        self.assertEqual(self.sim.compare_hands(self.handhighcard,self.handhighcard2),1)
        self.assertEqual(self.sim.compare_hands(self.handhighcard2,self.handhighcard), -1)
        self.assertEqual(self.sim.compare_hands(self.handpair,self.handhighcard), 1)
        self.assertEqual(self.sim.compare_hands(self.handhighcard,self.handpair), -1)
        self.assertEqual(self.sim.compare_hands(self.handtwopair,self.handpair), 1)
        self.assertEqual(self.sim.compare_hands(self.handthreeofakind,self.handtwopair), 1)
        self.assertEqual(self.sim.compare_hands(self.handstraight,self.handthreeofakind), 1)
        self.assertEqual(self.sim.compare_hands(self.handstraight,self.handstraightacelow), 1)
        self.assertEqual(self.sim.compare_hands(self.handstraightacelow,self.handthreeofakind), 1)
        self.assertEqual(self.sim.compare_hands(self.handflush,self.handstraight), 1)
        self.assertEqual(self.sim.compare_hands(self.handfullhouse,self.handflush), 1)
        self.assertEqual(self.sim.compare_hands(self.handfourofakind,self.handfullhouse), 1)
        self.assertEqual(self.sim.compare_hands(self.handstraightflush,self.handfourofakind), 1)
        self.assertEqual(self.sim.compare_hands(self.handroyalflush,self.handstraightflush), 1)
        self.assertEqual(self.sim.compare_hands(self.handtwopair, self.handpair), 1)
        self.assertEqual(self.sim.compare_hands(self.handstraightflushacelow, self.handstraightexception), 1)


if __name__ == '__main__':
    unittest.main()
