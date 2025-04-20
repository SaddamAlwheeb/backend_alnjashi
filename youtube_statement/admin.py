from django.contrib import admin
from .models import *
from utlis.utils import get_youtube_comments

# Register your models here.
admin.site.register(Comment)
admin.site.register(Channel)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'youtube_id','view_count']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:  # فقط عند الإضافة الجديدة
            try:
                print(f"جلب للفديوا رقم : {obj}")
                # تأكد أنك ترسل youtube_id الصحيح
                items = get_youtube_comments(obj.youtube_id)
                print(f"جلب للفديوا رقم : {obj.youtube_id}")
                if items:
                    comments_to_create = []
                    for item in items:
                        snippet = item['snippet']['topLevelComment']['snippet']
                        comments_to_create.append(Comment(
                            video=obj,
                            youtube_id=item['id'],
                            comment_text=snippet['textDisplay'],
                            author_name=snippet['authorDisplayName'],
                            author_channel_id=snippet.get('authorChannelId', {}).get('value'),
                            like_count=snippet.get('likeCount', 0),
                        ))
                    
                    # حفظ دفعي للتعليقات
                    Comment.objects.bulk_create(comments_to_create, ignore_conflicts=True)

            except Exception as e:
                print(f"تعذر جلب أو حفظ التعليقات: {e}")