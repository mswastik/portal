from django import forms
from .models import So,Plan,Line,Speed
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Div,Field,Fieldset,HTML,ButtonHolder,Row
from crispy_forms.bootstrap import InlineField
from django.forms.models import inlineformset_factory,BaseInlineFormSet
from .custom_layout_object import Formset


class DateInput(forms.DateInput):
    input_type = 'date'

class SoForm(forms.ModelForm):
    class Meta:
        model = So
        #fields=('closed','so','so_date','so_del_date','code','qty','customer','act_disp_qty','act_disp_date')
        localized_fields ='__all__'
        exclude=['currency','rate']
    def __init__(self, *args, **kwargs):
        super(SoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_tag = True
        #self.helper.field_class = 'col-md-4'
        #self.helper.form_class = 'form-inline'
        #helper.template = 'bootstrap4/table_inline_formset.html'
        self.helper.layout = Layout(
                    Row('so','so_date',
                        'customer',
                        'so_del_date','closed'),
                    Row(    
                        Field('qty'),
                        Field('act_disp_qty'),
                        Field('act_disp_date'),
                        'code',
                        ),
                    Row(
                        Fieldset('Add Plan',
                        Formset('plan')),
                    ),
                    #ButtonHolder(Submit('submit', 'Submit')),
                    )
        #self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Submit'))
        #self.fields['act_disp_date'].widget = DateInput()
        self.helper.render_required_fields = True


class PlanForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (PlanForm,self ).__init__(*args,**kwargs) # populates the post
        #self.fields['so'].queryset = So.objects.filter(closed=0).select_related('code').filter(plan__date__isnull=True)
        self.fields['so'].queryset = So.objects.filter(closed=0)
        self.helper = FormHelper()
    class Meta:
        model = Plan
        fields=('so','date','line')
        exclude=()
        localized_fields ='__all__'
        widgets = {
            'date': DateInput(),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_method = 'post'
    helper.template = 'bootstrap4/table_inline_formset.html'

class PlanForm1(forms.ModelForm):
    class Meta:
        model = Plan
        exclude=()
    def __init__(self, *args, **kwargs):
        super(PlanForm1, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Submit Plan'))

class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        exclude=()
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_method = 'post'

class SpeedForm(forms.ModelForm):
    class Meta:
        model = Speed
        exclude=()
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_method = 'post'

class SoForm2(forms.ModelForm):
    class Meta:
        model = So
        fields=('so','so_date','so_del_date','code','qty','customer','closed','act_disp_qty','act_disp_date')
        localized_fields ='__all__'
    def __init__(self, *args, **kwargs):
        super(SoForm2, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.template = 'bootstrap4/table_inline_formset.html'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['act_disp_date'].widget = DateInput()
        self.helper.render_required_fields = True
        self.helper.layout = Layout(
                    Field('so',readonly=True),
                        Field('so_date',readonly=True),
                        Field('code',readonly=True),
                        Field('customer',readonly=True))