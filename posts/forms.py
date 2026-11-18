from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    """فرم ساخت پست (عکس یا ویدیو)"""
    class Meta:
        model = Post
        fields = ('caption', 'image', 'video')
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'کپشن خود را بنویسید...'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        
        if not image and not video:
            raise forms.ValidationError('حداقل باید یک عکس یا یک ویدیو آپلود کنید.')
            
        return cleaned_data

class CommentForm(forms.ModelForm):
    """فرم کامنت"""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کامنت خود را بنویسید...'}),
        }