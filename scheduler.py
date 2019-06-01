#example:
# M1[ O11, O22 ]
# M2[ O21, O12 ]


class Operation:
    def __init__(self, job, index, machine, time): #index and machine seems to be the same
        self.job = job
        self.index = index
        self.machine = machine
        self.time = time
    #variable:
    #job
    #index
    #machine
    
# each row is job
# each colum is machine : time
def readData(file_name):
    with open('.\\data\\'+file_name, 'r') as f:
        
        lines = f.readlines()
        print(lines[0].strip().split(' '))
        job_number = int(lines[0].strip().split(' ')[0])
        machine_number = int(lines[0].strip().split(' ')[1])
        
        operation_list = []
        for i in range(0,len(lines[1:])):
            time_list = lines[i+1].strip().split(' ')
            for j in range(0,len(time_list),2):
                operation_list.append(Operation(i, int(j/2), int(time_list[j]), int(time_list[j+1])))
        #for o in operation_list:
        #    print(o.time)
        #    pass
        #print(len(operation_list))
    return operation_list
        
    
def arrange(operation_list):
    #TODO: how to generate a new operation_list? ==> simulated annealing
    
    return operation_list
    
def evaluate(operation_list):
    legal_flag = false
    #TODO:
    #firstly check if this list legal or not
    # but how?
    
    if legal_flag == true:
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
    
    
main()