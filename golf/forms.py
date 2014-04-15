from django import forms
from golf.models import Golfer, Course, Round


class GolferForm(forms.ModelForm):
    last_name = forms.CharField(max_length=128, help_text="Last Name.")
    first_name = forms.CharField(max_length=128, help_text="First Name.")
    email = forms.CharField(max_length=128, help_text="Email Address.", required=False)
    phone = forms.CharField(max_length=12, help_text="Phone Number.", required=False)
    phone_alt = forms.CharField(max_length=12, help_text="Alternate Phone", required=False)
    def_handicap = forms.IntegerField(help_text="Starting Handicap.")
    handicap = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Golfer


class CourseForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Course Name")
    rating = forms.FloatField(help_text="Rating")
    slope = forms.FloatField(help_text="Slope")
    hole1par = forms.IntegerField(help_text="Hole 1 Par")
    hole2par = forms.IntegerField(help_text="Hole 2 Par")
    hole3par = forms.IntegerField(help_text="Hole 3 Par")
    hole4par = forms.IntegerField(help_text="Hole 4 Par")
    hole5par = forms.IntegerField(help_text="Hole 5 Par")
    hole6par = forms.IntegerField(help_text="Hole 6 Par")
    hole7par = forms.IntegerField(help_text="Hole 7 Par")
    hole8par = forms.IntegerField(help_text="Hole 8 Par")
    hole9par = forms.IntegerField(help_text="Hole 9 Par")
    hcap01 = forms.IntegerField(help_text="Hole 1 Handicap")
    hcap02 = forms.IntegerField(help_text="Hole 2 Handicap")
    hcap03 = forms.IntegerField(help_text="Hole 3 Handicap")
    hcap04 = forms.IntegerField(help_text="Hole 4 Handicap")
    hcap05 = forms.IntegerField(help_text="Hole 5 Handicap")
    hcap06 = forms.IntegerField(help_text="Hole 6 Handicap")
    hcap07 = forms.IntegerField(help_text="Hole 7 Handicap")
    hcap08 = forms.IntegerField(help_text="Hole 8 Handicap")
    hcap09 = forms.IntegerField(help_text="Hole 9 Handicap")

    class Meta:
        model = Course


class RoundForm(forms.ModelForm):
    golfer_id = forms.ModelChoiceField(queryset=Golfer.objects.all().order_by('last_name'),
                                       empty_label="(Select a golfer...)", help_text="Golfer")
    course_id = forms.ModelChoiceField(queryset=Course.objects.all().order_by('name'), help_text="Course",
                                       empty_label="(Select a course...)")
    date = forms.DateField(help_text="Date")
    year = forms.IntegerField(widget=forms.HiddenInput(), initial=2014)
    week_num = forms.ChoiceField(widget=forms.Select, choices=((str(x), x) for x in range(1, 19)), help_text="Week No.")
    hole_1 = forms.IntegerField(help_text="Hole 1")
    hole_2 = forms.IntegerField(help_text="Hole 2")
    hole_3 = forms.IntegerField(help_text="Hole 3")
    hole_4 = forms.IntegerField(help_text="Hole 4")
    hole_5 = forms.IntegerField(help_text="Hole 5")
    hole_6 = forms.IntegerField(help_text="Hole 6")
    hole_7 = forms.IntegerField(help_text="Hole 7")
    hole_8 = forms.IntegerField(help_text="Hole 8")
    hole_9 = forms.IntegerField(help_text="Hole 9")

    class Meta:
        model = Round

