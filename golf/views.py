from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from golf.models import Golfer, Round, Course
from django.http import Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from golf.forms import GolferForm, CourseForm, RoundForm
from django.db.models import Avg, Count, Sum
import math


def custom_404(request):
    return render_to_response('404.html')

def index(request):
    context = RequestContext(request)
    table_dict = {}
    golfer_list = sorted(Golfer.objects.order_by(), key=lambda a: a.adj_points, reverse=True)
    cur_year = datetime.now().year

    nums = []
    for i in range(1, 19):
        nums.append(i)

    for g in golfer_list:
        points_list = [0.0] * (len(nums))

        rounds = Round.objects.all().filter(date__year=cur_year, golfer_id=g.id).order_by('-week_num')
        # temp_list.append(g.id)
        for r in rounds:
            points_list[r.week_num - 1] = r.mod_points
            #((r.week_num - 1), r.points)

        table_dict[g.id] = {'points': points_list}

    round_list = Round.objects.order_by('-date')[:10]

    context_dict = {'golfers': golfer_list, 'rounds': round_list, 'nums': nums, 'table': table_dict}

    return render_to_response('golf/index.html', context_dict, context)

def golfer(request, golfer_id):
    context = RequestContext(request)
    # Get the current year and pass it to the avg_score function
    cur_year = datetime.now().year

    try:
        golfer = Golfer.objects.get(pk=golfer_id)
        total = golfer.total_points
        holes = hole_breakdown(golfer_id, cur_year)
        #hcap = handicap(golfer_id, cur_year)
        #if hcap == 0:
            #hcap = golfer.def_handicap
            #Round.objects.all().filter(golfer_id=golfer).aggregate(Avg(score))
    except Golfer.DoesNotExist:
        raise Http404
    return render_to_response('golf/golfer.html', {'golfer': golfer, 'points': total, 'holes': holes}, context)


def course(request, course_id):
    context = RequestContext(request)
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404
    return render_to_response('golf/course.html', {'course': course}, context)


def round(request, round_id):
    context = RequestContext(request)
    try:
        r = Round.objects.get(pk=round_id)
    except Round.DoesNotExist:
        raise Http404
    return render_to_response('golf/round.html', {'round': r}, context)


def courses(request):
    context = RequestContext(request)

    course_list = Course.objects.all

    return render_to_response('golf/courses.html', {'courses': course_list}, context)


def rounds(request):
    context = RequestContext(request)

    round_list = Round.objects.all

    return render_to_response('golf/rounds.html', {'rounds': round_list}, context)


def about(request):
    context = RequestContext(request)

    return render_to_response('golf/about.html', context)


