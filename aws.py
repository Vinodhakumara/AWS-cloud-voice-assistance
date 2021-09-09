#  Modules
from os import system
from subprocess import getoutput
import json
# Variables
inst_list = dict()
vol_list = dict()

# EC2
class ec2:
    
    def create(imageId,type,keypair,subnet="ap-south-1",SecurityGroup="sg-68248b0f",numberOfInst=1):
        system("aws ec2 run-instances --image-id {} --instance-type {} --subnet-id {} --count {} --security-group-ids {} --key-name {}".format(imageId,type,subnet,numberOfInst,SecurityGroup,keypair))
        ec2.status(instanceID)
        
    def status(instanceID):
        if_match = json.loads(getoutput("aws ec2 describe-instances --instance-ids ".format(instanceID)))
        inst_list["instanceId"],inst_list["status"] = if_match["Reservations"][0]["Instances"][0]["InstanceId"],if_match["Reservations"][0]["Instances"][0]["State"]["Name"]
        print("InstanceID: {} \t\t Status: {}".format(inst_list["instanceId"],inst_list["status"]))
        return inst_list
    
    def stop(instanceID):
        getoutput("aws ec2 stop-instances --instance-ids {}".format(instanceID))
        check = ec2.status(instanceID)
        if check["status"] == "stopped":
            print("Instance not running....")
    
    def start(instanceID):
        getoutput("aws ec2 start-instances --instance-ids {}".format(instanceID))
        check = ec2.status(instanceID)
        if check["status"] == "started":
            print("Instance already satarted....")
        
    def reboot(instanceID):
        getoutput("aws ec2 reboot-instances --instance-ids {}".format(instanceID))
        check = ec2.status(instanceID)
        if check["status"] == "stopped":
            print("Instance not running....")
        
    def terminate(instanceID):
        getoutput("aws ec2 terminate-instances --instance-ids {}".format(instanceID))
        ec2.status(instanceID)
        
    def list():
        if_match = json.loads(getoutput("aws ec2 describe-instances"))
        for i in range(len(if_match["Reservations"])):
            ec2.status(i)
            
# Elastic Block Storage(EBS)
class ebs:
    #EBS Volumes
    def assignValue(volID):  #Assign a volume 
        try:
            vol_list['volList'] = json.loads(getoutput("aws ec2 describe-volumes")) 
            vol = json.loads(getoutput("aws ec2 describe-volumes --volume-ids {}".format(volID)))
            vol_list["Attachments"] = vol["Volumes"][0]["Attachments"]
            vol_list['AvailabilityZone'] = vol["Volumes"][0]['AvailabilityZone']
            vol_list['Size']= vol["Volumes"][0]['Size']
            vol_list['State'] = vol["Volumes"][0]['State']
            vol_list['VolumeId'] = vol["Volumes"][0]['VolumeId']
            for i in range(len(vol_list["Attachments"])):
                vol_list['InstanceId'] = vol_list["Attachments"][i]['InstanceId']
                vol_list['Device Name'] = vol_list["Attachments"][i]['Device']
                vol_list['AttachStatus'] = vol_list["Attachments"][i]['State']
            return vol_list
        except:
            print("Something Went wrong")
    
    def volCreate(volType="gp2",size="1",AZ="ap-south-1a"): #Create A volume
        try:
            system("aws ec2 create-volume --volume-type {} --size  {} --availability-zone {}".format(volType,size,AZ)) 
            ebs.volCreate()
        except:
            print("Something Went wrong")
    
    def volDetails(volID):  #show volume details
        try:
            vol_list = ebs.assignValue(volID)
            print("\nVolumeId: {}\t".format(vol_list['VolumeId']))
            for i in range(len(vol_list["Attachments"])):
                print("Attachments:\n\tInstanceId: {}\n\tDevice Name: {} \n\tState: {}".format(vol_list['InstanceId'] ,vol_list['Device Name'],vol_list['AttachStatus']))
            print("AvailabilityZone: {}\t Size: {}\tState:{}\t\n".format(vol_list['AvailabilityZone'],vol_list['Size'],vol_list['State'],vol_list['VolumeId'])) 
        except:
            print("Something Went wrong")
    
    def volList():  #list a VOlumes
        vol = json.loads(getoutput("aws ec2 describe-volumes"))
        for i in range(len(vol["Volumes"])):
            ebs.volDetails(vol["Volumes"][i]['VolumeId'])

    def volAttach(volID,instanceID):    # Attach Volume to Instance
        vol_list = ebs.assignValue(volID)
        print(vol_list["VolumeId"])
        try:
            if "attach" in vol_list["AttachStatus"]:
                print("Device Already attached.")
        except:
            try:
                getoutput("aws ec2 attach-volume --volume-id {} --instance-id {} --device /dev/sdf".format(volID,instanceID))
                vol_list = ebs.assignValue(volID)
                print("VolumeID: {}\t\tInstanceID: {}\t\tDeviceName: {}\t\tStatus: {}\n".format(vol_list["VolumeId"],vol_list["InstanceId"],vol_list["Device Name"],vol_list["AttachStatus"]))
                print("Successfully attached Device from instance ID: {}".format(instanceID))
            except:
                print("Something Went wrong")
            
        
    def volDetach(volID,instanceID):   #Detach Volume from Instances
        vol_list = ebs.assignValue(volID)
        try:
            if "attach" in vol_list["AttachStatus"]:
                try:
                    getoutput("aws ec2 detach-volume --volume-id {} --instance-id {}".format(volID,instanceID))
                    print("Successfully Detached Device from instance ID: {}".format(instanceID))
                except:
                    print("Something Went wrong")
        except:
            print("Device not attached to this {} incetance.".format(instanceID))
            
    def volDelete(volID):   #Delete volume
        vol_list = ebs.assignValue(volID)
        try:
            if "attach" in vol_list["AttachStatus"]:
                print("Device attached please detach a device and try again.")
        except:
            try:
                getoutput("aws ec2 delete-volume --volume-id {}".format(volID))
                print("Successfully removed Volume".format(volID))
            except:
                print("Something Went wrong")
                
    # EBS SnapeShots
    #def snapCreat():
    #def snapDelate():
    #def snapList():

