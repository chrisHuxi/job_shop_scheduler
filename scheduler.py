from typing import List, Optional, Dict
from collections import deque
from random import randint, random
from math import exp
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button,RadioButtons
import os
import pickle

import glob

import sys
import re

# =====Helper functions=============
def head(l: list):
    """
    Get first element of list. If list is empty return None
    """
    return None if len(l) == 0 else l[0]
# ==================================

class Operation:
    def __init__(self, job: int, index: int, machine: int, time: int): 
        self.job = job
        self.index = index
        self.machine = machine
        self.time = time

    def __repr__(self): #这个方法是用来display的
        return "<{};{};{}>".format(self.job, self.index, self.machine)
    
    def to_timespan(self, start: int):
        return TimeSpan(start, start + self.time, self)


class TimeSpan:
    def __init__(self, start: int, end: int, operation: Operation):
        self.start = start
        self.end = end
        self.operation = operation

    def get_machine(self) -> int:
        return self.operation.machine

    def get_job(self) -> int:
        return self.operation.job

    def __repr__(self):
        return "({}, {}, {}:{})".format(self.start, self.end, self.operation.job, self.operation.index)

class Schedule:
    def __init__(self, scheduleDict: Dict[int,List[TimeSpan]]):
        self.scheduleDict = scheduleDict

    def __repr__(self):
        return self.scheduleDict.__repr__()

    def make_span(self) -> int:
        return max(
            max(x.end for x in timespan_list)
            for machine, timespan_list in self.scheduleDict.items()
        )
            
    def log(self):
        for key, value in self.scheduleDict.items():
            print("{}: {}".format(key,value))

class TimeSpanList:
    def __init__(self,*timespans: TimeSpan):
        # deque is a python list-like data structure which is much more performant on inserting elements at the front
        # See: https://docs.python.org/3.6/library/collections.html#collections.deque
        self.deque = deque(timespans) 
    
    def append_timespan(self, ts: TimeSpan):
        self.deque.appendleft(ts)

    def get_previous_job_timespan(self, job: int) -> Optional[TimeSpan]: 
        return head([x for x in self.deque if x.get_job() == job])

    def get_previous_machine_timespan(self, machine: int) -> Optional[TimeSpan]: 
        return head([x for x in self.deque if x.get_machine() == machine])

    def get_machine_timespans(self, machine: int) -> List[TimeSpan]:
        return [x for x in self.deque if x.get_machine() == machine]

