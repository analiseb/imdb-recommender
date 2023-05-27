from django.shortcuts import render
from django.http import HttpResponseRedirect
from recommender import basic_recommender

from users.models import MoviesListUser
from .forms import MovieForm

from math import nan

# recommender = basic_recommender.Recommender.from_config_mongo()
recommender = basic_recommender.Recommender.from_csv()


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = MovieForm(request.POST)

        if request.POST.get('save_movie'):
            form = MovieForm()

            if len(MoviesListUser.objects.filter(user=request.user,title=request.POST.get('title')))==0:
                movie_saved = MoviesListUser.objects.create(
                    user = request.user, 
                    title = request.POST.get('title'),
                    popularity = request.POST.get('popularity'),
                    vote_average = request.POST.get('vote_average'),
                    url_image = request.POST.get('url_image')
                    )
                movie_saved.save()

            movie_input = request.session['movie_input']
        else:
            form = MovieForm(request.POST)
            # create a form instance and populate it with data from the request:
            if form.is_valid():
                movie_input = request.POST.get("movie_ref")
                request.session['movie_input'] = movie_input

        # create a form instance and populate it with data from the request:
        movies_recommended = recommender.recommend(movie_input)
        movies_recommended = ["Movie Not found"] if movies_recommended is None else movies_recommended
        movie_input_found = movies_recommended[1]
        movie_input_found = (
            f"These are the recommendations we have found for you based on <b>{movie_input_found}</b>:"  
            if movie_input_found.lower()==movie_input.lower() else 
            f"<b>{movie_input}</b> not found . You may have been looking for <b>{movie_input_found}</b>? Here are our recommendations:"
            )

        df_similar_movies = movies_recommended[0]
        values_similar_movies = []
        for index, row in df_similar_movies.iterrows():
            title = row['title']
            pop = round(float(row['popularity']),2)
            ave = round(float(row['vote_average']),2)
            url_image = row['urls'] if isinstance(row['urls'],str) else None
            print(isinstance(url_image,str))
            if request.user.is_authenticated:
                previously_saved = len(MoviesListUser.objects.filter(user=request.user,title=title))==0
            else:
                previously_saved = None
            values_similar_movies.append({
                "title" : title,
                "popularity" : pop,
                "vote_average" : ave,
                "url_image": url_image,
                "previously_saved": previously_saved
                }
            )
        # print([m["url_image"] for m in values_similar_movies])
        # if form.is_valid():
        return render(request,'index.html',{
            'form':form,
            'movie_input_found':movie_input_found,
            'values_similar_movies':values_similar_movies
            }
        )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MovieForm()

    return render(request, 'index.html', {
        'form': form
        })

def about(request):
    return render(request, 'about.html')