from django import forms
# from django.forms import ModelChoiceField
from .models import Incident

class IncidentForm(forms.ModelForm):

    class Meta:
        model = Incident
        fields = '__all__'

    def clean(self):

        status_type = self.cleaned_data['status_incident']
        affected = self.cleaned_data['services_afted']
        end_date = self.cleaned_data['finish_date_incidente']
        # reports = ModelChoiceField(queryset=None, label='reports', required=False)


        if status_type == 'rs':
            if not end_date:
                raise forms.ValidationError('Informe a data de conclusão do Incidente! ')

        # if affected.count() == 3:
        #     # print(reports.count(), "<<")
        #     print(reports.to_field_name)
        #     print(dir(reports))
        #     raise forms.ValidationError('Mude o status do incidente para "Em Análise"')