from django import forms

from .models import Item


INPUT_CLASSES = "w-full py-4 px-6 rounded-xl border"


class NewItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = (
            'Category',
            'name',
            'description',
            'price',
            'image',
        )

        widgets = {
            'Category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),

            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),

            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),

            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'min': '0.01',
                'step': '0.01',
            }),

            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # Limit the image size to 5 MB.
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Image size must not exceed 5 MB."
                )

            # Allow only JPEG, PNG, and WebP images.
            allowed_types = [
                'image/jpeg',
                'image/png',
                'image/webp',
            ]

            if image.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Only JPEG, PNG, and WebP images are allowed."
                )

        return image


class EditItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = (
            'name',
            'description',
            'price',
            'image',
            'is_sold',
        )

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),

            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),

            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'min': '0.01',
                'step': '0.01',
            }),

            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # Limit the image size to 5 MB.
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Image size must not exceed 5 MB."
                )

            # Allow only JPEG, PNG, and WebP images.
            allowed_types = [
                'image/jpeg',
                'image/png',
                'image/webp',
            ]

            if image.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Only JPEG, PNG, and WebP images are allowed."
                )

        return image