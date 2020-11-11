#!/usr/bin/python3.6

import pandas as pd
import re
import yaml
import glob

cols= ['Area', 'Component Name', 'Subcomponents', 'Hostname','Mgmt IP Address', 'Scope']

datapath = "./"
allfiles = glob.glob(datapath  + "*.xlsx")

print(allfiles)
dfs = pd.DataFrame()

for excelfiles in allfiles:
 df = pd.read_excel(excelfiles, sheet_name='OBO', usecols=cols)
 dfs = dfs.append(df,ignore_index=True)



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

final_lld_host_list = []
for index, rows in final_data_set_list.iterrows():
    lld_host_list = [rows.Hostname]
    final_lld_host_list.append(str(lld_host_list)[2:-2])

############################################

with open('prod.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)

icinga_iplist = []
icinga_hostname = []
for key, value in recursive_items(data):
    if key == "ansible_host":
      if re.search('^[a-zA-Z]',value):
       icinga_hostname.append(value)
      if  re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", value):
       icinga_iplist.append(value)

icinga_hostname

icinga_inventory_no_host = []
for i in final_lld_host_list:
    if i not  in icinga_hostname:
       icinga_inventory_no_host.append(i)
       f = open("host_not_in_icinga_host_list", "a")
       f.write(i+'\n')
       f.close()

print('Not in icinga_hostname list {}'.format(len(icinga_inventory_no_host)))


lld_iplist = []
for index, rows in final_data_set_list.iterrows():
        ip_list = rows['Mgmt IP Address']
        lld_iplist.append(ip_list)

ipaddr_with_no_hostname_in_icinga = final_data_set_list[final_data_set_list['Mgmt IP Address'].isin(icinga_iplist)]
export_result = ipaddr_with_no_hostname_in_icinga.to_excel('./ipaddr_with_no_hostname_in_icinga.xlsx')
