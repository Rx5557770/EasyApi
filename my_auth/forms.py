from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '邮箱必须填写',
            'invalid': '请输入有效的邮箱'
        },
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
            'class': 'form-input w-full p-3 rounded-lg bg-[#252636] border border-gray-700 text-white focus:border-[#7927F5] transition-colors',
             'placeholder': '请输入邮箱'
            })
    )

    password = forms.CharField(min_length=6, max_length=32, error_messages={
        'required': '密码不能为空'
    }, widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full p-3 rounded-lg bg-[#252636] border border-gray-700 text-white focus:border-[#7927F5] transition-colors',
        'placeholder': '请输入密码'
    }),label='密码'
    )

    password2 = forms.CharField(min_length=6, max_length=32, error_messages={
        'required': '密码不能为空'
    }, widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full p-3 rounded-lg bg-[#252636] border border-gray-700 text-white focus:border-[#7927F5] transition-colors',
        'placeholder': '请再次输入密码'
    }), label='确认密码'
    )


    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(username=email).first()
        if user:
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("密码不一致，请确认密码相同")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '邮箱必须填写',
            'invalid': '请输入有效的邮箱'
        },
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input w-full p-3 rounded-lg bg-[#252636] border border-gray-700 text-white focus:border-[#7927F5] transition-colors',
                'placeholder': '请输入邮箱'
            })
    )

    password = forms.CharField(min_length=6, max_length=32, error_messages={
        'required': '密码不能为空'
    }, widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full p-3 rounded-lg bg-[#252636] border border-gray-700 text-white focus:border-[#7927F5] transition-colors',
        'placeholder': '请输入密码'
    }), label='密码')


    def clean_email(self):
        # 将邮箱当作django默认User表中的username
        email = self.cleaned_data['email']
        user = User.objects.filter(username=email).exists()
        if not user:
            raise forms.ValidationError('账号未注册')
        return email

