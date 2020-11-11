#!/usr/bin/python3.6

import boto3
f = open('shouldtag', 'r')
mylist = f.read().splitlines()

print(len(mylist))
#print(mylist)
taglist=[]
def list_ami():
        filters = [{'Name': 'tag:ravi', 'Values': ['ami-for-deletion']}
        ]

        ec2 = boto3.client('ec2',  region_name='eu-west-1')
        image=ec2.describe_images(Filters=filters)
        for img in image['Images']:
                #print (img['ImageId'])
                taglist.append(img['ImageId'])
        return taglist



tagami=list_ami()
print(tagami)
nottag=[]
def ntt():
	for i in mylist:
		if i not in tagami:
			nottag.append(i)
	return print(nottag)

ntt()
	
	
