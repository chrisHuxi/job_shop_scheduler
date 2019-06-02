from typing import List, Optional, Dict

# =====Helper functions=============
def head(list: list):
    """
    Get first element of list. If list is empty return None
    """
    return next(iter(list), None)
# ==================================

class Operation:
    def __init__(self, job: int, index: int, machine: int, time: int): 
        self.job = job
        self.index = index
        self.machine = machine
        self.time = time
    
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



class TopologicalSort:
    def __init__(self, machine_number: int, opList: List[Operation]):
        self.opList = opList
        self.machine_number = machine_number

    def get_schedule(self):
        #adding all new elements at start
        time_span_list: List[TimeSpan] = []

        for curr_op in self.opList:

            # Optional[TimeSpan]-type: varable can be of type TimeSpan or None
           
            # Searching for endpoints of the timeslots of previous job operation and previous machine operation
            prev_machine_timeslot: Optional[TimeSpan] = head([x for x in time_span_list if x.get_machine() == curr_op.machine])
            prev_machine_end = prev_machine_timeslot.end if prev_machine_timeslot else 0

            prev_job_timeslot: Optional[TimeSpan] = head([x for x in time_span_list if x.get_job() == curr_op.job])
            prev_job_end = prev_job_timeslot.end if prev_job_timeslot else 0

            # Compute according timespan to the current operation
            curr_timespan = curr_op.to_timespan(max(prev_job_end, prev_machine_end))
            # Add timespan to the left side of the list
            time_span_list.insert(0, curr_timespan)

        time_span_list.reverse()
        return Schedule({
            machine_idx: [x for x in time_span_list if x.get_machine() == machine_idx] for machine_idx in range(0, self.machine_number)
        })


    #variable:
    #job
    #index
    #machine
    #time
    
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
    initial_operation_list = readData('test_data1.txt')
    new_operation_list = arrange(initial_operation_list)
    evaluate(new_operation_list)
    
if __name__ == "__main__":
    main()


example_topSort = TopologicalSort(2,[
    Operation(0,0,0,80),
    Operation(0,1,1,60),
    Operation(1,0,0,50),
    Operation(1,1,1,100),
])