from django.forms import ModelForm
from .models import Book, NoticeBoard,BookIssue


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

        self.fields['notice'].widget.attrs.update({'class': 'form-control'})


class BookIssueForm(ModelForm):
    class Meta:
        model = BookIssue
        fields = ['person_name', 'person_id', 'person_type',
                  'person_email', 'person_phone', 'return_date']

    def __init__(self, *args, **kwargs):
        super(BookIssueForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
