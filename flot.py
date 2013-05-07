#!/usr/bin/env python

import os

flotgit="https://github.com/flot/flot.git"
flotdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "flot")
flotreldir=os.path.relpath(flotdir)

if not os.path.exists(flotdir):
    os.system("git clone %s %s"%(flotgit, flotreldir))

if not os.path.exists(flotdir):
    print "flot does not exist. please do \"git clone %s\""%flotgit

class PlotData:
    BAR="bars"
    LINE="lines"
    POINT="points"
    
    TYPES=[BAR, LINE, POINT]
    
    def __init__(self, plottype, data):
        if plottype not in PlotData.TYPES:
            print "Invalid plottype %s"%plottype
            sys.exit(1)
        self.plottype = plottype
        self.data = data

    def __str__(self):
        return """{{data: {data},{plottype}: {{ show: true }} }}""".format(plottype=self.plottype, data=str(self.data))

class Plot:
    def __init__(self, title):
        self.title = title
        self.xlabels = []
        self.ylabels = []
        self.bardata = PlotData(PlotData.BAR, [])
        self.linedata = PlotData(PlotData.LINE, [])
        self.pointdata = PlotData(PlotData.POINT, [])
        self.plotdata = [self.bardata, self.linedata, self.pointdata]

    def AddData(self, plottype, x, y):
        if plottype == PlotData.BAR:
            self.bardata.data.append([x,y])
        elif plottype == PlotData.LINE:
            self.linedata.data.append([x,y])
        elif plottype == PlotData.POINT:
            self.pointdata.data.append([x,y])
        else:
            print "ERROR: AddData invalid plottype %s"% plottype
            sys.exit(1)

    def AddXLabel(self, x, label):
        self.xlabels.append([x, label,])

    def AddYLabel(self, y, label):
        self.ylabels.append([y, label,])

    def xlabelStr(self):
        if self.xlabels:
            return """, xaxis: {{ticks: {labels} }}""".format(labels=str(self.xlabels))
        else:
            return ""

    def ylabelStr(self):
        if self.ylabels:
            return """, yaxis: {{
ticks: {labels}
}}""".format(labels=str(self.ylabels))
        else:
            return ""
        
    def __str__(self):
        page = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{title}</title>
<link href="{flotdir}/examples/examples.css" rel="stylesheet" type="text/css">
<!--[if lte IE 8]><script language="javascript" type="text/javascript" src="{flotdir}/excanvas.min.js"></script><![endif]-->
<script language="javascript" type="text/javascript" src="{flotdir}/jquery.js"></script>
<script language="javascript" type="text/javascript" src="{flotdir}/jquery.flot.js"></script>
<script language="javascript" type="text/javascript" src="{flotdir}/jquery.flot.navigate.js"></script>
<script type="text/javascript">
$(function() {{
$.plot("#placeholder", {plotdata}, {{ series: {{
}}
{xlabel} {ylabel}
}}
);
}});
</script>
</head>
<body>

<div id="header">
<h2>{title}</h2>
</div>

<div id="content">

<div class="demo-container">
<div id="placeholder" class="demo-placeholder"></div>
</div>

</body>
</html>
""".format(title=self.title, flotdir=flotreldir, plotdata="[%s]"%(",".join(map(str, self.plotdata)),), xlabel=self.xlabelStr(), ylabel=self.ylabelStr())
        return page

if __name__ == "__main__":
    filename="test.html"
    p = Plot("TEST test")
    p.AddData(PlotData.BAR, 0, 1)
    p.AddData(PlotData.BAR, 3, 5)
    p.AddData(PlotData.LINE, 3, 5)
    p.AddData(PlotData.LINE, 4, 6)
    p.AddXLabel(0, "xlabel1")
    p.AddXLabel(3, "xlabel2")
    p.AddYLabel(2, "ylabel1")
    
    with open(filename, "w") as f:
        f.write(str(p))
    
