from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from captcha.fields import CaptchaField

from accounts.models import User, Consultation

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class ConsultationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
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

        # exclude = ['created_date']

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
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "medical history"}
        ),
        error_messages={"required": "Please fill in the details."},
    )
    consultation_text = forms.CharField(max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "consultation text"}
        ),
        error_messages={"required": "Please fill in the details."},
    )

    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email"
        self.fields['age'].label = "age"

        self.fields['phone_number'].label = "Phone Number"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['consultation_text'].label = "consultation text"
        self.fields['medical_history'].label = "medical history"
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
        if commit:
            user.save()
        return user


class DoctorRegistrationForm(UserCreationForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
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
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

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
