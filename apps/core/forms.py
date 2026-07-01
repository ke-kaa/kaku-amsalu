from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    # Honeypot: real users never see/fill this; bots do.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactSubmission
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell me about your project…", "rows": 5}),
        }

    def is_spam(self):
        """True when the honeypot was filled."""
        return bool(self.cleaned_data.get("website"))
