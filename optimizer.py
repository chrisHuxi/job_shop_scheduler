from  topological_sort import TopologicalSort
from random import randint, random
from math import exp
from typing import List, Optional, Dict

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
        logging: str = "progress",
        colored_log = True,
        cooling_duration: float = 0.95
    ):
        self.step = 0
        self.T = init_T
        self.currentTS = ts
        self.currentMakeSpan = ts.make_span()
        self.max_steps = maxSteps
        
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

    def shuffle(self, steps: int = 1500):
        """
        Creates a random topological sort by applying random swops
        """
        for i in range(0,steps):
            self.currentTS = self.currentTS.random_neighbor()
        self.currentMakeSpan = self.currentTS.make_span()
        self.log("[shuffle]")
        return self.currentTS

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
        while self.step <= self.max_steps:
            self.next()
            self.print_progress_bar()
        
        if self.logging >= 1: # Add linebreak after finishing
            print("")
        
        return (self.currentTS, self.learning_curve, self.temperature_curve)
