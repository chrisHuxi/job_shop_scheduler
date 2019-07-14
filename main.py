#! python3

from vistalizator import Visualizator, ButtonDisplayer
from topological_sort import TopologicalSort
from optimizer import SimulatedAnnealingOptimizer
from sys import argv

def main():

  # Load Settings
  settings = {
    "setup": argv[1],
    "iteration_number": int(argv[2])
  }
  print("Schedule Setup Code: {}".format(settings["setup"]))
  print("Number of Iterartion: {}".format(settings["iteration_number"]))
  print("~" * 128)


  # Read data
  init_ts = TopologicalSort.read_from_file(settings["setup"])
  
  # Optimize Schedule
  optimizer = SimulatedAnnealingOptimizer(65, init_ts, settings["iteration_number"], cooling_duration=0.5)
  ts_after_shuffeling = optimizer.shuffle(250)
  optimized_ts, learning_curve, temperature_curve = optimizer.optimize()

  # Render plots of computed schedules
  v_initial = Visualizator(init_ts.get_schedule().scheduleDict, init_ts.make_span(), 0)
  v_initial.plot()  
  v_after_shuffeling = Visualizator(ts_after_shuffeling.get_schedule().scheduleDict, init_ts.make_span(), 1)
  v_after_shuffeling.plot()
  v_opt = Visualizator(optimized_ts.get_schedule().scheduleDict, init_ts.make_span(), 2)
  v_opt.plot()
  
  # Display 
  bp = ButtonDisplayer("./image")
  bp.display(learning_curve,temperature_curve) #not elegant, but works :(

    
if __name__ == "__main__":
  main()