from django.forms import ModelForm
from .models import Book, NoticeBoard

class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['id']
        
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class NoticeBoardForm(ModelForm):
    class Meta:
        model = NoticeBoard
        fields = ['notice']

    def __init__(self, *args, **kwargs):
        super(NoticeBoardForm, self).__init__(*args, **kwargs)

        self.fields['notice'].widget.attrs.update({'class':'form-control'})