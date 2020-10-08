from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic # easier for templating, contains generic views that can be altered
from .models import Question, Choice


class IndexView(generic.ListView): # subclassed from ListView
    template_name = 'app02/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView): # subclassed from DetailView
    # The DetailView generic view expects the primary key value captured from the URL to be called "pk", so we’ve changed question_id to pk for the generic views (urls.py)
    model = Question
    template_name = 'app02/detail.html' # overwrites default naming of the page


class ResultsView(generic.DetailView): # subclassed from DetailView
    model = Question
    template_name = 'app02/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) # request.POST["choice"] will show value (HTML) of the selected radiobutton
    except (KeyError, Choice.DoesNotExist):
        return render(request, "app02/detail.html", {"question": question, "error_message": "No choice selected"})
        # redirect back to detail.html page if no choice was selected
    else:
        selected_choice.votes += 1
        selected_choice.save() # save into db
        print(reverse('app02:results', args=(question_id,))) # args must be iterable not args
        # fills in arguments from the urls.py file: ['app01/(?P<question_id>[0-9]+)/results/$']
        return HttpResponseRedirect(reverse('app02:results', args=(question_id,))) # HttpResponseRedirect only receives a URL as a argument (HTTP302)
        # reverse is a url constructor, check documentation