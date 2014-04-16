from django.db import models
from datetime import datetime
from django.db.models import Avg
import math


class Golfer(models.Model):
    last_name = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True, default="test")
    phone = models.CharField(max_length=128, null=True, blank=True)
    phone_alt = models.CharField(max_length=128, null=True, blank=True)
    def_handicap = models.IntegerField(default=0)
    handicap = models.IntegerField(default=0, null=True, blank=True)
    mod_date = models.DateField(auto_now=True)

    @property
    def total_points(self):
        # Sum the points for a golfer for the current year
        total = 0.0
        cur_year = datetime.now().year
        rounds = Round.objects.all().filter(date__year=cur_year, golfer_id=self.id)
        for r in rounds:
            total += r.points

        return total

    @property
    def name(self):
        full_name = self.first_name + " " + self.last_name

        return full_name

    @property
    def adj_points(self):
        # Sum the points for a golfer for the current year
        total = 0.0
        cur_year = datetime.now().year
        rounds = Round.objects.all().filter(date__year=cur_year, golfer_id=self.id)
        for r in rounds:
            total += r.mod_points

        return total

    @property
    def avg_score(self):
        # Returns golfer's average for the year
        rounds = Round.objects.all().filter(date__year=datetime.now().year, golfer_id=self)
        total = 0
        count = 0
        for r in rounds:
            total += int(r.score)
            count += 1
        if not total or not count:
            r_avg = 0
        else:
            r_avg = total / count

        return r_avg

    @property
    def num_rds(self):
        # count the number of rounds for a golfer by year
        ##### THIS IS HOW WE AGGREGATE THINGS!
        total = Round.objects.filter(date__year=datetime.now().year, golfer_id=self).count()

        if total:
            return total
        else:
            return 0

    #def save(self):
        #if not self.handicap:
            #self.handicap = self.def_handicap
        # year = datetime.now().year
        # scores = []
        # rounds = Round.objects.filter(golfer_id=self.pk).order_by('week_num')
        # # golfer = Golfer.objects.get(self)
        # for r in rounds:
        #     if r.date.year == year:
        #         c = Course.objects.get(name=r.course_id)
        #         # Year is the same. Get the correct number of rounds
        #         calc = (r.score - c.rating)
        #         scores.append(calc)
        #
        # scores.sort()
        #
        # temp_h = []
        #
        # if len(scores) % 2 == 0:
        #     # Even number of rounds. Grab the lowest half
        #     lowest = scores[:len(scores)/2]
        # else:
        #     # Odd number of rounds. Grab the lowest half, rounding up
        #     lowest = scores[:len(scores)/2+1]
        #
        # for s in lowest:
        #     flt_s = float(s) * .96
        #
        #     temp_h.append(int(round(flt_s)))
        # if not temp_h:
        #     self.handicap = self.def_handicap
        # else:
        #     self.handicap = sum(temp_h) / len(temp_h)

        #super(Golfer, self).save()

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    rating = models.FloatField()
    slope = models.FloatField()
    hole1par = models.IntegerField(default=0)
    hole2par = models.IntegerField(default=0)
    hole3par = models.IntegerField(default=0)
    hole4par = models.IntegerField(default=0)
    hole5par = models.IntegerField(default=0)
    hole6par = models.IntegerField(default=0)
    hole7par = models.IntegerField(default=0)
    hole8par = models.IntegerField(default=0)
    hole9par = models.IntegerField(default=0)
    hcap01 = models.IntegerField(default=0)
    hcap02 = models.IntegerField(default=0)
    hcap03 = models.IntegerField(default=0)
    hcap04 = models.IntegerField(default=0)
    hcap05 = models.IntegerField(default=0)
    hcap06 = models.IntegerField(default=0)
    hcap07 = models.IntegerField(default=0)
    hcap08 = models.IntegerField(default=0)
    hcap09 = models.IntegerField(default=0)
    mod_date = models.DateField(auto_now=True)

    @property
    def total_par(self):
        return self.hole1par + self.hole2par + self.hole3par + self.hole4par + self.hole5par + self.hole6par + \
               self.hole7par + self.hole8par + self.hole9par

    def __unicode__(self):
        return self.name


