from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from nba.models import Player, League, Conference, \
	Division, School, Team, Arena, PlayerMembership, Group, Season, Game

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text', 'first_name', 'last_name']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date')
#     list_filter = ['pub_date']

# # Register your models here.
# admin.site.register(Choice)
# admin.site.register(Question, QuestionAdmin)

class PlayerMembershipInline(admin.TabularInline):
	model = PlayerMembership
	extra = 3

class TeamAdmin(admin.ModelAdmin):
	inlines = (PlayerMembershipInline,)

class PlayerAdmin(admin.ModelAdmin):
	inlines = (PlayerMembershipInline,)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Conference)
admin.site.register(Division)
admin.site.register(Group, MPTTModelAdmin)
admin.site.register(School)
admin.site.register(Team, TeamAdmin)
admin.site.register(Arena)
admin.site.register(Season)
admin.site.register(Game)
