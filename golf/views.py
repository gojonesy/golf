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

    context_dict = {'golfers': golfer_list, 'nums': nums, 'table': table_dict}

    return render_to_response('golf/index.html', context_dict, context)

def golfer(request, golfer_id):
    context = RequestContext(request)
    # Get the current year and pass it to the avg_score function
    cur_year = datetime.now().year
    round_list = Round.objects.filter(golfer_id=golfer_id).order_by('date')
    try:
        golfer = Golfer.objects.get(pk=golfer_id)
        holes = hole_breakdown(golfer_id, cur_year)
        def_holes = holes[0]
        adj_holes = holes[1]
        stable = stable_points(adj_holes)

    except Golfer.DoesNotExist:
        raise Http404
    return render_to_response('golf/golfer.html', {'golfer': golfer, 'def_holes': def_holes, 'adj_holes': adj_holes,
                                                   'rounds': round_list, 'stable_points': stable}, context)


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

@login_required
def rounds(request, week_num):
    context = RequestContext(request)

    round_list = Round.objects.filter(week_num=week_num, year=datetime.now().year)

    return render_to_response('golf/rounds.html', {'rounds': round_list, 'week': week_num}, context)


def about(request):
    context = RequestContext(request)

    return render_to_response('golf/about.html', context)


def roster(request):
    context = RequestContext(request)

    roster_list = Golfer.objects.order_by('last_name')
    nums = []
    for i in range(1, (len(roster_list) + 1)):
        nums.append(i)

    return render_to_response('golf/roster.html', {'roster': roster_list, 'nums': nums},  context)


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
def skins(request):
    context = RequestContext(request)

    weeks = Round.objects.values_list('week_num', flat=True).distinct().order_by('week_num')

    return render_to_response('golf/skins.html', {'weeks': weeks}, context)

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

def hole_breakdown(g_id, year):
    # return the number of eagles, birdies, pars, bogies and other scores
    eagl, bird, par, bogy, othr, a_par, a_bird, a_eagl, a_bogy, a_othr = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    rounds = Round.objects.all().filter(date__year=year, golfer_id=g_id)

    for r in rounds:
        c = Course.objects.get(name=r.course_id)
        adj = [[r.adj_scores[0], c.hole1par], [r.adj_scores[1], c.hole2par], [r.adj_scores[2], c.hole3par],
               [r.adj_scores[3], c.hole4par], [r.adj_scores[4], c.hole5par], [r.adj_scores[5], c.hole6par],
               [r.adj_scores[6], c.hole7par], [r.adj_scores[7], c.hole8par], [r.adj_scores[8], c.hole9par],]
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

        for a in adj:
            a_par += par_check(a[0], a[1])
            a_bird += bird_check(a[0], a[1])
            a_eagl += eagl_check(a[0], a[1])
            a_bogy += bogy_check(a[0], a[1])
            a_othr += othr_check(a[0], a[1])

    hole_break = [par, bird, eagl, bogy, othr]
    adj_break = [a_par, a_bird, a_eagl, a_bogy, a_othr]
    return hole_break, adj_break


def stable_points(holes):
    s_par = holes[0] * 2
    s_bir = holes[1] * 3
    s_eag = holes[2] * 4
    s_bog = holes[3]

    total = s_par + s_bir + s_eag + s_bog
    if not total:
        total = 0.0

    return total


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
