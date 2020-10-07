from django.db import models

# Create your models here.
# Models are used to interact with databases in Django
# So each must subclass models.Model, each class has classvariables --> each represent a field in the database
# so each classvar is from a specific class relating to the type of the field
class Question(models.Model):
    question_text = models.CharField(max_length=200) # max length is a required property
    pub_date = models.DateTimeField('date published') # first argument (if filled in) is to make code more human readable

    def __str__(self): # since you will be handling value as objects, you want a __str__ to represent at a human readable format
        return """
        {} asked on {}
        """.format(self.question_text, self.pub_date)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # take a foreign key (single use) out of Question class/table (One Choice can only relate to one Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return """
        {} choice with {} votes on question {}
        """.format(self.choice_text, self.votes, self.question)

def print_stuff():
    print(Question.objects.all())
    print(Question.objects.filter(id = 1))
    print(Question.objects.filter(question_text = "What's newer?"))
    print(Question.objects.filter(question_text__startswith = "What")) # __ underscore to apply function within the values
    from django.utils import timezone
    cyear = timezone.now().year
    print(Question.objects.filter(pub_date__year = cyear))
    print(Question.objects.get(pk = 1)) # pk stands for primary key, get only gets one unique line

    q = Question.objects.get(pk = 1)
    q.choice_set.all() # list choices that are available for question (q object)
    q.choice_set.create(choice_text='Not much', votes=0)
    q.choice_set.create(choice_text='The sky', votes=0)
    c = q.choice_set.create(choice_text='Just hacking again', votes=0)
    print(q.choice_set.all()) 

# This model can be added to the INSTALLED_APPS list in settings
# After performing "python manage.py makemigrations app01", this model will be added to the migrations folder
# migrate will update and manages your databases
# use "python manage.py sqlmigrate app01 0001" to return SQL statements of the database that you created with the makemigrations command
# to apply at the end, perform command "python manage.py migrate"
# a detailed explanation here: "https://docs.djangoproject.com/en/3.1/intro/tutorial02/"


# "python manage.py shell": opens a shell (just like ipython but than in your django application --> shell can be configured in settings.py (env vars))
# working in this shell operates database as a object oriented approach
# make new parts of the db and save them, you can just have an object of the line and call methods on it
command = """ 
>>> from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]> 
"""