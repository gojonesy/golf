from django.db import models
from datetime import datetime


class Golfer(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, null=True, blank=True, default="test")
    phone = models.CharField(max_length=128, null=True, blank=True)
    phone_alt = models.CharField(max_length=128, null=True, blank=True)
    def_handicap = models.IntegerField(default=0)
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
    mod_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('week_num', 'year', 'golfer_id')

    @property
    def score(self):
        return self.hole_1 + self.hole_2 + self.hole_3 + self.hole_4 + self.hole_5 + self.hole_6 + self.hole_7 + self.hole_8 + self.hole_9

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

    def __unicode__(self):
        return str(self.week_num)
