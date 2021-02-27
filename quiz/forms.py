from django import forms
from django.forms.widgets import RadioSelect


class QuestionForm(forms.Form):
    def __init__(self, question,my_ques, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        print(my_ques)
        for ques in my_ques:

            choice_list = [x for x in ques.get_answers_list()]
            print(choice_list)

            print(str(ques))
            print()
            self.fields['custom_%s'%ques] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)
