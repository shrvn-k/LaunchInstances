import boto3
import cfg
import json
import os
import sys


def get_name(instance):
	for tag in instance['Tags']:
			if tag['Key'] == 'Name':
				return tag['Value']


def ssh_instance(ip_addr, key_name):
	# try:
		cmd = "ssh -i "+cfg.KEY_PATH+key_name+".pem "+"ec2-user@"+ip_addr
		print cmd
		os.system(cmd)
	# except IndexError:
	# 	print "Invalid choice"


def show_menu():
	# print runningInstances
	print("Make a choice:")
	for i,instance in enumerate(runningInstances,1):
		print("{}. {} - {}".format(i, instance['instanceId'], instance['instanceName']))
	print ("\nn. Launch new instance \nc. Change region \ne. Exit")
	return raw_input("Choice:")


def check_choice(choice):
	try:
		if choice == 'n':
			launch_new()
		elif choice == 'c':
			change_region()
		elif choice == 'e':
			print("Exiting program")
			sys.exit()

		else:
			choice = int(choice)
			ip_addr = runningInstances[choice-1]['publicIp']
			print ip_addr
			key_name= runningInstances[choice-1]['keyName']
			print key_name
			ssh_instance(ip_addr, key_name)
	except (IndexError, ValueError):
		print "\nInvalid choice. Try again."


def change_region():
	desc_regions_client = boto3.client('ec2')
	desc_regions = desc_regions_client.describe_regions()
	# print desc_regions
	print "\n"
	for i,region in enumerate(desc_regions['Regions'],1):
		print("{}. {}".format(i,region['RegionName']))
	choice = int(raw_input("Select region:"))
	cfg.USER_REGION = desc_regions['Regions'][choice-1]['RegionName']
	# print cfg.USER_REGION


def get_running_instances():
	ec2 = boto3.client('ec2', region_name = cfg.USER_REGION,)
	response = ec2.describe_instances(
	    Filters=[
	        {
	            'Name': 'instance-state-name',
	            'Values': [
	                'running',
	            ]
	        }
	    ],)
	runningInstances = []
	for reservation in response['Reservations']:
		for instance in reservation['Instances']:
			tempinstance = {
			'instanceId': str(instance['InstanceId']),
			'instanceName': str(get_name(instance)),
			'publicIp': str(instance['PublicIpAddress']),
			'keyName': str(instance['KeyName'])
			}
			runningInstances.append(tempinstance.copy())
	return runningInstances

if __name__ == "__main__":
	# with open('config.json') as data:
	# 	config = json.load(data)
	while True:
		print "\n"+cfg.USER_REGION
		runningInstances = get_running_instances()
		choice = show_menu().lower()
		check_choice(choice)


