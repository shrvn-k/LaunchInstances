import boto3
import json

ec2 = boto3.client('ec2')

with open('config.json') as data:
	config = json.load(data)

print("Enter region(Default:%s):" %(config["Default"]["Region"]))
x = raw_input()
if x is "":
	user_region = config["Default"]["Region"]
else:
	user_region = x

print("Enter AMI id(Default:%s):" %(config["EC2"]["Regions"][user_region]["ImageId"]))
x = raw_input()
if x is "":
	user_ami = config["EC2"]["Regions"][user_region]["ImageId"]
else:
	user_ami = x


print("Enter Instance name(Default:%s):" %(config["EC2"]["Regions"][user_region]["InstanceName"]))
x = raw_input()
if x is "":
	user_instance_name = config["EC2"]["Regions"][user_region]["InstanceName"]
else:
	user_instance_name = x


print("Enter Key name(Default:%s):" %(config["EC2"]["Regions"][user_region]["KeyName"]))
x = raw_input()
if x is "":
	user_key = config["EC2"]["Regions"][user_region]["KeyName"]
else:
	user_key = x

print("Enter InstanceType(Default:%s):" %(config["Default"]["InstanceType"]))
x = raw_input() 
if x is "":
	user_itype = config["Default"]["InstanceType"] 
else:
	user_itype = x

print("Enter MinCount(Default:%s):" %(config["Default"]["MinCount"]))
x = raw_input() 
if x is "":
	user_min = config["Default"]["MinCount"] 
else:
	user_min = int(x)

print("Enter MaxCount(Default:%s):" %(config["Default"]["MaxCount"]))
x = raw_input() 
if x is "":
	user_max = config["Default"]["MaxCount"] 
else:
	user_max = int(x)

print("Creating your instances")

response = ec2.run_instances(ImageId = user_ami, 
	InstanceType = user_itype, 
	MaxCount = user_max, 
	MinCount = user_min, 
	KeyName = user_key,
	TagSpecifications = [
		{
			'ResourceType' : 'instance',
			'Tags' : [
				{
					'Key' : 'Name',
					'Value' : user_instance_name
				},
			]
		},
	]
)


if response:
	print("Instances Created Successfully")
	
else:
	print("Error in creating instances")



