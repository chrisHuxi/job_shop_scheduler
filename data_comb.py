import sys
import re

print("time file:" + sys.argv[1])
print("machine file" +sys.argv[2])

def read_from_file(time_file_name,machine_file_name,save_data_file_name):
    with open('./data/'+time_file_name, 'r') as f:
        lines = f.readlines()
        job_number = (lines[0].strip().split(' ')[0])
        machine_number = (lines[0].strip().split(' ')[1])
        time_list = []

        for i in range(0,len(lines[1:])):
            time_list.append(re.split(r'[\s]+',lines[i+1].strip()))
    
    with open('./data/'+machine_file_name, 'r') as f:
        lines = f.readlines()

        machine_list = []
        for i in range(0,len(lines)):
            tline = re.split(r'[\s]+',lines[i].strip())
            rline = []
            for s in tline:
                rline.append(str(int(s)-1))
            machine_list.append(rline)
            #machine_list.append(lines[i].strip().split(' '))
    print(time_list)
    print(machine_list)
    with open('./data/'+save_data_file_name, 'w') as f:
        write_list = [' '+job_number+' ',machine_number]
        for i in range(len(machine_list)):
            write_list.append('\n')
            for j in range(len(machine_list[i])):
                write_list.append(' '+ machine_list[i][j]+' '+time_list[i][j])
        f.writelines(write_list)
        

read_from_file(sys.argv[1],sys.argv[2],sys.argv[3])