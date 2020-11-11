#!/usr/bin/python3.6

import pandas as pd
import re
import yaml

cols= ['Area', 'Component Name', 'Subcomponents', 'Hostname','Mgmt IP Address', 'Scope']
dfs = pd.read_excel('R4_23_3_2_PRD_PL_INFRA_LLD.xlsx', sheet_name='OBO', usecols=cols)
dfs_final = dfs.dropna()
Row_list =[] 
final_list = []
hostname_list = []
final_hostname_list= []
out_of_scope = []
for index, rows in dfs_final.iterrows():
	my_list =[rows.Area]
	Row_list.append(my_list)
	for i in Row_list:
		final_list.append(str(i)[2:-2])
itr = set(final_list)
value_list = []
for i in itr:
	if re.search("obo", i, re.IGNORECASE):
		value_list.append(i)
area_final = dfs_final[dfs_final.Area.isin(value_list)]


tenant_country_list = ['lg', 'pl', 'ie', 'nl', 'ch', 'uk', 'cl', 'at']
for index, rows in area_final.iterrows():
	host_list = [rows.Hostname]
	hostname_list.append(host_list)
	for j in hostname_list:
		final_hostname_list.append(str(j)[2:-2])
my_host_list=[]
for i in final_hostname_list:
	if 'lg' in i or 'pl' in i or 'ie' in i or 'uk' in i or 'cl' in i or 'at' in i or 'nl' in i or 'ch' in i:
		if not re.search("-odh|odh", i, re.IGNORECASE):
			my_host_list.append(i)
final_data_set = area_final[area_final.Hostname.isin(my_host_list)]

final_host_list = []
for index, rows in final_data_set.iterrows():
	out_scope = [rows.Scope]
	out_of_scope.append(out_scope)
	for k in out_of_scope:
		if not re.search("Out", str(k)[2:-2], re.IGNORECASE):
			final_host_list.append(str(k)[2:-2])
			
	
final_data_set_list = final_data_set[final_data_set.Scope.isin(final_host_list)]
export_result = final_data_set_list.to_excel('output.xlsx')

############################################

with open('prod.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)

for key, value in recursive_items(data):
    if key == "ansible_host":
      print(value)

