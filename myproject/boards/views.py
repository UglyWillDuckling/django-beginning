from django.http import HttpResponse

from myproject.boards.models import Board


def home(request):
    boards = Board.objects.all()
    boards_names = []

    for board in boards:
        boards_names.append(board.name)

    html = "<br>".join(boards_names)

    return HttpResponse(html)
