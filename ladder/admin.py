from django.contrib import admin
from ladder.models import Player
from ladder.models import Match

class PlayerAdmin(admin.ModelAdmin):
    list_display=('name', 'rating')

admin.site.register(Player, PlayerAdmin)

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields': ['black','white','date','handicap','komi']}),
        ('Result',   {'fields': ['result', 
                                 'result_type',
                                 'score_black', 
                                 'score_white']}),
    ]
    list_filter = ['date']
    search_fields = ['black__name', 'white__name']


admin.site.register(Match, MatchAdmin)


admin.site.site_header = "Go Ladder Administration"
admin.site.site_title  = "Go Ladder Administration"
