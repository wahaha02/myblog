#
# Copyright 2008 Darrel Herbst
#
# This file is part of Django-Rabid-Ratings.
#
# Django-Rabid-Ratings is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Django-Rabid-Ratings is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Django-Rabid-Ratings.  If not, see <http://www.gnu.org/licenses/>.
#

from django import template
from rabidratings.models import Rating, RatingEvent

register = template.Library()

def show_rating(context, rating_key):
    """ 
    displays necessary html for the rating
    """
    rating_key = str(rating_key)
    rating, created = Rating.objects.get_or_create(key=rating_key)
    return {
        'rating_key': rating_key,
        'total_votes': rating.total_votes,
        'total_ratings': rating.total_rating,
        'rating': "%.2f" % rating.avg_rating,
        'percent': rating.percent,
        'max_stars': 5
        }
register.inclusion_tag("rabidratings/rating.html", takes_context=True)(show_rating)

def rating_header(context):
    """
    Inserts the includes needed into the html
    """
    return { 'rabidratings_media_url': '/static/rabidratings' }

register.inclusion_tag("rabidratings/rating_header.html", takes_context=True)(rating_header)

