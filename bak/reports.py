from django_pandas.io import read_frame
from .models import So
import dtale

qs = So.objects.all()
df = read_frame(qs)
d = dtale.show(df)
d.open_browser()