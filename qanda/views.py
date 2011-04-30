from django.shortcuts import render_to_response
from qanda.models import Answer,Question,Category
from django.core.paginator import Paginator,EmptyPage, InvalidPage
from django.http import Http404
from qanda.forms import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

@login_required
def reply_question(request,
                   id,
                   template='reply.html'):
    """
    Reply to question
    """
    # get the question
    try:
        q = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']            
            # create new reply
            reply = Answer.objects.create(user=request.user,
                                           content=content,
                                           question=q)
            reply.save()
            # redirect to question page
            return HttpResponseRedirect(q.get_absolute_url())
    else:
        form = AnswerForm()
    return render_to_response(template,
                              {'form':form,'q':q},
                              context_instance=RequestContext(request))

def get_question(request,
                 id,
                 sl,
                 template='question.html'):
    """
    Fetch a single question
    sl = slug of the question
    """
    try:
        q = Question.objects.get(pk=id,slug=sl,active=1)
    except Question.DoesNotExist:
        raise Http404
    # we have a question
    # now find the answers that belong to this question
    try:
        answers = Answer.objects.filter(question=q)
    except Answer.DoesNotExist:
        answers = None

    return render_to_response(template,
                              {
                               'question' : q ,
                               'answers' : answers
                               },
                              context_instance=RequestContext(request))


def get_questions(request,
                  order='',
                  template='questions.html',
                  questions_per_page=10):
    """
    Returns questions
    default : returns latest questions
    """
    if order == '':
        questions = Question.objects.filter(active=1)
    else:
        questions = Question.objects.order_by(order).filter(active=1)
    
    paginator = Paginator(questions,questions_per_page)
    
    # check page number
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1 
    # Check page number again,make sure its correct
    try:
        questions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)
    
    return render_to_response(template,
                              {'questions' : questions },
                              context_instance=RequestContext(request))


def get_questions_by_category(request,
                              category_slug,
                              template='questions_by_category.html',
                              questions_per_page=10):
    """
    Return questions by category
    """
    try:
        that_category = Category.objects.get(slug=category_slug)
    except Exception: # fix this later!
        raise Http404
    
    if that_category is not None:
        questions = Question.objects.filter(categories=that_category)
       
    paginator = Paginator(questions,questions_per_page)
    
    # check page number
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    # Check page number again,make sure its correct        
    try:
        questions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)
            
    return render_to_response(template,
                              { 'questions' : questions },
                              context_instance=RequestContext(request))

@login_required
def ask_question(request,
                 template='ask.html',
                 success_url='/'):
    """
    ask a question!
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            question = form.cleaned_data['question']
            categories = form.cleaned_data['categories']
            # all clear!
            # simple slugify! temporary fix
            s = '-'.join(str(title).split())
            q = Question.objects.create(user=request.user,
                                        title=title,
                                        body=question,
                                        active=0,
                                        slug=s)
            # add categories - ManyToMany field
            for cat in categories:
                ea = Category.objects.get(title=cat)
                q.categories.add(ea)
            # done! save it
            q.save()
            # question created
            # now redirect to homepage
            return HttpResponseRedirect(success_url)     
    else:
        form = QuestionForm()
    
    return render_to_response(template,
                              {'form':form},
                              context_instance=RequestContext(request))
