# job_shop_scheduler
practical work for pssai 2019

By __Edgar Dorausch__ and __Xi Hu__

## description
This project uses the simulated annealing heuristic to compute optimized solution for the job shop problem. The number of iterations can be statically set when starting the script.

## usage:
(You need to install numpy and matplotlib to use the script.)
Run the main script: `python ./main <setup_code> <iteration_number>`
e.g. `python ./main ta01 3000`

(the project is tested on python 3.6 - there may occur errors if the script is executed by a python interpreter with an other version)

## result:
after processing you will get images of scheduling before optimizing, after applying a certain amount of random swops and after optimizing under directory "./images/" (e.g.):

![](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/image/0.png)
![](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/image/1.png)
![](https://github.com/chrisHuxi/job_shop_scheduler/blob/master/image/2.png)

Those computed images are also shown together with a plot of the learning curve and the temperature curve immediate after the optimization has finished.
 
## useful information:
* [task description](https://iccl.inf.tu-dresden.de/w/images/4/41/PSSAI_Practical_Assignment_2019.pdf)
* [test data](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt)
* [test result](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement)
