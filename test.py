import altair as alt
from vega_datasets import data
import datapane as dp

source = data.cars()

plot1 = alt.Chart(source).mark_circle(size=60).encode(
    x='Horsepower', y='Miles_per_Gallon', color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).interactive()

dp.Report(
    dp.Plot(plot1),
    dp.DataTable(source)
).upload(name="My first report")

