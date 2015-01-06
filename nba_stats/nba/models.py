from django.db import models
from datetime import date, datetime

class NBAModelManager(models.Manager):
    def get_by_natural_key(self, nba_id):
        return self.get(nba_id=nba_id)

# NBA Mixin
class NBAModel(models.Model):
    objects = NBAModelManager()

    nba_id = models.PositiveIntegerField(null=False, unique=True)

    def natural_key(self):
        return (self.nba_id,)

    class Meta:
        abstract = True

class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) \
            < (self.birthdate.month, self.birthdate.day))

    def __unicode__(self):
        return self.full_name

    class Meta:
        abstract = True
        ordering = ['first_name', 'last_name']

class School(models.Model):

    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

class Player(Person, NBAModel):

    school = models.ForeignKey(School, null=True)

class League(models.Model):
    
    name = models.CharField(max_length=60)

class Conference(models.Model):
   
    name = models.CharField(max_length=60)
    league = models.ForeignKey(League)

class Division(models.Model):
    
    name = models.CharField(max_length=60)
    conference = models.ForeignKey(Conference)

class Team(NBAModel):

    city = models.CharField(max_length=60)
    nickname = models.CharField(max_length=60)
    division = models.ForeignKey(Division)

class Game(NBAModel):

    attendance = models.PositiveIntegerField()
    