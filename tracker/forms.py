from django import forms
from tracker.models import Users, Skills, SkillMap
from django.utils.translation import gettext_lazy as _

class NewUserForm(forms.ModelForm):
    class Meta():
        model = Users
        fields = 'user_name','user_email'

class EditUserForm(forms.ModelForm):
    class Meta():
        model = Users
        fields = 'user_name','user_email', 'user_date_created'
        labels = {
            'user_name': _('Name'),
            'user_email': _('Email'),
            'user_date_created': _('Created On'),
        }

        widgets = {
            'user_email': forms.EmailInput(attrs={'readonly': True, 'class': 'grayedout_input_field', }, ),
            'user_date_created': forms.TextInput(attrs={'readonly': True, 'class': 'grayedout_input_field', }),
        }

        # help_texts = {
        #     'user_name': _('Some useful help text.'),
        # }

class NewSkillForm(forms.ModelForm):
    class Meta():
        model = Skills
        fields = 'skill_name','skill_description'


class EditSkillForm(forms.ModelForm):
    class Meta():
        model = Skills
        fields = 'skill_name', 'skill_description', 'skill_date_created'
        labels = {
            'skill_name': _('Name'),
            'skill_description': _('Description'),
            'skill_date_created': _('Created On'),
        }

        widgets = {
            'skill_date_created': forms.TextInput(attrs={'readonly': True, 'class': 'grayedout_input_field', }),
        }

        # help_texts = {
        #     'user_name': _('Some useful help text.'),
        # }


class EditSkillProfile(forms.ModelForm):
    class Meta():
        model = SkillMap
        fields = 'skillmap_user_id', 'skillmap_skill_id', 'skillmap_level'

    # def __init__ (self, user_id=None):
    #     # super(EditSkillProfile, self)
    #
    #     if user_id:
    #         print('here')
    #         self.objects.filter(skillmap_user_id=user_id)
    #     # labels = {
    #     #     'skill_name': _('Name'),
    #     #     'skill_description': _('Description'),
    #     #     'skill_date_created': _('Created On'),
    #     # }

        # widgets = {
        #     'skill_date_created': forms.TextInput(attrs={'readonly': True, 'class': 'grayedout_input_field', }),
        # }

        # help_texts = {
        #     'user_name': _('Some useful help text.'),
        # }