class TopologicalSort:

    # each row is job
    # each colum is (machine,time)
    @staticmethod
    def read_from_file(file_name):
        with open('./data/'+file_name, 'r') as f:
            lines = f.readlines()
            job_number = int(lines[0].strip().split(' ')[0])
            machine_number = int(lines[0].strip().split(' ')[1])
            
            operation_list = []
            for i in range(0,len(lines[1:])):
                time_list = re.split(r'[\s]+',lines[i+1].strip())
                print(time_list)
                for j in range(0,len(time_list),2):
                    operation_list.append(Operation(i, int(j/2), int(time_list[j]), int(time_list[j+1])))
        return TopologicalSort(machine_number, operation_list)


    def __init__(self, machine_number: int, opList: List[Operation]):
        self.opList = opList
        self.machine_number = machine_number

    def __repr__(self):
        return self.opList.__repr__()

    def __len__(self):
        return len(self.opList)

    def find_index_prev_job_op(self, job: int, current_index: int) -> int:
        for i,x in enumerate(self.opList):
            if x.job is job and x.index is current_index-1:
                return i
        return -1

    def find_index_next_job_op(self, job: int, current_index: int) -> int:
        for i,x in enumerate(self.opList):
            if x.job is job and x.index is current_index+1:
                return i
        return len(self.opList)+1

    def is_valid_swop(self, idx1: int, idx2: int) -> bool:
        op1 = self.opList[idx1]
        op2 = self.opList[idx2]

        prev_job_op1_idx = self.find_index_prev_job_op(op1.job, op1.index)
        next_job_op1_idx = self.find_index_next_job_op(op1.job, op1.index)
        
        prev_job_op2_idx = self.find_index_prev_job_op(op2.job, op2.index)
        next_job_op2_idx = self.find_index_next_job_op(op2.job, op2.index)

        return idx1 != idx2 and \
            idx2 > prev_job_op1_idx and idx2 < next_job_op1_idx and \
                idx1 > prev_job_op2_idx and idx1 < next_job_op2_idx

    def swop(self, idx1: int, idx2: int):
        newOpList = self.opList.copy()
        h = newOpList[idx1]
        newOpList[idx1] = newOpList[idx2]
        newOpList[idx2] = h
        return TopologicalSort(self.machine_number, newOpList)

    def neighborhood(self):
        swops = [
            (i,j)
            for i in range(len(self))
            for j in range(len(self))
            if i < j
        ]

        return [
            self.swop(i,j)
            for i,j in swops
            if self.is_valid_swop(i,j)
        ]

    def random_neighbor_really_slow(self):
        n = self.neighborhood()
        return n[randint(0,len(n)-1)]

    def random_neighbor_slow(self):
        valid_swops = [
            (i,j)
            for i in range(len(self))
            for j in range(len(self))
            if i < j
            if self.is_valid_swop(i,j)
        ]

        swop = valid_swops[randint(0,len(valid_swops)-1)]
        return self.swop(swop[0], swop[1])

    # Faster implementation to pick a random neighbor
    def random_neighbor(self):
        while True:
            i = randint(0,len(self)-1)
            j = randint(0,len(self)-1)
            if self.is_valid_swop(i,j):
                return self.swop(i, j)

    def get_schedule(self):
        #adding all new elements at start
        time_span_list = TimeSpanList()

        for current_op in self.opList:
            # Optional[TimeSpan]-type: varable can be of type TimeSpan or None
           
            # Searching for endpoints of the timeslots of previous job operation and previous machine operation
            prev_machine_timeslot = time_span_list.get_previous_machine_timespan(current_op.machine)
            prev_machine_end = prev_machine_timeslot.end if prev_machine_timeslot else 0

            prev_job_timeslot = time_span_list.get_previous_job_timespan(current_op.job)
            prev_job_end = prev_job_timeslot.end if prev_job_timeslot else 0

            # Compute according timespan to the current operation
            current_timespan = current_op.to_timespan(max(prev_job_end, prev_machine_end))
            # Add timespan to the list
            time_span_list.append_timespan(current_timespan)

        return Schedule({
            machine_idx: time_span_list.get_machine_timespans(machine_idx) for machine_idx in range(0, self.machine_number)
        })

    def make_span(self) -> int:
        return self.get_schedule().make_span()

class HillClimbingOptimizer():
    @staticmethod
    def next(ts: TopologicalSort) -> Optional[TopologicalSort]:
        n = ts.neighborhood()
        return min(
            (x for x in n),
            default=None,
            key=lambda y: y.make_span()
        )

    @staticmethod
    def optimize(ts: TopologicalSort):
        current_ts = ts
        while True:
            next_ts = HillClimbingOptimizer.next(current_ts)
            # Stop routine if there is no neighbor or if neighbor is worse then current schedule/topologicalSort
            if (next_ts == None) or next_ts.make_span() >= current_ts.make_span():
                return current_ts
            else:
                current_ts = next_ts

