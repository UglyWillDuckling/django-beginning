from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .forms import NewTopicForm

from .models import Board, Post


def home(request):
    boards = Board.objects.all()
    return render(request, "home.html", {"boards": boards})


def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, "topics.html", {"board": board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get("message"), topic=topic, created_by=user
            )
    else:
        form = NewTopicForm()

    return render(request, "new_topic.html", {"board": board, "form": form})