# Networking and Security
class networkAndSecurity:
    def keyCreate(keyname):  #Create Keypair
        result = getoutput("aws ec2 create-key-pair --key-name {}".format(keyname))
        return result
    
    def keyRemove(keyname):  #Remove Key pairs
        result = getoutput("aws ec2 delete-key-pair --key-name {}".format(keyname))
        return result
    
    def addSecurityGroup(groupname,desc):  # Add Security Group
        result = getoutput("aws ec2 create-security-group --group-name {} --description {}".format(groupname,desc))
        return result
    
    def deleteSecurityGroup(groupname,desc):   # Delete Security group
        result = getoutput("aws ec2 delete-security-group --group-name {} --description {}".format(groupname,desc))
        return result

# CloudFront
class cloudFront:
    def createCloudFront(domainName): # Create Cloud Front
        result = getoutput("aws cloudfront create-distribution --origin-domain-name {}".format(domainName))
        return result
    
    def deleteCloudFront(cloudFrontID):     # Delete/Remove Cloud front Distribution
        try:         # Taking complete JSON to find if-match ID
            if_match_ID = json.loads(getoutput("aws cloudfront get-distribution --id {}".format(cloudFrontID)))
            result = getoutput("aws cloudfront delete-distribution --id {} --if-match {}".format(cloudFrontID,if_match_ID["ETag"]))
            if "DistributionNotDisabled" in delRes:
                prt = ("Your Coudfront id {} is not disabled,  Please go to AWS account and Disable Your Cloud front Distribution.\n".format(cloudFrontID))
                return prt
            else:
                prt = "Success!!, Cloud Front ID {} is deleted".format(cloudFrontID)
                return prt
        except Exception as e:         # Display message if Exception Occured
            prt = "Oops! Something gone wrong!"
            return prt
        
    def listCloudFront():  # List CloudFront 
        if_match = json.loads(getoutput("aws cloudfront list-distributions"))
        for i in range(len(if_match["DistributionList"]["Items"])):
            print(str(i+1)+") Cloudfront Distribution ID : ",if_match["DistributionList"]["Items"][i]["Id"],"\n") 
            print("  => Status : ",if_match["DistributionList"]["Items"][i]["Status"])
            print("  => CloudFront Domain Name : ",if_match["DistributionList"]["Items"][i]["DomainName"])
            print("  => CloudFront Origin Domain Name : ",if_match["DistributionList"]["Items"][i]["Origins"]["Items"][0]["DomainName"])
            print("  => CloudFront is Enable : ",if_match["DistributionList"]["Items"][i]["Enabled"],"\n")      
            # a = [if_match_ID["DistributionList"]["Items"][i]["Id"] for i in range(len(if_match_ID["DistributionList"]["Items"]))] #Single line For loop
            # print("\n".join(str(a).strip("[]").split(",")).replace("\'","").replace(" ",""))  # helps to remove all extras    
    
# S3 Buckets
class s3Buckets:
    def createS3(bucketName):    # Create New S3 Buckets
        try:
            result = getoutput("AWS s3api create-bucket --bucket {} --regoin ap-south-1".format(bucketName))
            return result
        except:
            return "Oops! "+ e.__class__+" occurred."
        
    def uploadFile(fileLoc,bucketName):    # Uploading a file or folder to Bucket
        try:
            publicAcess = input("Do you want to allow public acess (y,n) : ")
            desicion = "--acl public-read-write" if "y" in publicAcess else ""
            res = getoutput("AWS s3 cp {} s3://{} {}".format(fileLoc,bucketName,desicion))
            if "Completed" in res or "complete" in res or "completed" in res or "Complete" in res: 
                result = "Success!!, File, or folder uploaded to a bucket name {}".format(bucketName)
                return result
            else:
                return "Oops!, Something gone wrong!"
        except Exception as e:
            return "Oops! "+e.__class__+" occurred."
        
    def deleteS3Bucket(bucketName):    # Delete or Remove Buckets
        try:
            result = getoutput("aws s3api delete-bucket --bucket {}".format(bucketName))
            if "BucketNotEmpty" in result:
                print("Sorry, Bucket is not empty first empty Files.")
            elif "Error" in check or "error" in result:
                print("Please enter Valid.")
            if "del" in result or "Del" in result:
                prt = "Success!!, Bucket is removed."
                print(prt)
        except Exception as e:
            print("Oops! ",e," occurred.")
       
    def deleteS3files(bucketName,fileName):    # Remove files/folders from Buckets 
        getoutput("aws s3 rm s3://{}/{}".format(bucketName,fileName))
        try:
            if "del" in delFile:
                return "Success!!, File is removed."
            else:
                return ("Oops! ",e," occurred.")
        except Exception as e:
            return ("Oops! ",e," occurred.")
        
    def listS3():    # Show a list of S3 buckets
        print("\t\t\t--- Buckets ---\n")
        if_match = json.loads(getoutput("aws s3api list-buckets"))
        for i in range(len(if_match["Buckets"])):
            print("\t\t",i+1,") ",if_match["Buckets"][i]["Name"])
                
    def listS3files(bucketName):    # Show list of Files/folder in a backet
        print(getoutput("aws s3 ls {}".format(bucketName)),"\n")
