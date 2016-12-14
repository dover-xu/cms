from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'uid', 'placeholder': '手机号/邮箱'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': '密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, widget=forms.TextInput(
        attrs={'id': 'username', 'onblur': 'authentication()', 'placeholder': '手机号/邮箱'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '密码'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '重复密码'}))
