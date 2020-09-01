from django import forms

from .models import Events, Puples, DaysTask


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ("date", "name", "organization", "verification_file")


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ("event_rate", "check",)


class ImgChangeForm(forms.ModelForm):
    class Meta:
        model = Puples
        fields = ("image",)


class AnswerTask(forms.ModelForm):
    class Meta:
        model = DaysTask
        fields = ("result",)


class CollectData(forms.ModelForm):
    class Meta:
        model = Puples
        fields = ("email", "phone")

class Notifications(forms.ModelForm):
    theme = forms.CharField(label="Тема")
