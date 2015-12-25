from django.test import TestCase

from ladder.models import Player, Match
# Create your tests here

class PlayerTests(TestCase):

    def test_new_player_draw(self):
        # (1000,"11 kyu",70,155),
        p1 = Player(name='p1', games_played=1000, rating=1000)
        tp = Player(name='new player', rating=0, games_played=0) 

        # draws first 3 matches (so gets p1's rating)
        tp.drew_with(p1)
        p1.drew_with(tp)
        self.assertEqual(tp.games_played, 1)
        self.assertEqual(tp.rating, p1.rating)
        self.assertEqual(tp.rating, 1000)
        self.assertEqual(tp.display_rating(), 'no rating')
        self.assertEqual(tp.rank(), 'newbie')

        self.assertEqual(p1.games_played, 1001)

        tp.drew_with(p1)
        p1.drew_with(tp)
        self.assertEqual(tp.games_played, 2)
        self.assertEqual(tp.rating, 2000)
        self.assertEqual(tp.display_rating(), 'no rating')
        self.assertEqual(tp.rank(), 'newbie')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1002)

        tp.drew_with(p1)
        p1.drew_with(tp)
        self.assertEqual(tp.rating, 1000)
        self.assertEqual(tp.games_played, 3)
        self.assertEqual(tp.display_rating(), 1000)
        self.assertEqual(tp.rank(), '11 kyu')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1003)
        
    def test_new_player_win(self):
        # (1000,"11 kyu",70,155),
        p1 = Player(name='p1', games_played=1000, rating=1000)
        tp = Player(name='new player', rating=0, games_played=0) 

        # wims first 3 matches (so gets p1's rating + 200)
        tp.beat(p1)
        p1.lost_to(tp)
        self.assertEqual(tp.games_played, 1)
        self.assertEqual(tp.rating, 1200)
        self.assertEqual(tp.display_rating(), 'no rating')
        self.assertEqual(tp.rank(), 'newbie')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1001)

        tp.beat(p1)
        p1.lost_to(tp)
        self.assertEqual(tp.games_played, 2)
        self.assertEqual(tp.rating, 2400)
        self.assertEqual(tp.display_rating(), 'no rating')
        self.assertEqual(tp.rank(), 'newbie')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1002)

        # FIXME: reversing these lines causes it to fail. this is because the
        # check on "player.games_played" in p1.lost_to() it too late (it's
        # already been updated by the previous call to tp.beat()). The solution
        # would be for there to just be 1 method (beat, or lost_to) which
        # updates both
        p1.lost_to(tp)
        tp.beat(p1)
        self.assertEqual(tp.rating, 1200)
        self.assertEqual(tp.games_played, 3)
        self.assertEqual(tp.display_rating(), 1200)
        self.assertEqual(tp.rank(), '9 kyu')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1003)

    def test_new_player_loss(self):
        # (1000,"11 kyu",70,155),
        p1 = Player(name='p1', games_played=1000, rating=1000)
        tp = Player(name='new player', rating=0, games_played=0) 

        # wims first 3 matches (so gets p1's rating - 200)
        p1.beat(tp)
        tp.lost_to(p1)
        self.assertEqual(tp.games_played, 1)
        self.assertEqual(tp.rating, 800)
        self.assertEqual(tp.display_rating(), 'no rating')
        self.assertEqual(tp.rank(), 'newbie')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1001)

        p1.beat(tp)
        tp.lost_to(p1)
        self.assertEqual(tp.games_played, 2)
        self.assertEqual(tp.rating, 1600)
        self.assertEqual(tp.display_rating(), 'no rating')
        self.assertEqual(tp.rank(), 'newbie')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1002)

        # FIXME: reversing these lines causes it to fail. this is because the
        # check on "player.games_played" in p1.lost_to() it too late (it's
        # already been updated by the previous call to tp.beat()). The solution
        # would be for there to just be 1 method (beat, or lost_to) which
        # updates both
        tp.lost_to(p1)
        p1.beat(tp)
        self.assertEqual(tp.rating, 800)
        self.assertEqual(tp.games_played, 3)
        self.assertEqual(tp.display_rating(), 800)
        self.assertEqual(tp.rank(), '13 kyu')

        self.assertEqual(p1.rating, 1000)
        self.assertEqual(p1.games_played, 1003)

    def test_win_loss_draw(self):
        pass

        
