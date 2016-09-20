import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, Dropdown
from bokeh.io import curdoc


# import the data
df = pd.read_csv(r'H:\Sources\Short analysis\bokeh\tweets.csv')
df = df[['user_screen_name', 'created_at', 'tweet']]
df = df.set_index(pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S', errors='coerce'))

df = df.dropna()

# Create the source for the plot
source_plot = ColumnDataSource(data=dict(time=[], value=[]))

# Create figure, add the line
p = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset",  y_axis_location="right")
p.line(x='time', y='value', source=source_plot)


# Function that updates the source. The figure will be automatically updated when the source_plot is triggered
def update_plot():
    a = df['tweet'].groupby(pd.TimeGrouper('{}{}'.format(slider_number_groupby.value,
                                                         dropdown_cat_groupby.value))).count()
    # So here we adjust the source_data itself
    source_plot.data = {
        'time': a.index,
        'value': a.values
    }
    # And here we trigger the figure!
    source_plot.trigger('data', source_plot.data, source_plot.data)


# Making a nice slider, so that we can select the number of hours to combine
slider_number_groupby = Slider(title="Groupby", start=1, end=60, value=1, step=1)
slider_number_groupby.on_change('value', lambda attr, old, new: update_plot())

menu = [('Minutes', 'min'), ('Hours', 'h'), ('Days', 'D')]
dropdown_cat_groupby = Dropdown(label='Grouped', menu=menu, value='h')
dropdown_cat_groupby.on_change('value', lambda attr, old, new: update_plot())


# Create the first plot
update_plot()

# Add the plot and slider to the windows
curdoc().add_root(
                 row(
                     column(slider_number_groupby, dropdown_cat_groupby),
                     p
                     )
                     )
