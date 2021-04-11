from model.population import Population as Pop
import sys
  
try:
	visual = sys.argv[1]
except IndexError:
	visual = "off"
	print("Visualisation turned off. Type 'python run.py on' to run simulation with visualisation")

pop = Pop()
pop.create()
pop.launch(dev=visual)
# pop.launch(dev='on')