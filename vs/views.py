from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import CreateView
from .models import Question,Choice,ControlVote
from .forms import RegistrationForm,LoginForm

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

def loginView(request):
    context={}
    if request.user.is_authenticated:
        return redirect('vs:poll')
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('vs:poll')
    else:
        form=LoginForm()
    context['logform']=form
    return render(request,'login.html',context)


def logoutview(request):
    logout(request)
    return redirect('/')


@login_required(login_url="vs:login")
def pollview(request):
    context={}
    ques=Question.objects.order_by('-pub_date')[:5]
    context['ques']=ques
    return render(request,'poll.html',context)

def registrationview(request):
    context={}
    if request.user.is_authenticated:
        return redirect('vs:poll')
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vs:login')
        else:
            context['regform']=form
    else:
        form=RegistrationForm()
        context['regform']=form
    return render(request,'register.html',context)
    
def logoutView(request):
    logout(request)
    return redirect('vs:index')

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context={}
    ques=Question.objects.order_by('-pub_date')[:5]
    context['ques']=ques
    if request.method=="POST":
        temp=ControlVote.objects.get_or_create(user=request.user,position=question)[0]
        if temp.status==False:
            selected_choice=question.choice_set.get(pk=request.POST['choice'])
            selected_choice.votes+=1
            selected_choice.save()
            temp.status=True
            temp.save()
            return HttpResponseRedirect(reverse('vs:results', args=(question.id,)))
        else:
            messages.success(request, 'You have already been voted this position')
            return render(request,'poll.html',context)
    else:
        return render(request,'poll.html',context)
    

