from django import forms
from core.models import DockerImage, DockerContainer, User
from core.utils import validate_pow

class DeployContainerForm(forms.Form):
    image = forms.ModelChoiceField(
        queryset=DockerImage.objects.filter(is_enabled=True),
        label="Select Image to deploy",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    pow = forms.CharField(
        max_length=255,
        label="Proof of Work",
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-5',
            'placeholder': 'Enter the full string that when hashed with MD5 gives the required result'
        })
    )

    def __init__(self, *args, **kwargs):
        running_image_ids = kwargs.pop('running_image_ids', [])
        self.required_result = kwargs.pop('required_result', None)
        super().__init__(*args, **kwargs)
        # TODO: Exclude running images for the same user
        # self.fields['image'].queryset = self.fields['image'].queryset.exclude(id__in=running_image_ids, )

    def clean(self):
        cleaned_data = super().clean()
        input_hash = cleaned_data.get('pow')
        if not input_hash:
            raise forms.ValidationError("Proof of Work is required")

        # TODO: check if image is already running for given user
        if not validate_pow(input_hash, self.required_result):
            raise forms.ValidationError("The Proof of Work is incorrect.")

        return cleaned_data

    def _validate_pow_for_image(self, input_hash):
        return validate_pow(input_hash)
    
class KillContainerForm(forms.Form):
    container_id = forms.CharField(
        widget=forms.HiddenInput()
    )
    magic_key = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['container_id'] = forms.CharField(
            widget=forms.HiddenInput()
        )
        self.fields['magic_key'] = forms.CharField(
            widget=forms.HiddenInput()
        )
    
    def clean(self):
        cleaned_data = super().clean()
        container_id = cleaned_data.get('container_id')
        if not container_id:
            raise forms.ValidationError("Container ID is required")
        
        user = User.objects.get(magic_key=cleaned_data.get('magic_key'))
        
        if not DockerContainer.objects.filter(id=container_id, allocated_to=user).exists():
            raise forms.ValidationError("Invalid Container ID")
        return cleaned_data
    
