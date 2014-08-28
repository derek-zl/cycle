import time
import utils
from cycling import Cycling as Cycling

class LeaderboardEntry():
    '''
    Leaderboard entry data class
    '''

    def __init__(self, user=None, first_date=None, storyline=None):
        self.user       = user
        self.first_date = first_date
        self.storyline  = storyline

        self.name       = ''
        self.distance   = 0.0
        self.duration   = 0.0
        self.speed      = 0
        self.toWork     = 0
        self.fromWork   = 0
        self.nCommutes  = 0
        self.rate       = 0
        self.newuser    = False

        self.commute_days = 0
        self.work_days    = 0

        self.leaderboard_entry()
        
    def leaderboard_entry(self):
        '''
        format cycling data as leaderboard entry
        '''

        for day in self.storyline:
            
            meter2mile = 1609.34
            self.name  = self.user['first_name'] + ' ' + self.user['last_name']

            # find cycling commutes for the day
            segments = day['segments']
            cycles = utils.cycles_of_the_day(segments)
            is_commute_to_work_today = False
            is_commute_from_work_today = False

            # only count one commute per way even though there may be multiple cycling trips
            # in one direciton (considering stops), maximum two total commutes per day
            for c in cycles:
                self.distance += c.distance
                self.duration += c.duration
                if not is_commute_to_work_today and c.direction == Cycling.TO_WORK:
                    is_commute_to_work_today = True
                    self.toWork += 1
                elif not is_commute_from_work_today and c.direction == Cycling.FROM_WORK:
                    is_commute_from_work_today = True
                    self.fromWork += 1

            # find the numer of days when commuting to/from work
            if len(cycles) > 0:
                self.commute_days += 1

            # find the number of days where workplace is in the storyline
            if segments is None:
                continue
            for segment in segments:
                if utils.is_work(segment):
                    self.work_days += 1
                    break

            # find if the user started using Moves during the storyline peirod
            if self.first_date == day['date']:
                self.newuser = True

        # format cycling data
        # distance: convert from meters to miles
        # speed: mph
        # duration: convert from seconds to HH:MM:SS
        self.distance   = self.distance / meter2mile
        if self.duration > 0:
            self.speed  = self.distance / (self.duration / 3600)

        self.duration   = time.strftime('%H:%M:%S', time.gmtime(self.duration))
        self.nCommutes  = self.toWork + self.fromWork

        # round up to 0.1
        self.distance   = round(self.distance, 1)
        self.speed      = round(self.speed, 1)

        # return the cycling rate in percentage
        if self.work_days == 0:
            self.rate = 0
        else:
            self.rate = int(float(self.commute_days) / self.work_days * 100)

