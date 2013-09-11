from django.core.context_processors import request
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django import forms

from referenda.models import Poll, Vote
from referenda.forms import VoteForm

def home(request):
    poll_list = Poll.objects.order_by('-pub_date')[:5]
    voteform = VoteForm()
    voteform.fields['vote'].widget = forms.HiddenInput()
    context = {'poll_list': poll_list, 'voteform': voteform}
    return render(request, 'home.html', context)

def profile(request):
    return render(request, 'profile.html')

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    poll_list = Poll.objects.order_by('-pub_date')[:5]
    context = {'poll_list': poll_list}
    try:
        voteform = VoteForm(request.POST)
        if voteform.is_valid():
            print "Form valid"
            #user_votes = Vote.objects.filter(referendum=p)
            user_votes = Vote.objects.filter(referendum=p).filter(userid=request.user.id)
            print "User votes"
            print len(user_votes)
            if len(user_votes) > 0:
                print "ya has votado"
            else: 
                user = request.user.id
                print "User"
                print user
                if voteform.data['vote'] == 'Yes':
                    p.votes_positive = p.votes_positive + 1
                else:
                    p.votes_negative = p.votes_negative + 1
                p.save()
                vote = Vote()
                print "Vote"
                print vote.id
                vote.referendum = p
                vote.userid = user
                vote.save()
                print vote.id
        else:
            user_vote = voteform.errors
    except Exception as e:
        print e
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html', context)

def vote_referendum(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except:
        raise Http404
    return redirect(p)

def referendum(request, poll_id):
    try:
        referendum = Poll.objects.get(pk=poll_id)
        context = {'referendum': referendum}
    except:
        raise Http404
    return render(request, 'referendum.html', context)
