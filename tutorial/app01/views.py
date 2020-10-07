from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice

# Create your views here.
def index(request):
    q_list = Question.objects.order_by("-pub_date")[:5]
    out = ""
    for x in q_list:
        out = out + "<br>\"" + x.question_text + "\": published on: " + str(x.pub_date.day) + "/" + str(x.pub_date.month) + "/" + str(x.pub_date.year)
        # can put html in the string apparently for layouting
    return HttpResponse(out)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)