from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'uid', 'placeholder': u'用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': u'密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, widget=forms.TextInput(
            attrs={"class": "form-control", 'id': 'username', 'onblur': '', 'placeholder': '用户名'}))
    # email = forms.EmailField(label='邮箱', max_length=320, widget=forms.TextInput(
    #     attrs={"class": "form-control", 'id': 'email', "placeholder": "关联邮箱账号", "required": "required"}),
    #                          error_messages={'invalid': '请输入有效的邮箱地址'})
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(
                                        attrs={"class": "form-control", 'id': 'pw1', 'placeholder': '密码'}))
    password2 = forms.CharField(label='密码确认',
                                widget=forms.PasswordInput(
                                        attrs={"class": "form-control", 'id': 'pw2', 'placeholder': '重复密码'}))


class SettingForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, required=False, widget=forms.TextInput(
            attrs={"class": "form-control", 'id': 'username', 'onblur': '', 'width': '20px'}))
    sex = forms.ChoiceField(label='性别', choices=[('male', '男'), ('female', '女')],
                            widget=forms.Select(attrs={"class": "form-control", 'id': 'sex'}))
    profile = forms.CharField(label='签名', max_length=200, required=False, widget=forms.Textarea(
            attrs={'class': 'from-control', 'id': 'profile', 'cols': 28}))
