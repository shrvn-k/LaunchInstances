import boto3
import cfg
import json
import os
import sys

#Get the name of the instance from the 'Name' tag
def get_name(instance):
	if 'Tags' in instance:
		for tag in instance['Tags']:
			if tag['Key'] == 'Name':
				return tag['Value']
	return 'N/A'


#Construct and run the SSH command
def ssh_instance(ip_addr, key_name):
	cmd = "ssh -i "+cfg.KEY_PATH+key_name+".pem "+"ec2-user@"+ip_addr
	print(cmd)
	os.system(cmd)


def show_menu():
	print("Make a choice:")
	if(runningInstances == []):
		print("\n--No running instances--")
	else:
		for i,instance in enumerate(runningInstances,1):
			print("{}. {} - {}".format(i, instance['instanceId'], instance['instanceName']))
	print("\nc. Change region \nr. Refresh list \ne. Exit")
	return input("Choice:")

#Check the choice entered by the user and run the relevant command
def check_choice(choice):
	try:
		if choice == 'c':
			change_region()
		elif choice == 'e' or choice=='exit':
			print("Exiting program. \nEC2-SSHer - By Shravan Kanagokar")
			sys.exit()
		elif choice == 'r':
			return

		else:
			choice = int(choice)
			ip_addr = runningInstances[choice-1]['publicIp']
			print(ip_addr)
			key_name= runningInstances[choice-1]['keyName']
			print(key_name)
			ssh_instance(ip_addr, key_name)
	except (IndexError, ValueError):
		print("\nInvalid choice. Try again.")


def change_region():
	desc_regions_client = boto3.client('ec2')
	desc_regions = desc_regions_client.describe_regions()
	print("\n")
	for i,region in enumerate(desc_regions['Regions'],1):
		print("{}. {}".format(i,region['RegionName']))
	choice = int(input("Select region:"))
	cfg.USER_REGION = desc_regions['Regions'][choice-1]['RegionName']


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
			if 'KeyName' in instance and 'PublicIpAddress' in instance:
				tempinstance = {
				'instanceId': str(instance['InstanceId']),
				'instanceName': str(get_name(instance)),
				'publicIp': str(instance['PublicIpAddress']),
				'keyName': str(instance['KeyName'])
				}
				runningInstances.append(tempinstance.copy())
	return runningInstances

if __name__ == "__main__":
	while True:
		print("\n"+cfg.USER_REGION)
		runningInstances = get_running_instances()
		choice = show_menu().lower()
		check_choice(choice)


