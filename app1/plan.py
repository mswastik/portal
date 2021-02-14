import pandas as pd
import numpy as np
import collections
from ortools.sat.python import cp_model

qs = So.objects.all()
ff=[f.name for f in So._meta.get_fields()]
ff.extend(['fgcode__'+k.name for k in Product._meta.get_fields()])
ff.remove('fgcode__so')
df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')