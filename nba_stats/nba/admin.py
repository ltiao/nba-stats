from django.contrib import admin
from nba.models import Player

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

admin.site.register(Player)
