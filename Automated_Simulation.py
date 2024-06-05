import os
import Scenario1DCA
import Scenario2
import Scenario3
import importlib

# fills file_names list with the names of the files in Price_History folder
directory_path = 'Price_History'
file_names = []
for each in os.listdir(directory_path):
    file_names.append("Price_History/" + each)

# iterates through file_names list and runs simulation for each scenario with each data set in the folder
for each in file_names:
    importlib.reload(Scenario1DCA)
    importlib.reload(Scenario2)
    importlib.reload(Scenario3)
    Scenario1DCA.scenario1dca(each)
    Scenario2.scenario2(each)
    Scenario3.scenario3(each)

print("Simulation complete.")
