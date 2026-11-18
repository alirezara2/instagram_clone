from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    """مدل پست (عکس یا ویدیو با کپشن)"""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    caption = models.TextField('کپشن', max_length=2200, blank=True)
    
    # برای سادگی، عکس و ویدیو رو جدا گذاشتیم (میشه فقط یکی پر بشه)
    image = models.ImageField('عکس', upload_to='posts/images/', blank=True, null=True)
    video = models.FileField('ویدیو', upload_to='posts/videos/', blank=True, null=True)
    
    created_at = models.DateTimeField('تاریخ انتشار', default=timezone.now)
    updated_at = models.DateTimeField('آخرین بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['-created_at']  # جدیدترین پست‌ها اول نمایش داده بشن

    def __str__(self):
        # type: ignore برای نادیده گرفتن هشدار Pylance در مورد فیلد id
        return f"پست {self.author.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Comment(models.Model):
    """مدل کامنت برای پست‌ها"""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    text = models.TextField('متن کامنت', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # قدیمی‌ترین کامنت‌ها اول

    def __str__(self):
        return f"کامنت {self.author.email} روی پست {self.post.id}"  # type: ignore


class Like(models.Model):
    """مدل لایک برای پست‌ها"""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # هر کاربر فقط یک بار می‌تونه یک پست رو لایک کنه
        unique_together = ('post', 'user')

    def __str__(self):
        return f"لایک {self.user.email} روی پست {self.post.id}"  # type: ignore