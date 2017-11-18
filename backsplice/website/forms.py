from django import forms

class ImportForm(forms.Form):
    def __init__(self, course_choices=(), *args, **kwargs):
        super(ImportForm, self).__init__(*args, **kwargs)

    doubleknot_roster = forms.FileField(
        widget=forms.FileInput(attrs={'accept':'.xls,.xlsx,.ods'}))

class ReviewUploadForm(forms.Form):
    def __init__(self, course_choices=(), *args, **kwargs):
        super(ReviewUploadForm, self).__init__(*args, **kwargs)
        self.fields['courses'].choices = course_choices

    courses = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'checked':'checked'}),
        choices=())
