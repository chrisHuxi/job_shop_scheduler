# job_shop_scheduler
praktikum project for pssai 2019

## usage:
* get [data](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement): put "time" file and "machine" file into 2 files under directory "./data". example: [time.txt](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/data/test_data2_machine.txt), [machine.txt](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/data/test_data2_time.txt)
* run cmd ``` python data_comb.py time.txt machine.txt data.txt```
* run cmd ``` python scheduler.py data.txt```

## result:
after processing you will get images of scheduling before optimizing and after optimizing under directory "./images/":

![](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/image/0.png)
![](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/image/1.png)
 
## useful information:
* [task description](https://iccl.inf.tu-dresden.de/w/images/4/41/PSSAI_Practical_Assignment_2019.pdf)
* [test data](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt)
* [test result](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement)
