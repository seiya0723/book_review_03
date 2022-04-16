from django import forms 
from .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model   = Book
        fields  = [ "isbn","category","title","author","description","published","thumbnail","info" ]

class BookAdminForm(forms.ModelForm):

    class Meta:
        model   = Book
        fields  = [ "isbn","dt","category","title","author","description","published","thumbnail","info" ] #dtも編集できるように追加しておく

    description = forms.CharField(  widget = forms.Textarea(attrs={ "maxlength":str(Book.description.field.max_length),  } ),
                                    label = Book.description.field.verbose_name,
                                    required = False,     #説明文の未入力を許可する
                                    )


