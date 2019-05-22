import plotly.plotly as py
import plotly.figure_factory as ff

import numpy as np

x = np.random.randn(1000)  
hist_data = [x]
group_labels = ['distplot']

fig = ff.create_distplot(hist_data, group_labels)
py.plot(fig, filename = 'basic-line', auto_open=True)
