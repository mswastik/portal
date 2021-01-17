from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Div,Field,Fieldset,HTML,ButtonHolder,Row,Button
from crispy_forms.bootstrap import InlineField,FormActions
from django.forms.models import inlineformset_factory,BaseInlineFormSet
from .custom_layout_object import Formset
from django_select2.forms import Select2Widget,ModelSelect2Widget
from datetime import datetime  
from django.contrib.admin.widgets import FilteredSelectMultiple


class DateInput(forms.DateInput):
    input_type = 'date'

class SoWidget(ModelSelect2Widget):
    model = So
    search_fields = [
        'so__icontains',
        'fgcode__code__icontains',
        'fgcode__desc__icontains',
    ]

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'    
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit Plan'))

class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))

class SpeedForm(forms.ModelForm):
    class Meta:
        model = Speed
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'   
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_method = 'post'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'
    #helper.field_class = 'form-group-sm form-control-sm input-sm'
    #helper.form_class = 'form-group-sm form-control-sm input-sm'
    #helper.label_class = 'form-group-sm form-control-sm input-sm'    
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'    
    helper.form_method = 'post'
    #helper.form_class='form-control mt-0'
    helper.add_input(Submit('submit', 'Submit'))

class ProductionForm1(forms.ModelForm):
    class Meta:
        model = Production
        exclude=()
        widgets = {
            'so': SoWidget
        }
    #helper = FormHelper()
    #helper.template = 'bootstrap4/table_inline_formset.html'    
    #helper.form_method = 'post'
    #helper.add_input(Submit('submit', 'Submit'))

class DispatchForm1(forms.ModelForm):
    class Meta:
        model = Dispatch
        exclude=()
        widgets = {
            'so': SoWidget
        }

class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'    
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))
 

class SoForm(forms.ModelForm):
    class Meta:
        model = So
        fields='__all__'
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'    
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))
    '''
    def __init__(self, *args, **kwargs):
        super(SoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_tag = True
        #self.helper.field_class = 'col-lg-12'
        #self.helper.form_class = 'form-inline'
        self.helper.template = 'bootstrap4/table_inline_formset.html'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['so_date'].widget = DateInput()
        self.fields['act_disp_date'].widget = DateInput()
        #self.fields['fgcode'].widget = ProductWidget()
        #self.helper.layout = Layout(Field('code',css_class="controls col-lg-12")) '''

class SoForm1(forms.ModelForm):
    class Meta:
        model = So
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html' 
    #helper.form_class = 'form-sm'     
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))

class BOMForm(forms.ModelForm):
    class Meta:
        model = BOM
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))
    #FilteredSelectMultiple("verbose name", is_stacked=False)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'    
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))
    
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude=()
    helper = FormHelper()
    helper.template = 'bootstrap4/table_inline_formset.html'    
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Submit'))
    helper.add_input(Button('delete', 'Delete'))
    helper.layout = Layout(FormActions(
        HTML("""{% if object %}
                &lt;a href="{% url "ticket-delete" object.id %}"
                class="btn btn-outline-danger pull-right"&gt;
                Delete &lt;i class="fa fa-trash-o" aria-hidden="true"&gt;&lt;/i&gt;&lt;/button&gt;&lt;/a&gt;
                {% endif %}"""),
    )
)