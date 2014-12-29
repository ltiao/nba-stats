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
    birth_date = models.DateField()

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def _get_age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) \
            < (self.birthdate.month, self.birthdate.day))

    full_name = property(_get_full_name)
    age = property(_get_age)

    def __unicode__(self):
        return self.full_name

    class Meta:
        abstract = True
        ordering = ['first_name', 'last_name']

class Player(Person, NBAModel):
    school = models.CharField(max_length=60, null=True)
