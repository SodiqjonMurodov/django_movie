from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft="False")


class MovieDetailView(DetailView):
    """Детали фильма"""
    model = Movie
    slug_field = "url"


class AddComment(View):
    """ADD Comment"""

    def post(self, request, pk):
        form = CommentForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('receiver', None):
                form.receiver_id = int(request.POST.get('receiver'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
