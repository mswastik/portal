from django import forms
from .models import So,Plan,Line
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout
from crispy_forms.bootstrap import InlineField
from django.forms.models import inlineformset_factory,BaseInlineFormSet

class SoForm(forms.ModelForm):
    class Meta:
        model = So
        fields=('closed','so','so_del_date','code','qty','customer')

class SoHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SoHelper, self).__init__(*args, **kwargs)
        self.template = 'bootstrap4/table_inline_formset.html'
        self.form_method = 'post'
        self.add_input(Submit('submit', 'Submit'))
        self.layout = Layout(
            'so',
            'so_del_date',
            InlineField('code',readonly=True),
            'qty',
            InlineField('closed'),
            InlineField('customer',readonly=True),
        )
        self.render_required_fields = True

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields=('so','date','line')
        localized_fields ='__all__'
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_method = 'post'
    helper.template = 'bootstrap4/table_inline_formset.html'

class PlanHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PlanHelper, self).__init__(*args, **kwargs)
        self.template = 'bootstrap4/table_inline_formset.html'
        self.add_input(Submit('submit', 'Submit'))
        self.form_method = 'post'
        self.layout = Layout(
            InlineField('so',readonly=True),
            'date',
            'line',
        )
        self.render_required_fields = True

class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        exclude=()
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_method = 'post'


class PlanForm1(forms.ModelForm):
    class Meta:
        model = Plan
        fields=('so','date','line')
    def __init__(self, *args, **kwargs):
        super(PlanForm1, self).__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'post'
        self.helper.template = 'bootstrap4/table_inline_formset.html'
        self.helper.layout = Layout(
                InlineField('so',readonly=True),
                'date',
                'line',
            )
        self.helper.render_hidden_fields = True
        self.helper.render_required_fields = True
