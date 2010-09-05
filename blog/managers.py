from django.db import models

class FavouriteManager(models.Manager):
    def get_public(self):
        return self.get_query_set().filter(is_public=True).order_by('-mod_date')

class PostManager(models.Manager):
    def get_post(self):
        return self.get_query_set().filter(type='post', status='publish').order_by('-date')

    def get_post_by_category(self, cat):
        return self.get_query_set().filter(type='post', status='publish',
                category=cat.id).order_by('-date')

    def get_post_by_date(self, year, month):
        return self.get_query_set().filter(type='post', status='publish',
                date__year=int(year),
                date__month=int(month)).order_by('-date')

    def get_page(self):
        return self.get_query_set().filter(type='page', status='publish')
