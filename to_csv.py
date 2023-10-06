import json
import pandas as pd

with open('app_info_2.json') as json_file:
    app_info = json.load(json_file)

for i in range(len(app_info)):
    app_info[i]['Classifications'] = ', '.join(app_info[i]['Classifications'])

df = pd.DataFrame(app_info)

df.to_csv("app_info.csv", index=False)