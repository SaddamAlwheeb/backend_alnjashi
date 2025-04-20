from django.db import models

class CommentState(models.IntegerChoices):
    positive=1, 'Positive',
    negative=2, 'Negative',
    neutral=3, 'Neutral',   