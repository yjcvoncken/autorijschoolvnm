from django import forms
from .models import ContactRequest, Package


class ContactRequestForm(forms.ModelForm):
    package = forms.ModelChoiceField(
        label="Pakket (optioneel)",
        queryset=Package.objects.none(),
        required=False,
        empty_label="Nog geen pakket gekozen",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["package"].queryset = Package.objects.filter(active=True)

    class Meta:
        model = ContactRequest
        fields = ["name", "phone", "email", "package", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Jouw naam"}),
            "phone": forms.TextInput(attrs={"placeholder": "06 12345678"}),
            "email": forms.EmailInput(attrs={"placeholder": "naam@email.nl"}),
            "message": forms.Textarea(attrs={"placeholder": "Vertel ons kort waar je naar op zoek bent..."}),
        }
