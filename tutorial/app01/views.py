from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice

# Create your views here.
# def index(request):
#     q_list = Question.objects.order_by("-pub_date")[:5]
#     out = ""
#     for x in q_list:
#         out = out + "<br>\"" + x.question_text + "\": published on: " + str(x.pub_date.day) + "/" + str(x.pub_date.month) + "/" + str(x.pub_date.year)
#         # can put html in the string apparently for layouting
#     return HttpResponse(out)

def index(request):
    q_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("app01/index.html") # template engine
    context = { "latest_question_list" : q_list } # dictionary with what will be passed to the template engine 
    # (key is what will be used in the template engine, value is object in python)
    return HttpResponse(template.render(context, request)) # full explanation: you make a generate object with context to be filled in, then this passed into an HTTPresponse

    # the above code has been shortcuted in Django (DRY thought I guess)
# def index(request):
#     q_list = Question.objects.order_by("-pub_date")[:5]
#     context = { "latest_question_list" : q_list }
#     return render(request, "app01/index.html", context)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id) # get the question_id'ed row in the database
#     except Question.DoesNotExist:
#         raise Http404(f"Question {question_id} does not exist in database")
#     return render(request, "app01/detail.html", {"question" : question})

    # again there is a shortcut for the above code
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) # default error message is given on 404
    return render(request, "app01/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    return render(request, 'app01/results.html', {"question": question, "choices": choices})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) # request.POST["choice"] will show value (HTML) of the selected radiobutton
    except (KeyError, Choice.DoesNotExist):
        return render(request, "app01/detail.html", {"question": question, "error_message": "No choice selected"})
        # redirect back to detail.html page if no choice was selected
    else:
        selected_choice.votes += 1
        selected_choice.save() # save into db
        print(reverse('app01:results', args=(question_id,))) # args must be iterable not args
        # fills in arguments from the urls.py file: ['app01/(?P<question_id>[0-9]+)/results/$']
        return HttpResponseRedirect(reverse('app01:results', args=(question_id,))) # HttpResponseRedirect only receives a URL as a argument (HTTP302)
        # reverse is a url constructor, check documentation