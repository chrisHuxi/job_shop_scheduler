from typing import List, Optional, Dict
from topological_sort import TopologicalSort
from optimizer import SimulatedAnnealingOptimizer
from matplotlib.widgets import Button,RadioButtons
import matplotlib.pyplot as plt
import numpy as np
import glob


    
class Visualizator():
    """
    Handles all task related to plotting the schedules and the learning curve
    """
    def __init__(self, scheduleDict, total_time, iteration_index):
        self.scheduleDict = scheduleDict
        self.total_time = total_time
        self.iteration_index = iteration_index
        
    def avg(self, a, b):
        return (a + b) / 2.0
            
    def plot(self):
        plot_list = []
        for machine_idx in self.scheduleDict.keys():
            time_line = [-1]*self.total_time

            for span in self.scheduleDict[machine_idx]:
                #time_line[span.start:span.end] = span.operation.job
                for i in range(span.start,span.end):
                    time_line[i] = span.operation.job
            plot_list.append(time_line)
        #print(plot_list[4])
        fig = plt.figure(figsize=(20, 8))
        ax = fig.add_subplot(111)
        plt.subplots_adjust(left = 0.1, bottom = 0.2)
        ax.axes.get_yaxis().set_visible(False)
        #ax.set_aspect(1)
        for y, row in enumerate(plot_list):
            y1 = np.array([y, y])
            y2 = y1+1
            current_span_len = 0
            current_job_idx = -1
            #empty_flag = True
            last_col = -1
            x_start = 0
            for x, col in enumerate(row):
                #if (col == -1) and (current_span_len == 0): 
                if(col == -1) and (last_col == -1): #持续没东西
                    #empty_flag = True
                    last_col = col
                    continue
                elif (last_col == -1) and (last_col != col): #上边缘
                    x_start = x
                    current_job_idx = col
                    current_span_len =0 
                    last_col = col
                elif (last_col != -1) and (last_col == col): #持续有东西
                    current_span_len += 1
                    last_col = col
                elif (last_col != -1) and (col != -1) and (last_col != col): #一个schedule的上边缘 另一个的下边缘
                    x1 = np.array([x_start, (x_start + current_span_len)])
                    plt.fill_between(x1, y1, y2, color=( current_job_idx/20.0, 0.5, 0.8))
                    plt.text(self.avg(x1[0], x1[1]), self.avg(y1[0], y2[0]), str(current_job_idx), 
                                                    horizontalalignment='center',
                                                    verticalalignment='center')
                    current_span_len = 0
                    
                    x_start = x
                    current_job_idx = col
                    current_span_len =0 
                    last_col = col
                elif (col == -1) and (last_col != col): #下边缘
                    x1 = np.array([x_start, (x_start + current_span_len)])
                    plt.fill_between(x1, y1, y2, color=( current_job_idx/20.0, 0.5, 0.8))
                    plt.text(self.avg(x1[0], x1[1]), self.avg(y1[0], y2[0]), str(current_job_idx), 
                                                    horizontalalignment='center',
                                                    verticalalignment='center')
                    current_span_len = 0
                    last_col = col
                else:
                    print("---------------------")
        
        plt.ylim(len(plot_list),0)
        plt.xlim(0,self.total_time)
        
        #next_plot_button_axe = plt.axes([0.5,0.05,0.08,0.05]) #left, bottom, width, height
        #next_plot_button = Button(ax = next_plot_button_axe, label = "next iteration")
        
        plt.savefig("./image/"+str(self.iteration_index)+".png")
        plt.close()
        

class ButtonDisplayer:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.image_list = glob.glob(dir_name+"/*.png")
        self.index = 0
        self.fig =  plt.figure(figsize=(20, 8))
        
        self.image_axes = plt.axes([0.0, 0.0, 1.0, 1.0])
        self.button_axes = plt.axes([0.5,0.05,0.08,0.05])

    def click_button(self,event):
        if(self.index >= len(self.image_list) - 1):
            self.index = 0
        else:
            self.index += 1
        current_image = plt.imread(self.image_list[self.index])
        self.image_axes.imshow(current_image)
        self.fig.canvas.draw_idle()
        
            
    def display(self,learning_curve,temperature_curve):
        #plt.connect('button_press_event', self.click_button)
        current_image = plt.imread(self.image_list[self.index])
        self.image_axes.imshow(current_image)
        self.button_axes = Button(ax = self.button_axes, label = "next iteration")
        self.button_axes.on_clicked(self.click_button)
        self.image_axes.axes.get_yaxis().set_visible(False)
        self.image_axes.axes.get_xaxis().set_visible(False)
        #plt.show()
        
        plt.figure()
        plt.plot(range(len(learning_curve)), learning_curve)
        plt.plot(range(len(learning_curve)), [10*x for x in temperature_curve])
        plt.show()



