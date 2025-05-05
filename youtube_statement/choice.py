from django.db import models

class CommentState(models.IntegerChoices):
    positive=1, 'Positive',
    negative=2, 'Negative',
    neutral=3, 'Neutral',   

class ChannelTypeStat(models.IntegerChoices):
    youtub=1, 'يوتيوب',
    x=2, 'تويتر',
    tiktok=3, 'تيك توك',   
