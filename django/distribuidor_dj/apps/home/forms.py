from django import forms


# creating a form
class TrackingForm(forms.Form):
    tracking_id = forms.UUIDField(
        label="",
        required=True,
        error_messages={
            "required": "Por favor, ingresa un tracking",
            "invalid": "Tracking inválido",
        },
        widget=forms.TextInput(
            attrs={
                "class": "input input-primary input-bordered w-full",
                "placeholder": "Inserte su tracking",
            }
        ),
    )
