from typing import List, Optional, Dict
from collections import deque

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

    def __repr__(self):
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
        return (self.start, self.end).__repr__()

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
                time_list = lines[i+1].strip().split(' ')
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
            if not next_ts or next_ts.make_span() == current_ts.make_span():
                return current_ts
            else:
                current_ts = next_ts

# each row is job
# each colum is machine : time
def readData(file_name) -> List[Operation]:
    with open('./data/'+file_name, 'r') as f:
        
        lines = f.readlines()
        job_number = int(lines[0].strip().split(' ')[0])
        machine_number = int(lines[0].strip().split(' ')[1])
        
        operation_list = []
        for i in range(0,len(lines[1:])):
            time_list = lines[i+1].strip().split(' ')
            for j in range(0,len(time_list),2):
                operation_list.append(Operation(i, int(j/2), int(time_list[j]), int(time_list[j+1])))
    return operation_list
        
    
def arrange(operation_list):
    #TODO: how to generate a new operation_list? ==> simulated annealing
    
    return operation_list
    
    
def evaluate(operation_list):
    legal_flag = False
    #TODO:
    #firstly check if this list legal or not
    # but how? ==> main idea: if there is no circle: legal
    # is there a tool or algorithm to check circle?
    for i in range(len(operation_list)):
        op1 = operation_list[i]
        if i < len(operation_list) - 1:
            op2 = operation_list[i+1]
        
    
    
    
    if legal_flag == True:
        #then check the total time of this operation_list
        total_time = calculateTotalTime(operation_list)
        return total_time
    else:
        print("this arrangement is illegal!")
        return 9999

#input: {0: [op1, op3, ...]; 1: [op0, op2, ...]}
def calculateTotalTime(machine_to_op_dict):
    total_time_list = []
    for machine in machine_to_op_dict.keys():
        total_time = 0
        op_list = machine_to_op_dict[machine]
        for op in op_list:
            total_time += op.time
        total_time_list.append(total_time)
    print("max total time of this arrangement:")
    print(max(total_time_list))
    return max(total_time_list)
    
    
def main():
    # initial_operation_list = readData('test_data1.txt')
    # new_operation_list = arrange(initial_operation_list)
    # evaluate(new_operation_list)

    
    ts = TopologicalSort.read_from_file('test_data1.txt')
    print(ts)
    print("Score: {}".format(ts.make_span()))
    opt = HillClimbingOptimizer.optimize(ts)
    print(opt)
    print("Score: {}".format(opt.make_span()))
    
if __name__ == "__main__":
    main()


example_topSort = TopologicalSort(2,[
    Operation(0,0,0,80),
    Operation(0,1,1,60),
    Operation(1,0,0,50),
    Operation(1,1,1,100),
])