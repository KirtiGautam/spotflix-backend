import requests
from backend.settings import TMDB_KEY

API_BASE = 'https://api.themoviedb.org/3/'
POSTER_BASE = 'https://image.tmdb.org/t/p/'


def get_trending(type: str, window: str, page: str):
    '''
    Get trending Media
    '''
    return requests.get(API_BASE + f'/trending/{type}/{window}?api_key={TMDB_KEY}&page={page}').json()


def trending_media(page: int = 1):
    '''
    Get trending Media
    '''
    return get_trending('all', 'day', page)


def trending_movies(page: int = 1):
    '''
    Get trending Movies
    '''
    return get_trending('movie', 'day', page)


def trending_shows(page: int = 1):
    '''
    Get trending Shows
    '''
    return get_trending('tv', 'day', page)
