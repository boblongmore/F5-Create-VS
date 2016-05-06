#!/usr/bin/env python

from f5.bigip import BigIP
import csv
bigip = BigIP("172.30.4.16", "admin", "password")

#open nodes.txt document and turn into an array
def open_csv():
	with open('vs-input.csv', 'rb') as csvfile:
		vs_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in vs_reader:
			sendrow = ','.join(row)
			vs_list = sendrow.split(',')
			get_val(vs_list)

def get_val(Node_Val):
#	Node_Val = x.split()
	vs_name = Node_Val[0]
	vs_dest = Node_Val[1]
	vs_port = Node_Val[3]
	vs_pool = Node_Val[5]
	#vs_profile = Node_Val[4]

	if vs_port == '80':
		vs_create_http(vs_name, vs_dest, vs_port, vs_pool)
	elif vs_port == '443':
		vs_create_https(vs_name, vs_dest, vs_port, vs_pool)
	
#Create pools
def vs_create_http (vs_name, vs_dest, vs_port, vs_pool):
    vs1 = bigip.ltm.virtuals.virtual.create(name=vs_name, partition='Common', destination=vs_dest+':'+vs_port, pool=vs_pool, rules='http_to_https', sourceAddressTranslation={'type':'automap'})
def vs_create_https (vs_name, vs_dest, vs_port, vs_pool):
    vs1 = bigip.ltm.virtuals.virtual.create(name=vs_name, partition='Common', destination=vs_dest+':'+vs_port, pool=vs_pool, profiles=vs_name+'-ssl-2048', sourceAddressTranslation={'type':'automap'})

#call on function to parse CSV
def create_vs():
	open_csv()

#kick it off
create_vs()