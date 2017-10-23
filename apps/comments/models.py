# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logreg_app.models import User

# a manager for validating comments very basic atm can add more validations like making sure a user isnt commenting on their own page
class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['content']) == 0:
            errors["empty_comment"] = "You can't leave a blank comment"
        return errors

# comment database table has content and a user recipient and user author
class Comment(models.Model):
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, related_name="commentsWritten")
    recipient = models.ForeignKey(User, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()