def roster(request):
    context = RequestContext(request)

    roster_list = sorted(Golfer.objects.all(), key=lambda a: a.total_points, reverse=True)

    return render_to_response('golf/roster.html', {'roster': roster_list},  context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect ('/golf/')
            else:
                return HTTPResponse("Your account is disabled. Contact justinjones00@gmail.com with the issue")
                # <a href='mailto:justinjones00@gmail.com'>justinjones00@gmail.com</a>
        else:
            # Bad login credentials
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied")
    else:
        return render_to_response('golf/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/golf/')

@login_required
def add_golfer(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = GolferForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect('/golf/')
        else:
            print form.errors
    else:
        form = GolferForm

    return render_to_response('golf/add_golfer.html', {'form': form}, context)


@login_required
def add_course(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect('/golf/courses/')
        else:
            print form.errors
    else:
        form = CourseForm

    return render_to_response('golf/add_course.html', {'form': form}, context)


@login_required
def add_round(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = RoundForm(request.POST)
        # print form.year
        if form.is_valid():

            dateval = form.cleaned_data['date']
            form.cleaned_data['year'] = dateval.year
            form.save(commit=True)

            return HttpResponseRedirect('/golf/')
        else:
            print form.errors
    else:
        form = RoundForm

    return render_to_response('golf/add_round.html', {'form': form}, context)


# Total functions follow. These are not views... Keep the views above this comment.
##################################################################################
##################################################################################

def num_rds(g_id, year):
    # count the number of rounds for a golfer by year
    ##### THIS IS HOW WE AGGREGATE THINGS!
    total = Round.objects.filter(date__year=year, golfer_id=g_id).count()
    # annotate(total_rounds=Count('golfer_id'))
    print total
    if total:
        return total
    else:
        return 0

def avg_score(g_id, year):
    # Returns golfer's average for the year
    rounds = Round.objects.all().filter(date__year=year, golfer_id=g_id)
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


def avg_points(g_id, year):
    # calculate golfer's average here
    # golfer = Golfer.objects.get(pk=golfer_id)
    rounds = Round.objects.all().filter(date__year=year, golfer_id=g_id)

    total = 0
    count = 0
    for r in rounds:

        total += int(r.points)
        count += 1
    if not total or not count:
        p_avg = 0
    else:
        p_avg = total / count
    return p_avg

def hole_breakdown(g_id, year):
    # return the number of eagles, birdies, pars, bogies and other scores
    eagl, bird, par, bogy, othr = 0, 0, 0, 0, 0
    rounds = Round.objects.all().filter(date__year=year, golfer_id=g_id)

    for r in rounds:
        c = Course.objects.get(name=r.course_id)

        scores = [[r.hole_1, c.hole1par], [r.hole_2, c.hole2par], [r.hole_3, c.hole3par], [r.hole_4, c.hole4par],
                  [r.hole_5, c.hole5par], [r.hole_6, c.hole6par], [r.hole_7, c.hole7par], [r.hole_8, c.hole8par],
                  [r.hole_9, c.hole9par]]
        # Check for hole outcomes
        for i in scores:
            par += par_check(i[0], i[1])
            bird += bird_check(i[0], i[1])
            eagl += eagl_check(i[0], i[1])
            bogy += bogy_check(i[0], i[1])
            othr += othr_check(i[0], i[1])

    value_list = [par, bird, eagl, bogy, othr]
    return value_list

def points_calc(g_id, year, week):
    hole_break = {}
    r = Round.objects.get(golfer_id=g_id, week_num=week, date__year=year)
    c = Course.objects.get(name=r.course_id)
    scores = [[r.hole_1, c.hole1par], [r.hole_2, c.hole2par], [r.hole_3, c.hole3par], [r.hole_4, c.hole4par],
                      [r.hole_5, c.hole5par], [r.hole_6, c.hole6par], [r.hole_7, c.hole7par], [r.hole_8, c.hole8par],
                      [r.hole_9, c.hole9par]]
    points = 0.0

    for s in scores:
        hole_break['Par'] = par_check(s[0], s[1])
        hole_break['Birdie'] = bird_check(s[0], s[1])
        hole_break['Eagle'] = eagl_check(s[0], s[1])
        hole_break['Bogey'] = bogy_check(s[0], s[1])
        hole_break['Other'] = othr_check(s[0], s[1])

    points += hole_break['Par'] * .5
    points += hole_break['Birdie'] * 1
    points += hole_break['Eagle'] * 1

    return points

def par_check(hole, hole_par):
    if hole - hole_par == 0:
        return 1
    else:
        return 0

def bird_check(hole, hole_par):
    if hole - hole_par == -1:
        return 1
    else:
        return 0

def eagl_check(hole, hole_par):
    if hole - hole_par == -2:
        return 1
    else:
        return 0

def bogy_check(hole, hole_par):
    if hole - hole_par == 1:
        return 1
    else:
        return 0

def othr_check(hole, hole_par):
    if hole - hole_par > 1:
        return 1
    else:
        return 0

def handicap(g_id, year):
    # Calculates a golfer's handicap based on rounds
    # count the number of rounds for a golfer by year
    # r_total = 0
    scores = []
    rounds = Round.objects.filter(golfer_id=g_id).order_by('week_num')

    for r in rounds:
        if r.date.year == year:
            c = Course.objects.get(name=r.course_id)
            # Year is the same. Get the correct number of rounds
            calc = (r.score - c.rating)
            scores.append(calc)

    scores.sort()

    temp_h = []
    # Make sure we have 5 scores
    if len(scores) % 2 == 0:
        # Even number of rounds. Grab the lowest half
        lowest = scores[:len(scores)/2]
    else:
        # Odd number of rounds. Grab the lowest half, rounding up
        lowest = scores[:len(scores)/2+1]

    for s in lowest:
            flt_s = float(s) * .96
            print "Pre convert: ", flt_s
            print "Post convert: ", int(flt_s)
            temp_h.append(int(flt_s))

    handicap = sum(temp_h) / len(temp_h)


    return handicap


