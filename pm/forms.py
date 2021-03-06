from django import forms
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

from crm.models import Company, ContractItem
from pm.models import *
from wm.models import Article

class MachineCommentForm(forms.ModelForm):
	machine = forms.ModelChoiceField(
		queryset=Machine.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = MachineComment
		exclude = ['author',]

class MachineForm(forms.ModelForm):
	estimated_delivery_on = forms.DateField(required=False,
		label=_("Estimated delivery"),
		input_formats=['%d/%m/%Y',])

	class Meta:
		model = Machine
		exclude = ['project', 'contract_item',]

class MachineFromContractItemForm(forms.ModelForm):
	contract_item = forms.ModelChoiceField(
		queryset=ContractItem.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = Machine
		exclude = ['number', 'shipped_on', 'running_on', 'is_retired',]

class NewMachineForm(forms.ModelForm):
	project = forms.ModelChoiceField(
		queryset=Project.objects.all(),
		widget=forms.HiddenInput)
	estimated_delivery_on = forms.DateField(required=False,
		label=_("Estimated delivery"),
		input_formats=['%d/%m/%Y',])

	class Meta:
		model = Machine
		fields = ['project', 'model', 'description', 'estimated_delivery_on',]
	
class PartForm(forms.ModelForm):
	machine = forms.ModelChoiceField(queryset=Machine.objects.all(),
		widget=forms.HiddenInput)
	article = forms.ModelChoiceField(queryset=Article.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = Part
		fields = ['article', 'machine', 'quantity', 'function']

class ProjectForm(forms.ModelForm):
	company = forms.ModelChoiceField(
		queryset=Company.objects.filter(is_customer=True),
		label=_("Company")
		)

	class Meta:
		model = Project
		exclude = ['serial', 'old_model',]

	def save(self, force_insert=False, force_update=False, commit=True):
		m = super(ProjectForm, self).save(commit=False)
		if not m.serial:
			try:
				last_project = Project.objects.order_by("-serial")[0]
				n = int(last_project.serial)
				m.serial = str(n + 1).zfill(4)
			except IndexError:
				m.serial = '0001'
		if commit:
			m.save()
		return m

class MachineSelectForm(forms.Form):
	project = forms.ModelChoiceField(
		label=_('Project'),
		queryset=Project.objects.all()
	)
	machine_id = forms.IntegerField(
		label=_('Machine'),
		widget=forms.Select
	)

class CopyPartsForm(forms.Form):
	machine_to = forms.ModelChoiceField(
		queryset = Machine.objects.all(),
		widget = forms.HiddenInput
	)
	parts = forms.ModelMultipleChoiceField(
		label = _('Select parts'),
		queryset = Part.objects.none(),
		widget = forms.CheckboxSelectMultiple
	)

	def __init__(self, *args, **kwargs):
		source_id = kwargs.pop('source_id')
		super(CopyPartsForm, self).__init__(*args, **kwargs)
		self.fields['parts'].queryset = Part.objects.filter(
			machine__id=source_id
		)

class CECertificateForm(forms.ModelForm):
	project = forms.ModelChoiceField(
		queryset=Project.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = CECertificate
                fields = '__all__'

class TicketForm(forms.ModelForm):
	project = forms.ModelChoiceField(
		queryset=Project.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = Ticket
		exclude = ['updated_by',]

class TicketStatusForm(forms.ModelForm):
	status = forms.ChoiceField(choices=TICKET_STATUS, label="")
	
	class Meta:
		model = Ticket
		fields = ['status',]

class TicketItemForm(forms.ModelForm):
	ticket = forms.ModelChoiceField(
		queryset=Ticket.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = TicketItem
		exclude = ['created_by',]

class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        date_ph = attrs.get('date_placeholder')
        del attrs['date_placeholder']
        time_ph = attrs.get('time_placeholder')
        del attrs['time_placeholder']

        widgets = (forms.DateInput(
            attrs={'placeholder': date_ph}, format=date_format),
            forms.TimeInput(
            attrs={'placeholder': time_ph}, format=time_format))
        super(forms.SplitDateTimeWidget, self).__init__(widgets, attrs)

class InterventionForm(forms.ModelForm):
    machine = forms.ModelChoiceField(
        queryset=Machine.objects.all(),
        widget=forms.HiddenInput)
    start_at = forms.DateTimeField(label=_("start at"),
        widget=SplitDateTimeWidget(
        attrs={'date_placeholder': _('dd/mm/yy'),
            'time_placeholder': _('HH:MM')},
            date_format="%d/%m/%y",
            time_format="%H:%M"))
    end_at = forms.DateTimeField(label=_("end at"),
        widget=SplitDateTimeWidget(
        attrs={'date_placeholder': _('dd/mm/yy'),
            'time_placeholder': _('HH:MM')},
            date_format="%d/%m/%y",
            time_format="%H:%M"))
    
    class Meta:
        model = Intervention
        fields = ['machine', 'employee', 'start_at', 'end_at']

class ImportInterventionsForm(forms.Form):
    csv_file = forms.FileField(label=_("csv file"))


