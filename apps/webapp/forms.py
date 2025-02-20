from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Film, Planet, Vehicle, SentientBeing, Language


class FilmForm(forms.ModelForm):
    """Form created for updating Film entity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Film
        fields = "__all__"


class PlanetForm(forms.ModelForm):
    """Form created for updating Film entity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Planet
        fields = "__all__"


class VehicleForm(forms.ModelForm):
    """Form created to edit Vehicle entity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Vehicle
        fields = "__all__"


class SentientBeingForm(forms.ModelForm):
    """Form created to edit Sentient Being entity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = SentientBeing
        fields = "__all__"


class LanguageForm(forms.ModelForm):
    """Form created to edit Language entity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Language
        fields = "__all__"
