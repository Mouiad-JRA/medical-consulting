from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

from .models import User, Consultation, Person


class ConsultationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['consultation_text'].label = _("consultation text")
        self.fields['medical_history'].label = _("medical history")
        self.fields['medical_history'].widget.attrs.update(
            {
                'placeholder': 'Enter Your medical history',
            }
        )
        self.fields['consultation_text'].widget.attrs.update(
            {
                'placeholder': 'Enter Your consultation text',
            }
        )

    class Meta:
            model = Consultation
            fields = ['medical_history', 'consultation_text', 'reply']
            error_messages = {
                'medical_history': {
                    'required': 'medical history is required'
                },
                'consultation_text': {
                    'required': 'consultation text is required'
                }
            }
            exclude = ('reply',)

    def save(self, commit=True):
        consultation = super(ConsultationForm, self).save(commit=False)
        user = User.objects.get(email=self.request.user.email)

        if commit:
            consultation.save()
        user.consultation = consultation
        user.save()
        return consultation

    def clean_medical_history(self):
        medical_history = self.cleaned_data.get('medical_history')
        if not medical_history:
            raise forms.ValidationError("medical history is required")
        return medical_history

    def clean_consultation_text(self):
        consultation_text = self.cleaned_data.get('consultation_text')
        if not consultation_text:
            raise forms.ValidationError("consultation text is required")
        return consultation_text


class PatientRegistrationForm(UserCreationForm):
    captcha = CaptchaField()
    medical_history = forms.CharField(max_length=255,
                                      widget=forms.Textarea(
                                          attrs={"class": "form-control", "placeholder": "medical history"}
                                      ),
                                      error_messages={"required": "Please fill in the details."},
                                      )
    consultation_text = forms.CharField(max_length=255,
                                        widget=forms.Textarea(
                                            attrs={"class": "form-control", "placeholder": "consultation text"}
                                        ),
                                        error_messages={"required": "Please fill in the details."},
                                        )

    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = _("First Name")
        self.fields['last_name'].label = _("Last Name")
        self.fields['email'].label = _("Email")
        self.fields['age'].label = _("age")

        self.fields['phone_number'].label = _("Phone Number")
        self.fields['password1'].label = _("Password")
        self.fields['password2'].label = _("Confirm Password")
        self.fields['consultation_text'].label = _("consultation text")
        self.fields['medical_history'].label = _("medical history")
        self.fields['captcha'].label = _("captcha")
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )
        self.fields['age'].widget.attrs.update(
            {
                'placeholder': 'Enter Age',
            }
        )
        self.fields['consultation_text'].widget.attrs.update(
            {
                'consultation_text': 'consultation text',
            }
        )
        self.fields['medical_history'].widget.attrs.update(
            {
                'placeholder': 'medical history',
            }
        )

        self.fields['captcha'].widget.attrs.update(
            {
                'placeholder': 'Enter The above captcha text',
            }
        )

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'phone_number', 'age', 'password1', 'password2', 'gender',
                  'consultation_text', 'medical_history', 'captcha']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'gender': {
                'required': 'Gender is required'
            },
            'age': {
                'required': 'age is required'
            },
        }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age:
            raise forms.ValidationError("age is required")
        return age

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        consultation = Consultation.objects.create(
            consultation_text=self.cleaned_data.get('consultation_text'),
            medical_history=self.cleaned_data.get('medical_history')
        )

        user.role = "patient"
        user.consultation = consultation
        user.username = user.email
        if commit:
            user.save()
        return user


class DoctorRegistrationForm(UserCreationForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = _("First Name")
        self.fields['last_name'].label = _("Last Name")
        self.fields['password1'].label = _("Password")
        self.fields['password2'].label = _("Confirm Password")
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )
        self.fields['captcha'].widget.attrs.update(
            {
                'placeholder': 'Enter The above captcha text',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'captcha']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': ' First Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "doctor"
        user.username = user.email
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].label = _("Email")
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(self.request, username=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class PatientProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PatientProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        )
        self.fields['age'].widget.attrs.update(
            {
                'placeholder': 'Age',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "age", "phone_number"]


class DoctorProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].label = _("age")
        self.fields['chest_pain_type'].label = _("chest pain type")
        self.fields['rest_electro'].label = _("rest electro")
        self.fields['rest_blood_pressure'].label = _("rest blood pressure")
        self.fields['max_heart_rate'].label = _("max heart rate")
        self.fields['blood_sugar'].label = _("blood sugar")
        self.fields['exercice_angina'].label = _("exercice angina")
        self.fields['chest_pain_type'].widget.attrs.update(
            {
                'placeholder': _('Choose chest pain type'),
            }
        )
        self.fields['rest_electro'].widget.attrs.update(
            {
                'placeholder': _('Choose rest electro'),
            }
        )
        self.fields['rest_blood_pressure'].widget.attrs.update(
            {
                'placeholder': _('Enter rest blood pressure'),
            }
        )
        self.fields['max_heart_rate'].widget.attrs.update(
            {
                'placeholder': _('Enter max heart rate'),
            }
        )
        self.fields['blood_sugar'].widget.attrs.update(
            {
                'placeholder': _('Enter blood sugar'),
            }
        )
        self.fields['exercice_angina'].widget.attrs.update(
            {
                'placeholder': _('Enter exercice angina'),
            }
        )
        self.fields['age'].widget.attrs.update(
            {
                'placeholder': _('Enter Age'),
            }
        )

    class Meta:
        model = Person

        fields = ['age', 'exercice_angina', 'blood_sugar', 'max_heart_rate', 'rest_blood_pressure', 'rest_electro',
                  'chest_pain_type',
                  ]
        error_messages = {
            'age': {
                'required': 'age is required'
            },
        }

    def save(self, commit=True):
        person = super(PersonForm, self).save(commit=False)
        if commit:
            person.save()
        return person
