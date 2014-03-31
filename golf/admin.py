from django.contrib import admin
from golf.models import Golfer, Round, Course

class RoundAdmin(admin.ModelAdmin):
    list_display = ('golfer_id', 'date', 'week_num', 'mod_date')

admin.site.register(Golfer)
admin.site.register(Round, RoundAdmin)
admin.site.register(Course)