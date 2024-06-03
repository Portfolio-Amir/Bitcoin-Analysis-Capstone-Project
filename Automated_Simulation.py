import os
import Scenario1DCA
import Scenario2
import Scenario3
import importlib

directory_path = 'Price_History'
file_names = []
for each in os.listdir(directory_path):
        file_names.append("Price_History/" + each)


for each in file_names:
    importlib.reload(Scenario1DCA)
    importlib.reload(Scenario2)
    importlib.reload(Scenario3)
    Scenario1DCA.scenario1DCA(each)
    Scenario2.scenario2(each)
    Scenario3.scenario3(each)

print("Simulation complete.")

