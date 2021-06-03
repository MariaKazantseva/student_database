from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Classes


class ClassesForm(ModelForm):
    class Meta():
        model = Classes
        fields = "__all__"

    def clean(self):
        super().clean()
        if self.cleaned_data['type'] == 'i':
            if not 'students' in self.cleaned_data or self.cleaned_data['students'].count() > 1:
                raise ValidationError({'students': _('One student only')})
