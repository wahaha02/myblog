from django.db import models
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

class CommentManager(models.Manager):

    def in_public(self):
        return self.get_query_set().filter(is_public = True, is_removed = False).order_by('-date')

    def in_moderation(self):
        """
        QuerySet for all comments currently in the moderation queue.
        """
        return self.get_query_set().filter(is_public=False, is_removed=False)

    def get_depth_odd(self, depth):
        "Post"
        pass

    def get_sorted_comments(self, qs):
        def sort_comment(root, list, sorted):
            sorted.append(root)
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                for child in children:
                    sort_comment(child, list, sorted)
            elif len(list) > 0 and root.is_last_child():
                sort_comment(list[0], list, sorted)

        comments = list(qs)
        if comments:
            sorted = []
            first = comments[0]
            print comments
            sort_comment(first, comments, sorted)

            return sorted
        else:
            return comments

    def get_children_by_id(self, id):
        list = []
        comments = self.get_query_set().filter(is_public = True, is_removed = False).order_by('date')
        for comment in comments:
            if comment.parent_id == id:
                list.append(comment)

        return list

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct, is_public = True)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()), is_public = True)
        return qs

