from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic


# def index(request):
# return HttpResponse("Hello Everyone!!, This is a Django framework!!")
# latest_question_list = Question.objects.order_by('-pub_date')[:5]
# output = ', '.join([q.question_text for q in latest_question_list])
# return HttpResponse(output)

# def index(request):
#   latest_question_list = Question.objects.order_by('-pub_date')[:5]
# templates = loader.get_template('employee_register/index.html')
# context = {
#    'latest_question_list': latest_question_list,
# }
# return HttpResponse(templates.render(context, request))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'employee_register/index.html', context)

class IndexView(generic.ListView):
    template_name = 'employee_register/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last two published questions."""
        return Question.objects.order_by('-pub_date')[:2]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'employee_register/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'employee_register/results.html'


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'employee_register/detail.html', {'question': question})
#
#     # try:
#     #    question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #    raise Http404("Question does not exist")
#     # return render(request, 'employee_register/detail.html', {'question': question})
#
#     # return HttpResponse("You're looking at question %s" % question_id)
#
#
# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'employee_register/results.html', {'question': question})


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'employee_register/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('employee_register:results', args=(question.id,)))