class SimulatedAnnealingOptimizer:
    def __init__(
        self,
        init_T: float,
        ts: TopologicalSort,
        maxSteps: int,
        shuffleing: int = 333,
        logging: str = "progress",
        colored_log = True,
        cooling_duration: float = 0.95
    ):
        self.step = 0
        self.T = init_T
        self.currentTS = ts
        self.currentMakeSpan = ts.make_span()
        self.max_steps = maxSteps
        self.shuffleing = shuffleing
        
        self.cooling_rate = init_T / (cooling_duration * maxSteps)
        self.colored_log = colored_log

        if logging == "none":
            self.logging = 0
        elif logging == "progress":
            self.logging = 1
        elif logging == "verbose":
            self.logging = 2
        else:
            raise Exception("Unknown logging flag:", logging)

        self.learning_curve: List[float] = []
        self.temperature_curve: List[float] = []


    # ==============Logging===================

    def log_colorful(self, label: str, color_code: str):
        """
        The logging will have the following formt:
        <label> <makeSpan> <temperature>
        """
        if self.logging == 2:
            if self.colored_log:
                print("\r" + color_code + label, self.currentMakeSpan, self.T, " " * 100, "\033[0m")
            else:
                print("\r" + label, self.currentMakeSpan, self.T, " " * 100)

    def log_red(self, label: str):
        self.log_colorful(label, "\033[31m")

    def log_green(self, label: str):
        self.log_colorful(label, "\033[32m")

    def log_yellow(self, label: str):
        self.log_colorful(label, "\033[33m")
    
    def log(self, label):
        self.log_colorful(label, "\033[0m")

    def print_progress_bar(self):

        if self.logging >= 1 and \
            (self.step % int(self.max_steps/100) == 0): # Only redraw progressbar if its necessary => faster!
            progress = int(100.0*self.step / self.max_steps)
            print(
                "\r[{}>{}] {}".format('=' * progress, ' ' * (100-progress), self.currentMakeSpan),
                end="              ") # end <-- padding if currentMakeSpan gets shorter

    # ========================================

    def shuffle(self, steps: int):
        """
        Creates a random topological sort by applying random swops
        """
        for i in range(0,steps):
            self.currentTS = self.currentTS.random_neighbor()
        self.currentMakeSpan = self.currentTS.make_span()
        self.log("[shuffle]")

    def next(self):
        rn = self.currentTS.random_neighbor()
        rn_makeSpan = rn.make_span()

        if rn_makeSpan <= self.currentMakeSpan:
            is_equal = self.currentMakeSpan == rn_makeSpan
            self.currentTS = rn
            self.currentMakeSpan = rn_makeSpan
            if is_equal:
                self.log("[equal]   ")
            else:
                self.log_green("[better]  ")
        elif random() < exp( float(self.currentMakeSpan - rn_makeSpan) / self.T):
            self.currentTS = rn
            self.currentMakeSpan = rn_makeSpan
            self.log_red("[worse]   ")
        else:
            self.log_yellow("[rejected]")
        
        self.learning_curve.append(self.currentMakeSpan)
        self.temperature_curve.append(self.T)
        self.T = max(self.T - self.cooling_rate, 0.00000001)
        self.step += 1

    def optimize(self):
        self.shuffle(self.shuffleing)
        while self.step <= self.max_steps:
            self.next()
            self.print_progress_bar()
        
        if self.logging >= 1: # Add linebreak after finishing
            print("")
        
        return (self.currentTS, self.learning_curve, self.temperature_curve)


    
class Visualizator():
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
        #pickle.dump(ax, open("./image/"+str(self.iteration_index) + ".pickle",'wb'))
        #plt.show()
        

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
        
            
    def display(self):
        #plt.connect('button_press_event', self.click_button)
        current_image = plt.imread(self.image_list[self.index])
        self.image_axes.imshow(current_image)
        self.button_axes = Button(ax = self.button_axes, label = "next iteration")
        self.button_axes.on_clicked(self.click_button)
        plt.show()



    
def main(argv):
    print("test file: " + argv[0])
    #ts = TopologicalSort.read_from_file('test_data1.txt')
    ts = TopologicalSort.read_from_file(argv[0])
    
    #print(ts.opList)
    #print(ts.get_schedule().scheduleDict)
    #print(ts.make_span())

    #test_v = Visualizator(ts.get_schedule().scheduleDict, ts.make_span(), 1)
    #test_v.plot()

    # print(ts.get_schedule().log())
    
    #print("Score: {}".format(ts.make_span()))
    #opt = HillClimbingOptimizer.optimize(ts)
    #print(opt)
    #print("Score: {}".format(opt.make_span()))
    
    #opt_v = Visualizator(opt.get_schedule().scheduleDict, opt.make_span(), 2)
    #opt_v.plot()

    test_v1 = Visualizator(ts.get_schedule().scheduleDict, ts.make_span(), 0)
    test_v1.plot()
    

    #print("Score: {}".format(ts.make_span()))
    opt, learning_curve, temperature_curve = SimulatedAnnealingOptimizer(65, ts, 8000, shuffleing=2500, cooling_duration=0.618).optimize()
    print("Score: {}".format(opt.make_span()))

    test_v2 = Visualizator(opt.get_schedule().scheduleDict, ts.make_span(), 1)
    test_v2.plot()
    
    bp = ButtonDisplayer("./image")
    bp.display()

    plt.figure()
    plt.plot(range(len(learning_curve)), learning_curve)
    plt.plot(range(len(learning_curve)), [10*x for x in temperature_curve])
    plt.show()

    # Visualizator(opt.get_schedule().scheduleDict, ts.make_span()).plot()
    
if __name__ == "__main__":
    main(sys.argv[1:])