class Round(models.Model):
    golfer_id = models.ForeignKey(Golfer)
    course_id = models.ForeignKey(Course)
    date = models.DateField()
    year = models.IntegerField(default=0, blank=True)
    week_num = models.IntegerField(default=0)
    hole_1 = models.IntegerField(default=0)
    hole_2 = models.IntegerField(default=0)
    hole_3 = models.IntegerField(default=0)
    hole_4 = models.IntegerField(default=0)
    hole_5 = models.IntegerField(default=0)
    hole_6 = models.IntegerField(default=0)
    hole_7 = models.IntegerField(default=0)
    hole_8 = models.IntegerField(default=0)
    hole_9 = models.IntegerField(default=0)
    cur_handicap = models.IntegerField(default=0, null=True, blank=True)
    mod_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('week_num', 'year', 'golfer_id')

    def save(self):
        year = datetime.now().year
        scores = []
        rounds = Round.objects.filter(golfer_id=self.golfer_id).order_by('week_num')
        golfer = Golfer.objects.get(pk=self.golfer_id.id)
        self.cur_handicap = golfer.handicap

        super(Round, self).save()
        for r in rounds:
            if r.date.year == year:
                c = Course.objects.get(name=r.course_id)
                # Year is the same. Get the correct number of rounds
                calc = (r.score - c.rating)
                scores.append(calc)

        scores.sort()

        temp_h = []

        if len(scores) % 2 == 0:
            # Even number of rounds. Grab the lowest half
            lowest = scores[:len(scores)/2]
        else:
            # Odd number of rounds. Grab the lowest half, rounding up
            lowest = scores[:len(scores)/2+1]

        for s in lowest:
            flt_s = float(s) * .96
            print "Pre convert: ", flt_s
            print "Post convert: ", int(round(flt_s))
            temp_h.append(int(round(flt_s)))

        if not temp_h:
            golfer.def_handicap = self.cur_handicap
        else:
            print "Current Golfer Handicap: ", golfer.handicap
            #self.cur_handicap = sum(temp_h) / len(temp_h)
            golfer.handicap = round(float(sum(temp_h)) / float(len(temp_h)))
            print golfer.handicap
            golfer.save()
            print "New Golfer Handicap: ", golfer.handicap
        # self.cur_handicap = sum(temp_h) / len(temp_h)

        super(Round, self).save()

    @property
    def adj_scores(self):
        # function to adjust scores hole by hole for handicap. Will return list of scores
        # make list of scores
        # g = Golfer.objects.get(pk=self.golfer_id.id)
        c = Course.objects.get(name=self.course_id)
        scores = [[self.hole_1, c.hcap01], [self.hole_2, c.hcap02], [self.hole_3, c.hcap03], [self.hole_4, c.hcap04], \
                 [self.hole_5, c.hcap05], [self.hole_6, c.hcap06], [self.hole_7, c.hcap07], \
                 [self.hole_8, c.hcap08], [self.hole_9, c.hcap09]]

        adj_final = []
        for s in scores:
            per_hole_handicap = math.floor(self.cur_handicap / 9)
            leftovers = self.cur_handicap % 9
            if per_hole_handicap >= 1:
                adj_score = s[0] - per_hole_handicap
                if leftovers >= s[1]:
                    final_score = adj_score-1
                else:
                    final_score = adj_score
            else:
                if leftovers >= s[1]:
                    final_score = s[0] - 1
                else:
                    final_score = s[0]
            adj_final.append(int(final_score))

        return adj_final

    @property
    def score(self):
        return self.hole_1 + self.hole_2 + self.hole_3 + self.hole_4 + self.hole_5 + self.hole_6 + self.hole_7 + \
               self.hole_8 + self.hole_9

    @property
    def mod_score(self):
        final = self.adj_scores
        return sum(final)

    @property
    def points(self):
        c = Course.objects.get(name=self.course_id)
        scores = [[self.hole_1, c.hole1par], [self.hole_2, c.hole2par], [self.hole_3, c.hole3par], [self.hole_4, c.hole4par],
                          [self.hole_5, c.hole5par], [self.hole_6, c.hole6par], [self.hole_7, c.hole7par], [self.hole_8, c.hole8par],
                          [self.hole_9, c.hole9par]]
        points = 0.0

        hole_break = {'Par': 0, 'Birdie': 0, 'Eagle': 0, 'Bogey': 0, 'Other': 0}
        for s in scores:
            if s[0] - s[1] == 0:
                hole_break['Par'] += 1
            elif s[0] - s[1] == -1:
                hole_break['Birdie'] += 1
            elif s[0] - s[1] == -2:
                hole_break['Eagle'] += 1
            elif s[0] - s[1] == 1:
                hole_break['Bogey'] += 1
            else:
                hole_break['Other'] += 1

        points += hole_break['Par'] * .5
        points += hole_break['Birdie'] * 1
        points += hole_break['Eagle'] * 1

        return points

    @property
    def mod_points(self):
        c = Course.objects.get(name=self.course_id)
        scores = [[self.adj_scores[0], c.hole1par], [self.adj_scores[1], c.hole2par], [self.adj_scores[2], c.hole3par],
                  [self.adj_scores[3], c.hole4par], [self.adj_scores[4], c.hole5par], [self.adj_scores[5], c.hole6par],
                  [self.adj_scores[6], c.hole7par], [self.adj_scores[7], c.hole8par], [self.adj_scores[8], c.hole9par]]
        mod_points = 0.0

        hole_break = {'Par': 0, 'Birdie': 0, 'Eagle': 0, 'Bogey': 0, 'Other': 0}
        for s in scores:
            if s[0] - s[1] == 0:
                hole_break['Par'] += 1
            elif s[0] - s[1] == -1:
                hole_break['Birdie'] += 1
            elif s[0] - s[1] <= -2:
                hole_break['Eagle'] += 1
            elif s[0] - s[1] == 1:
                hole_break['Bogey'] += 1
            else:
                hole_break['Other'] += 1

        mod_points += hole_break['Par'] * .5
        mod_points += hole_break['Birdie'] * 1
        mod_points += hole_break['Eagle'] * 1

        return mod_points

    def __unicode__(self):
        return str(self.week_num)
