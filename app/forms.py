from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import AIModel, Project, Run


# Create your forms here.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewAIModelForm(forms.Form):
    model_name = forms.CharField(required=True,
                                 label='Model Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    code_file = forms.FileField(required=True,
                                label='Code File',
                                widget=forms.FileInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(required=True,
                             label='Type',
                             choices=AIModel.ModelType.choices,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, user, commit=True):
        """
        set user and save model
        :param user:
        :param commit:
        :return:
        """
        model = AIModel(user=user,
                        code_file=self.cleaned_data['code_file'],
                        model_name=self.cleaned_data['model_name'],
                        type=self.cleaned_data['type'])
        if commit:
            model.save()
        return model

    def is_valid(self, user):
        """
        check if model name is unique for user
        :return:
        """
        valid = super(NewAIModelForm, self).is_valid()
        if not valid:
            return valid
        if not self.cleaned_data['code_file'].name.endswith('.py'):
            self.add_error('code_file', 'Code file must be a .py file')
            return False
        if AIModel.objects.filter(user=user, model_name=self.cleaned_data['model_name']).exists():
            self.add_error('model_name', 'Model name must be unique')
            return False
        return True


class NewProjectForm(forms.Form):
    data_name = forms.CharField(required=True,
                                label='Data Name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_file = forms.FileField(required=True,
                                label='Data File',
                                widget=forms.FileInput(attrs={'class': 'form-control'}))
    target_data_file = forms.FileField(required=True,
                                       label='Target Data File',
                                       widget=forms.FileInput(attrs={'class': 'form-control'}))

    def save(self, model, commit=True):
        """
        set model and save project
        :param model:
        :param commit:
        :return:
        """
        project = Project(model=model,
                          data_file=self.cleaned_data['data_file'],
                          data_name=self.cleaned_data['data_name'],
                          target_data_file=self.cleaned_data['target_data_file'])
        if commit:
            project.save()
        return project

    def is_valid(self, model):
        """
        check if data name is unique for model
        :param model:
        :return:
        """
        valid = super(NewProjectForm, self).is_valid()
        if not valid:
            return valid
        if Project.objects.filter(model=model, data_name=self.cleaned_data['data_name']).exists():
            self.add_error('data_name', 'Data name already exists')
            return False
        if not self.cleaned_data['data_file'].name.endswith('.npy'):
            self.add_error('data_file', 'Data file must be a .npy file')
            return False
        if not self.cleaned_data['target_data_file'].name.endswith('.npy'):
            self.add_error('target_data_file', 'Target data file must be a .npy file')
            return False
        return True


class NewRunForm(forms.Form):
    split_ratio = forms.FloatField(required=True,
                                   label='Split Ratio',
                                   widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                   'step': '0.01',
                                                                   'min': '0',
                                                                   'max': '1',
                                                                   'value': '0.8'}))
    type = forms.ChoiceField(required=True,
                             label='Type',
                             choices=Run.RunType.choices,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, project, commit=True):
        """
        set project and save run
        :param project:
        :param commit:
        :return:
        """
        run = Run(project=project,
                  type=self.cleaned_data['type'],
                  split_ratio=self.cleaned_data['split_ratio'])
        if commit:
            run.save()
        return run

    def is_valid(self):
        """
        check if split ratio is between 0 and 1
        :return:
        """
        valid = super(NewRunForm, self).is_valid()
        if not valid:
            print("Err::", self.errors)
            return valid
        if not 0 <= self.cleaned_data['split_ratio'] <= 1:
            self.add_error('split_ratio', 'Split ratio must be between 0 and 1')
            return False
        return True
