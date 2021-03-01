# AWS Voice assitant Provisioning tool
#'''This tool is to control AWS cloud using voice assistanant'''
from voice import speak,listens,change_voice
from aws import ec2,networkAndSecurity,ebs,cloudFront,s3Buckets
# in Time module sleep is used to wait for few seconds
import time
change_voice() #Change from male to female
speak("Hey,,, Vinod, How can i help you") #intro
def speakAgain():     #Start Speaking 
    audio = listens()
    return audio

def performTask(audio): #main Tasks
    def aws(cmd):
        # 1) Create new key pair 
        if("create" in cmd or "launch" in cmd) and ("key" in cmd or "keypad" in cmd ):
            speak("Enter Key pair name")
            key = input("Key Name : ")
            networkAndSecurity.keyCreate(key)
            speak("Key pair {} Successfully created.".format(key))
        # 2) Create new Security group
        elif("create" in cmd or "launch" in cmd) and ("security" in cmd or "security-group" in cmd ):
            speak("Enter group name and description")
            grp = input("Group Name : ")
            des = input("Description : ")
            networkAndSecurity.addSecurityGroup(grp,des)
            speak("Security Group with name {} iS successfully created".format(grp))
        # 3) Create new instance
        elif("create" in cmd or "launch" in cmd) and ("instance" in cmd or "laptop" in cmd or "ins" in cmd):
            speak("Enter image ID")
            img = input("Image ID : ")
            speak("Enter instance type")
            typ = input("Instance Type:")
            speak("Enter subnet ID")
            subnet = input("Subnet ID : ")
            speak("Enter Security group ID")
            grp = input("Security group ID :")
            converter.say("Enter key name ")
            keyname = input("Key Name : ")
            ec2.cerate(img,typ,subnet,grp,keyname)
            speak("Instance successfully created.")
        # 4) Termination of instance 
        elif ("terminate" in cmd or "delete" in cmd or "destroy" in cmd) and ("instance" in cmd or "laptop" in cmd or "ins" in cmd):
            speak("Enter Instance ID")
            ids = input("Instance ID : ")
            ec2.terminate(ids) 
            print("Instance ID {} successfully Terminated.".format(ids))
            speak("Instance successfully Terminated.")
        # 5) Display list of instances
        elif ("show" in cmd or "display" in cmd or "view" in cmd or "list" in cmd) and ("instance" in cmd or "laptop" in cmd or "ins" in cmd):
            speak("Please, wait Displaying list")
            ec2.list()
            speak("The following are the instances.")
            time.sleep(4)
        # 6) Creation a volume
        elif ("create" in cmd or "launch" in cmd) and ("volume" in cmd or "EBS voluem" in cmd):
            speak("Enter Size of EBS volume")
            size = input("EBS size : ")
            ebs.volCreate(size)
            print("Volume Is created size of "+size)
            speak("Volume Is created size of {}".format(size))
        # 7) Attach Volume to a instance
        elif ("attach" in cmd or "join" in cmd) and ("volume" in cmd or "EBS voluem" in cmd or "backet" in cmd):
            speak("Enter Volum id")
            volId = input("Enter volum id : ")
            speak("Enter Instance id")
            insId = input("Enter Instance Id : ")
            ebs.volAttach(volId,insId)
            print("Volume attached to a instance. \nInstance ID "+insId+"\n Volume ID "+volId)
            speak("Volume attached to a instance.") 
        # 8) Run/start instance
        elif ("start" in cmd or "run" in cmd) and ("instance" in cmd or "laptop" in cmd or "ec2" in cmd or "ins" in cmd):
            speak("Please enter instance id. ")
            data = input("EC2 ID:")
            ec2.start(data)
            print("Instance Started.\nInstance ID : "+data)
            speak("Instance Started.")
        # 9) Stop instance
        elif ("stop" in cmd or "exit" in cmd) and ("instance" in cmd or "laptop" in cmd or "ec2" in cmd or "ins" in cmd):
            speak("Please enter instance id. ")
            data = input("EC2 ID:")
            ec2.stop(data)
            print("Intance Stopped. \nInstance ID {}".format(data))
            speak("Intance Stopped.")
        # 10) Create Cloud Front Distribution
        elif ("create" in cmd or "launch" in cmd) and ("cloud front" in cmd or "cloudfront" in cmd):
            speak("Please enter Origilnal domain name. ")
            domainName = input("Enter Domain Name : ")
            cloudFront.createCloudFront(domainName)
            print("New CloudFront distribution is created")
            speak("New CloudFront distribution is created")
        # 11) Create New S3 Buckets
        elif ("create" in cmd or "launch" in cmd) and ("S3 bucket" in cmd or "bucket" in cmd):
            prt = ""
            while(True):
                # If Error occured goes to Except part
                try:
                    BucketName = input("Enter Bucket Name : ")
                    speak("Please enter {} Bucket name. ".format(prt))
                    s3Buckets.createS3(BucketName)
                    prt = "New Bucket is created"
                    print(prt)
                    speak(prt)
                    break;
                # Display message if Exception Occured
                except Exception as e:
                    print("Oops!", e.__class__, "occurred.")
                    prt = "Oops! Name Already exists!"
                    print(prt)
                    speak(prt)
                    prt = "Unique"
        # 12) Uploading a file or folder to Bucket
        elif ("upload" in cmd or "add" in cmd) and ("file" in cmd or "folder" in cmd or "image" in cmd or "picture" in cmd or "document" in cmd) and ("bucket" in cmd or "s3 bucket" in cmd):
            prt = ""
            while(True):
                # If Error occured goes to Except part
                try:
                    print(subprocess.getoutput("DIR /W"))
                    speak("Please enter {} Location,  orelse select File or folder name, from above list. ".format(prt) )
                    fileLoc = input("Enter {} Location orelse select  File or folder name from above list : ".format(prt))
                    s3Buckets.listS3()
                    speak("Please enter {} Bucket name, from above list. ".format(prt))
                    bucketName = input("Type Bucket name from above list : ")
                    res = s3Buckets.uploadFile()
                # Display message if Exception Occured
                except Exception as e:
                    print("Oops!", e.__class__, "occurred.")
                    prt = "Oops! Something gone wrong!"
                    print(prt)
                    speak(prt)
                    prt = "Valid"
        # 13) Delete/Remove Cloud front Distribution
        elif ("delete" in cmd or "remove" in cmd) and ("cloud front" in cmd or "cloudfront" in cmd):
            prt = ""
            while(True):
                # If Error occured goes to Except part
                speak("Please enter {} Cloudfront distribution id. ".format(prt))
                cloudFrontID = input("Enter {} Cloudfront distribution id : ".format(prt))
                # Taking complete JSON to find if-match ID
                try:
                    delRes = cloudFront.deleteCloudFront(cloudFrontID)
                    print(delRes)
                # Display message if Exception Occured
                except Exception as e:
                    print("Oops! ",e," occurred.")
        # 14) Show a list of CloudFront Distribution
        elif ("show" in cmd or "display" in cmd or "view" in cmd or "list" in cmd) and ("cloud front" in cmd or "cloudfront" in cmd):
            ptr = "The following are list of CloudFront"
            speak("Please, wait Displaying list")
            print(ptr)
            speak(ptr)
            cloudFront.listCloudFront()
            time.sleep(3)
        # 15) Show list of Files/folder in a backet
        elif ("show" in cmd or "display" in cmd or "view" in cmd or "list" in cmd) and ("file" in cmd or "folder" in cmd or "image" in cmd or "picture" in cmd or "document" in cmd) and ("bucket" in cmd or "s3 bucket" in cmd):
            speak("Please, wait Displaying list")
            print("\n\t\t\t--- Buckets ---\n")
            s3Buckets.listS3()
            ptr = "Enter the Bucket Name from above list "
            speak(ptr)
            bucketName = input("\n\t\t{} : ".format(ptr))
            ptr = "The following are list of files or folders available in "+bucketName+" bucket."
            print("\n\t",ptr,"\n")
            speak(ptr)
            print("\t\t\t--- ",bucketName," ---\n")
            s3Buckets.listS3files(bucketName)
        # 16) Show a list of S3 buckets
        elif ("file" not in cmd or "folder" not in cmd or "image" not in cmd or "picture" not in cmd or "document" not in cmd) and("show" in cmd or "display" in cmd or "view" in cmd or "list" in cmd) and ("S3 bucket" in cmd or "bucket" in cmd):
            ptr = "The following are list of Buckets available."
            speaka("Please, wait Displaying list")
            print("\n\t",ptr,"\n")
            speak(ptr)
            print("\t\t\t--- Buckets ---\n")
            s3Buckets.listS3()
        # 17) Remove files/folders from Buckets 
        elif ("delete" in cmd or "remove" in cmd) and ("file" in cmd or "folder" in cmd or "image" in cmd or "picture" in cmd or "document" in cmd) and ("bucket" in cmd or "s3 bucket" in cmd):
            while True:
                try:
                    ptr = "The following are list of Buckets available."
                    speak(", Displaying a list.")
                    print("\n\t\t\t--- Buckets ---\n")
                    s3Buckets.listS3()
                    ptr = "Please enter bucket name from above list"
                    speak(ptr)
                    bucketName = input("\n{} : ".format(ptr))
                    check = s3Buckets.listS3files(bucketName)
                    if "error" in check:
                        print(check)
                        speak("Sorry Dear, Bucket Name is not exists.")
                        speak("Please Enter Valid")
                        continue
                    print(check)
                    print("\t\t\t--- ",bucketName," ---")
                    ptr = "Type File Name to remove"
                    speak(ptr)
                    fileName = input("\n{} : ".format(ptr))
                    delFile = s3Buckets.deleteS3files(bucketName,fileName)
                except Exception as e:
                    print("Oops! ",e," occurred.")
                    prt = "Oops! Something gone wrong!"
                    print(prt)
                    speak(prt,". Check Bucket or file name.")
        # 18) Delete or Remove Buckets
        if ("delete" in cmd or "remove" in cmd) and ("bucket" in cmd or "s3 bucket" in cmd):
            while True:
                try:
                    ptr = "The following are list of Buckets available."
                    speak(", Displaying a list.")
                    print("\n\t\t\t--- Buckets ---\n")
                    s3Buckets.listS3()
                    ptr = "Please enter bucket name from above list, to remove a bucket"
                    speak(ptr)
                    bucketName = input("\n{} : ".format(ptr)) or "."
                    check = deleteS3Bucket(bucketName)
                    if "BucketNotEmpty" in check:
                        speak("Sorry Dear, Bucket is not empty first empty Files.")
                        continue
                    elif "Error" in check or "error" in check:
                        print("Please enter Valid.")
                        speak("Sorry Dear, Bucket Name is not exists.")
                        speak("Please enter Valid.")
                        continue
                    if "del" in check or "Del" in check:
                        prt = "Success!!, Bucket is removed."
                        speak(prt)
                    break
                except Exception as e:
                    prt = "Oops! Something gone wrong!"
                    speak(prt)
            # Task is not available
            else:
                print("sorry, There is no such task..")
                speak("sorry, There is no such task..")
    if "how are you" in audio:
        speak("I am doing great....")
    elif "tell me about" in audio:
        speak("I am Your voice assistant, very intelligent. I can control AWS public cloud for you.")
    elif "help" in audio:
        speak("I can help you from the following list.")
        print("I can help you from Provisioning from the following list.")
        print("1. EC2 instance")
        print("2. Managing Instances")
        print("3. Key pairs,Security groups")        
        print("4. CloudFront")
        print("5. EBS,S3")
        print("6. ")
        print("7. ")
        speak("Launchs a instance")
        speak("Provisioning key pair and Security group, Provisioning EBS,S3.Cloudfront, Provisioning ec2 instances.")
    elif "hello" in audio or "hey" in audio or "hi" in audio:
        speak("Hi dear, How are you..")
    else:
        aws(audio)
while 1: #Run Loop untill we logout
    aud = speakAgain()
    if "exit" in aud: #exit
        speak("AWS Account Logging out.")
        print("AWS account is logged out.")
        exit()
    else: #entire to tasks to perform
        print(aud)
        performTask(aud)