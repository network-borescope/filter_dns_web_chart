import os, sys, getopt

filename = None
collisions = None
try:
    opts, args = getopt.getopt(sys.argv[1:],"f:c:",["file=","collisions="])
except getopt.GetoptError as err:
    print(err)
    print('HINT: csvToChart.py -f <filename>')
    print('HINT: csvToChart.py -f <filename> -c <collisions>')
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-f", "--file"):
        filename = arg
    if opt in ("-c", "--collisions"):
        collisions = int(arg)
if(filename == None):
    print("Error: Missing Argument")
    print('HINT: csvToChart.py -f <filename>')
    sys.exit(1)

fin = open(filename, "r")
header = fin.readline()

try:
    os.mkdir(filename[:-4])
except FileExistsError:
    pass


# Construindo o gráfico

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import ceil

BARS_PER_CHART = 40

def autolabel(rects):
    #Attach a text label above each bar in *rects*, displaying its height.
    for rect in rects:
        height = rect.get_height() # height of the bar
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

labels = []
values = []
higher_value = 0

for line in fin:
    splitAt = line.rfind(";")
    key, value = line[:splitAt], int(line[splitAt+1:])
    key = key.replace(";", "\n")
    if collisions != None and value >= collisions:
        labels.append(key)
        values.append(value)
    if value > higher_value: higher_value = value

qtd_values = len(values)

qtd_plots = ceil(qtd_values / BARS_PER_CHART) # arredonda pra cima
chart_height = 30

begin = 0
end = BARS_PER_CHART

group_by = "Group By sip | ttl | domain"

for i in range(qtd_plots):
    # cada gráfico gerado terá no máximo BARS_PER_CHART barras
    try:
        y = values[begin:end]
        x_labels = labels[begin:end]
    except IndexError:
        y = values[begin:]
        x_labels = labels[begin:]
    begin = end
    end += BARS_PER_CHART
    
    plt.rcParams.update({'font.size': 20})
    chart_width = 1.9*len(y)
    if chart_width < 10: chart_width = 10
    plt.rcParams['figure.figsize'] = [chart_width, chart_height]

    x = np.arange(len(x_labels))
    width = 0.7 # the width of the bars
    fig, ax = plt.subplots()
    rect = ax.bar(x, y, width)

    ax.set_ylabel('Collisions')
    
    ax.set_xlabel(group_by)
    ax.set_title(filename)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_ylim([0, higher_value + 0.1*higher_value])

    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    
    autolabel(rect)
    
    if i + 1 < 10: plt.savefig(filename[:-4] + "/" + filename[:-4]+"_pt0{}.png".format(i+1))
    else: plt.savefig(filename[:-4] + "/" + filename[:-4]+"_pt{}.png".format(i+1))


fin.close()
