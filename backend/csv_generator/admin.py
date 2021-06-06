from django import forms
from django.contrib import admin

from .models import *


admin.site.unregister(get_user_model())


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'is_superuser', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(get_user_model())
class CustomAdmin(admin.ModelAdmin):
    form = UserCreationForm
    add_form = UserCreationForm
    fields = ('username', 'is_superuser', 'password')
