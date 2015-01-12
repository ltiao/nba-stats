from django.db import models
from datetime import date, datetime

class NBAModelManager(models.Manager):
   
    def get_by_natural_key(self, nba_id):
        return self.get(nba_id=nba_id)

# NBA Mixin
class NBAModel(models.Model):
    objects = NBAModelManager()

    nba_id = models.CharField(max_length=30, null=False, unique=True)
    nba_code = models.CharField(max_length=30, null=True)

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

    class Meta:
        ordering = ['name']

def player_photo_uploads_to(instance, filename):
    return unicode(instance.nba_id)

class Player(Person, NBAModel):

    school = models.ForeignKey(School, null=True)
    photo = models.ImageField(
        upload_to = 'players', 
        null = True
    )

class League(models.Model):
    
    name = models.CharField(max_length=60)

class Conference(models.Model):
   
    name = models.CharField(max_length=60)
    league = models.ForeignKey(League, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Division(models.Model):
    
    name = models.CharField(max_length=60)
    conference = models.ForeignKey(Conference)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Arena(models.Model):

    name = models.CharField(max_length=60, unique=True)
    capacity = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Team(NBAModel):

    abbr = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=60)
    nickname = models.CharField(max_length=60)
    logo = models.FileField(upload_to='logos', null=True)
    division = models.ForeignKey(Division, null=True)
    arena = models.ForeignKey(Arena, null=True)

    @property
    def name(self):
        return '%s %s' % (self.city, self.nickname)

    @property
    def conference(self):
        return self.division.conference

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("city", "nickname")

class Game(NBAModel):

    attendance = models.PositiveIntegerField()
    