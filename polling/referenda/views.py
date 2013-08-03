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
            old_votes = get_object_or_404(Vote, pk=poll_id)
            user_vote = form.cleaned_data['vote']
            user = request.user.id
            p.votes_negative = p.votes_negative + 1
            p.save()
            vote = Vote(poll_id)
            vote.userid = user
            vote.save()
        else:
            user_vote = voteform.errors
    except:
        return render(request, 'home.html', context)
    else:
        context.update({'usersan': old_votes.userid})
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
