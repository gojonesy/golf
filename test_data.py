import os

# script to populate golf league DB with some test data for demonstration/validation

def populate():

    add_golfer('Ric Flair', 'whoooooo@email.email', '2171212121')
    add_golfer('Hulk Hogan', 'hhogan@hulkamania.org', '2171211111')
    add_golfer('Randy Savage', 'ohyeah@macho.org', '2174999999')

    add_course('Bunn - Front 9', 34, 120, 5, 4, 4, 3, 4, 4, 5, 3, 4)
    add_course('Bunn - Back 9', 35.5, 120, 4, 5, 4, 4, 5, 3, 4, 3, 4)

    for g in Golfer.objects.all():
        print str(g)
    for c in Course.objects.all():
        print str(c)

def add_golfer(name, email, phone):
    g = Golfer.objects.get_or_create(name=name, email=email, phone=phone)[0]
    return g

def add_course(name, rating, slope, hole1par, hole2par, hole3par, hole4par, hole5par, hole6par, hole7par, hole8par,
               hole9par):
    c = Course.objects.get_or_create(name=name, rating=rating, slope=slope, hole1par=hole1par, hole2par=hole2par, hole3par=hole3par,
                                     hole4par=hole4par, hole5par=hole5par, hole6par=hole6par, hole7par=hole7par, hole8par=hole8par,
                                     hole9par=hole9par)[0]
    return c

def add_round(golfer_id, course_id, date, week_num, hole_1, hole_2,
              hole_3, hole_4, hole_5, hole_6, hole_7, hole_8, hole_9):
    r = Round.objects.get_or_create(golfer_id=golfer_id, course_id=course_id, date=date, week_num=week_num,
                                    hole_1=hole_1, hole_2=hole_2, hole_3=hole_3, hole_4=hole_4,
                                    hole_5=hole_5, hole_6=hole_6, hole_7=hole_7, hole_8=hole_8,
                                    hole_9=hole_9)
    return r

# executes from here
if __name__ == '__main__':
    print "Starting Golf League Test data population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golf_league.settings')
    from golf.models import Golfer, Course, Round
    populate()
