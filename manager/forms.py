from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'uid', 'placeholder': u'用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': u'密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, widget=forms.TextInput(
        attrs={"class": "form-control", 'id': 'username', 'onblur': 'authentication()', 'placeholder': '用户名'}))
    email = forms.EmailField(label='邮箱', max_length=320, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "required": "required"}),
                             error_messages={'invalid': '请输入有效的邮箱地址'})
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '密码'}))
    password2 = forms.CharField(label='密码确认',
                                widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '重复密码'}))
