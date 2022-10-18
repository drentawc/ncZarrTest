
#Tool to copy file paths and entire directories into S3 bucket.

import argparse
import glob
import os
import subprocess
import sys

#To run: /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/python /data/socd5/coastwatch/apps/tools/s3Tool.py s3://ncis-coastwatch/zarr_test/ filePath credentialsFile
# ls: /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/python /data/socd5/coastwatch/apps/tools/s3Tool.py --ls s3://riva-coastwatch/ ~/.aws/credentials
# cp: /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/python /data/socd5/coastwatch/apps/tools/s3Tool.py --cp s3://riva-coastwatch/viirs/science/L3/sector/chlora/daily/WW00/ ~/.aws/credentials /data/aftp/socd1/mecb/coastwatch/viirs/science/L3/global/chlora/daily/WW00/ --test --key 2022/

#To test: aws s3 ls s3://ncis-coastwatch/zarr_test/

def main():
    args = setupParser().parse_args()

    aws_dict = getCredentials(args.credentials, args)

    if args.ls:
        listFiles(aws_dict[0], aws_dict[1], args.bucket)
    elif args.cp:
        if os.path.isdir(args.path):
            copyFiles(aws_dict[0], aws_dict[1], args.path, args.bucket, True, args.split, args.test, args.key) 
        elif os.path.isfile(args.path):
            copyFiles(aws_dict[0], aws_dict[1], args.path, args.bucket, False, args.split, args.test, args.key) 
        else:
            sys.exit("Invalid path")
    elif args.rm:
        removeFile(aws_dict[0], aws_dict[1], args.bucket)
    


#Helper Methods

def getFileCount(directory, test):
    if test:
        print(directory)
    return subprocess.run("ls {0} | wc -l".format(directory), capture_output=True, shell=True).stdout.decode("ascii").strip()


def copyFiles(key, secret, path, bucket, directoryFlag, split, test, keyToAdd):

    if split is None:
        split = ""

    if keyToAdd is None:
        keyToAdd = ""
    
    if directoryFlag:

        print("directory")

        fileCount = getFileCount(path, test)

        #@TODO Objective is to split recursive directory calls into 4 or so subprocesses in order to speed up copying into bucket

        print(fileCount)

        #add flag to change this 
        fileList = getFileList(path, "V2022*")
        print(fileList)

        #Need to figure out exactly how to split this filelist and whether or not it is just easier to have it not split it
        #Also might just be good to keep the filelist splitter with 

        for file in fileList:

            print(file)

            if key is None:
                s3Key = file.split(bucket[-5:])[1] + "/"
            else:
                s3Key = keyToAdd + file.split(bucket[-5:])[1] + "/"

            print(s3Key)

            print(path)

            print(split)
            


            #@TODO Honestly might make this recursive, i.e. if it is directory recall, might not be worth it though 
            if os.path.isdir(file):
                print("directory")
                command = " AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1} /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/aws s3 cp --recursive {2} {3}".format(key, secret, file + "/", bucket + split + s3Key)
                print(file.split(path)[1])
            else:
                command = " AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1} /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/aws s3 cp {2} {3}".format(key, secret, file, bucket + split + keyToAdd + file.split("/")[-1])

            if test:
                print(command)

            else:

                copyCommand = subprocess.run(command, capture_output=True, shell=True)
                print(copyCommand.stdout.decode("ascii"))

                if copyCommand.returncode == 0:
                    print("Copy command was sucessful: {0}".format(copyCommand.stdout.decode("ascii")))
                else:
                    print("Copy command failed: {0}".format(copyCommand.stderr))
        # AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1}
        #command = " AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1} /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/aws s3 cp --recursive {2} {3}".format(key, secret, path, bucket + split + path.split(split)[1])

    else:
        copyCommand = subprocess.run(" AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1}".format(key, secret) + " aws s3 cp " + path + " " + bucket, capture_output=True, shell=True)

        if copyCommand.returncode == 0:
            print("Copy command was sucessful: {0}".format(copyCommand.stdout.decode("ascii")))
        else:
            print("Copy command failed: {0}".format(copyCommand.stderr))


def listFiles(key, secret, bucket):
    lsCommand = " AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1} /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/aws s3 ls {2}".format(key, secret, bucket)
    
    process = subprocess.run(lsCommand, capture_output=True, shell=True)

    print(process.stdout.decode('ascii'))


def removeFile(key, secret, bucketPath):
    rmCommand = " AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1} /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/aws s3 rm {2}".format(key, secret, bucketPath)

    process = subprocess.run(rmCommand, capture_output=True, shell=True)

    print(process.stdout.decode('ascii'))


def syncFiles():
    rmCommand = " AWS_ACCESS_KEY_ID={0} AWS_SECRET_ACCESS_KEY={1} /data/socd5/coastwatch/apps/miniconda3/envs/awscli/bin/aws s3 sync"


#Return sorted list of files
def getFileList(directory, suffix):
    return sorted(glob.glob(directory + suffix))

#Get key and secret from credentials file
def getCredentials(fileName, args):
    credentialFile = open(fileName, 'r')

    #Get specific lines from credentials file
    for index,line in enumerate(credentialFile):

        if "riva" in args.bucket:
            if index == 5:
                aws_key = line.split("= ")[1].split('\n')[0]
            elif index == 6:
                aws_secret = line.split("= ")[1].split('\n')[0]
        else: 
            if index == 1:
                aws_key = line.split("= ")[1].split('\n')[0]
            elif index == 2:
                aws_secret = line.split("= ")[1].split('\n')[0]


    return [aws_key, aws_secret]

#Setup parser 
def setupParser():
    parser = argparse.ArgumentParser(description='S3 bucket uploading tool.')

    #Build whole tool set with --ls --cp etc and each flag has a certain amount of parameters following it

    parser.add_argument('--ls', action='store_true', help='ls command.')
    parser.add_argument('--cp',  action='store_true', help='cp command.')
    parser.add_argument('--rm',  action='store_true', help='rm command.')

    parser.add_argument('bucket', help='S3 bucket to be accessed.')
    parser.add_argument('credentials', help='File path of the credentials file if needed.')
    parser.add_argument('path', nargs='?', help='Directory or file path to be upoladed to bucket.')

    parser.add_argument('--split', help='Part of directory to keep, i.e. /home/data/asd/ /asd/ --(Output goes to)--> s3_bucket:/asd/ ')

    parser.add_argument('--key', help='Additional sub key in s3, i.e. (Bucket: s3://riva-coastwatch/) --key /viirs/nrt/ --(Output goes to)--> s3://riva-coastwatch/viirs/nrt ')

    parser.add_argument('--test',  action='store_true', help='Test run.')
   
    return parser

if __name__ == '__main__':
    main()
