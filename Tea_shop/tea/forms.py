from django import forms
from django.utils.translation import ugettext_lazy as _


class PhoneWidget(forms.MultiWidget):

    def __init__(self, code_l, n_l, attrs=None, *args):
        widgets = [forms.TextInput(attrs={'size':code_l, 'maxlength': code_l}),
                   forms.TextInput(attrs={'size': n_l, 'maxlength': n_l}),]
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.code, value.number]
        return ['', '']

    def format_output(self, rendered_widgets):
        return '+38 (' + rendered_widgets[0] + ')' + rendered_widgets[1]


class PhoneField(forms.MultiValueField):
    def __init__(self, code_l, n_l, label, *args):
        list_fields = [forms.CharField(), forms.CharField()]
        super(PhoneField, self).__init__(list_fields, widget=PhoneWidget(code_l, n_l), label=label, *args)

    def compress(self, values):
        return '+38' + '(' + values[0] + ')' + values[1]


class CreateUserForm(forms.ModelForm):
    phone = PhoneField(3, 7, label=_('Телефон'))
    name = forms.CharField(max_length=100, label=_('Имя'))
    surname = forms.CharField(max_length=100, label=_('Фамилия'))
    address = forms.CharField(max_length=100, label=_('Адрес'))


class CreateProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField()
    photo = forms.ImageField()
