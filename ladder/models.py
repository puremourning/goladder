from django.db import models
from django.core.urlresolvers import reverse

import math

# there is almost certainly a more elegant way of doing this...
rating_table = (
    # rating, rank, "K", "a" (see http://senseis.xmp.net/?EGFRatingSystem)
    (2700,"7 dan",10,70),
    (2600,"6 dan",11,75),
    (2500,"5 dan",13,80),
    (2400,"4 dan",15,85),
    (2300,"3 dan",18,90),
    (2200,"2 dan",21,95),
    (2100,"1 dan",24,100),
    (2000,"1 kyu",27,105),
    (1900,"2 kyu",31,110),
    (1800,"3 kyu",35,115),
    (1700,"4 kyu",39,120),
    (1600,"5 kyu",43,125),
    (1500,"6 kyu",47,130),
    (1400,"7 kyu",51,135),
    (1300,"8 kyu",55,140),
    (1200,"9 kyu",60,145),
    (1100,"10 kyu",65,150),
    (1000,"11 kyu",70,155),
    (900,"12 kyu",75,160),
    (800,"13 kyu",80,165),
    (700,"14 kyu",85,170),
    (600,"15 kyu",90,175),
    (500,"16 kyu",95,180),
    (400,"17 kyu",100,185),
    (300,"18 kyu",105,190),
    (200,"19 kyu",110,195),
    (100,"20 kyu",116,200),
    (0,  "21 kyu",121,205),
    (-100,"22 kyu",129,230),
    (-200,"23 kyu",138,235),
    (-300,"24 kyu",145,245),
)

class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rating = models.IntegerField(db_index=True)
    games_played = models.IntegerField(default=0)

    def get_rating_params(self):
        for t in rating_table:
            if self.rating >= t[0] :
                return t

        # wat.
        return (-999,"no rating", 999, 999)
    
    def expected_score_vs(self, player, a):
        # from http://senseis.xmp.net/?EGFRatingSystem;
        # calculate the expected score vs another player
        return 1.0 / (1 + math.e ** ((player.rating - self.rating) / a))

    def _adjust_rating(self, exp_score, score, K):
        # also http://senseis.xmp.net/?EGFRatingSystem;
        # calculate the new rating based on a score vs expected
        self.rating += K * (score - exp_score)

    def incorporate_rating(self, rating, game_number):
        # before we have 3 games under our belt we don't have a rating, so we
        # accumulate score (calculated oddly as:
        #  win = opponent rating + 200
        #  draw = opponent rating
        #  loss = opponent rating - 200)
        #
        # until we have 3, at which point we take the mean
        self.rating += rating

        if game_number == 3:
            # not self.games_played, as this hasn't been updated yet
            self.rating /= game_number

    def lost_to(self, player):
        if player.games_played < 3:
            # until a player has a rating, they don't affect our score (in
            # particular because at this point their score is being accumulated)
            pass
        elif self.games_played >= 3:
            # ok we both have ratings, update
            (rating, rank, K, a) = self.get_rating_params()
            self._adjust_rating(self.expected_score_vs(player, a), 0, K)
        else:
            # we don't have a rating yet, accumulate until we can calculate one
            self.incorporate_rating(player.rating - 200,
                                    self.games_played + 1)

        self.games_played += 1

    def beat(self, player):
        if player.games_played < 3:
            # until a player has a rating, they don't affect our score
            pass
        elif self.games_played >= 3:
            # ok we both have ratings, update
            (rating, rank, K, a) = self.get_rating_params()
            self._adjust_rating(self.expected_score_vs(player, a), 1, K)
        else:
            # we don't have a rating yet, accumulate until we can calculate one
            self.incorporate_rating(player.rating + 200,
                                    self.games_played + 1)

        self.games_played += 1

    def drew_with(self, player):
        if player.games_played < 3:
            # until a player has a rating, they don't affect our score
            pass
        elif self.games_played >= 3:
            # ok we both have ratings, update
            (rating, rank, K, a) = self.get_rating_params()
            self._adjust_rating(self.expected_score_vs(player, a), 0.5, K)
        else:
            # we don't have a rating yet, accumulate until we can calculate one
            self.incorporate_rating(player.rating, self.games_played + 1)

        self.games_played += 1

    def __unicode__(self):
        return self.name

    def display_rating(self):
        if self.games_played < 3:
            return "no rating"
        else:
            return self.rating

    def rank(self):
        if self.games_played < 3:
            return 'newbie'

        return self.get_rating_params()[1]


class Match(models.Model):

    class Result:
        WHITE_WIN = 'W'
        BLACK_WIN = 'B'
        DRAW = 'D'

    class ResultType:
        RESIGNATION = 'R'
        TIME_OUT    = 'O'
        TERRITORY   = 'T'
        NO_RESULT   = ''

    # the actual fields
    black = models.ForeignKey(Player, related_name='+')
    white = models.ForeignKey(Player, related_name='+')
    date  = models.DateTimeField()
    komi  = models.FloatField()
    handicap = models.IntegerField()
    result = models.CharField(max_length=1, choices=(
        (Result.WHITE_WIN, 'White win'),
        (Result.BLACK_WIN, 'Black win'),
        (Result.DRAW,      'Draw - match abandoned'),
    ))
    result_type = models.CharField(max_length=1, choices=(
        (ResultType.RESIGNATION, 'Resignation'),
        (ResultType.TIME_OUT,    'Time out'),
        (ResultType.TERRITORY,   'Territory'),
        (ResultType.NO_RESULT,   'n/a'),
    ),blank=True,default=ResultType.TERRITORY)
    score_black = models.FloatField(null=True,blank=True)
    score_white = models.FloatField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse('match', 
                        urlconf='ladder.urls',
                        kwargs={'pk': self.pk})

    def __unicode__(self):
        return (self.black.name 
                + ' (B) vs ' 
                + self.white.name 
                + ' (W) on ' 
                + self.date.strftime('%Y-%m-%d'))

