from VideoCapture2 import df, avgContour, frameCount
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(x_axis_type="datetime", height=200, width=500, sizing_mode='scale_width', title="Motion Graph")
p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_num_ticks = 1

f = figure(height=400, width=500, sizing_mode='scale_width', title='Active Pixel Area')
f.step(frameCount, avgContour)
f.ygrid[0].ticker.desired_num_ticks = None


b = figure(height=400, width=500, sizing_mode='scale_width', title='Active Pixel Area 2')
b.vbar(x=frameCount, width=0.5, bottom=0, top=avgContour, color="green")
b.ygrid[0].ticker.desired_num_ticks = None

hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

q = p.quad(left="Start", right="End", bottom=0, top="ExitArea", color="green", source=cds)


output_file(r"E:\School Work\Code\PythonFaceDetector\timeGraph.html")
show(column(p, f, b))
