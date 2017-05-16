from __future__ import print_function

import urllib
import urllib.request
import boto3
import os
import subprocess
import shutil
import sys


def pdf2tiff(source, destination):
    try:
        idx = destination.rindex('.')
        destination = destination[:idx]
        args = [
        '-q', '-dNOPAUSE', '-dBATCH',
        '-sDEVICE=tiffg4',
        '-r600', '-sPAPERSIZE=a4',
        '-sOutputFile=' + destination + '__%03d.tiff'
        ]
        gs_cmd = 'gs ' + ' '.join(args) +' '+ source
        os.system(gs_cmd)
        args = [destination + '__*.tiff', destination + '.tiff' ]
        tiffcp_cmd = 'tiffcp  ' + ' '.join(args)
        os.system(tiffcp_cmd)
        args = [destination + '__*.tiff']
        rm_cmd = 'rm  ' + ' '.join(args)
        os.system(rm_cmd) 
    except:
        print('pdf2tiff failed')   


os.environ['PATH']

#copying tesseract to /tmp and editing permissions because lambda denies me running tesseract from /var/task
shutil.copyfile('/var/task/tesseract', '/tmp/tesseract')
os.chmod('/tmp/tesseract', 0o777)

s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Get the bucket and object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        print("Bucket: " + bucket)
        print("Key: " + key)
        filename,extension = key.split('.')

        exportfile = '/tmp/{}'.format(key.lstrip("images/").rstrip( ".pdf"))
        dlname = '/tmp/{}'.format(key.lstrip("images/"))
        print("Export: " + exportfile)
        print("download name: ", dlname)

        s3.download_file(bucket, key, dlname)


        
        print("Downloaded!")
        print("this better not fucking fail")
        tiffname = '/tmp/{}.tif'.format(key.lstrip('images/').rstrip('.pdf'))
        pdf2tiff(dlname, tiffname)
        
        print("tiffed! thank RNG!")

        # print("trying test command: ")
        # output = subprocess.check_output('/tmp/tesseract > /tmp/file.txt', stderr=subprocess.STDOUT, shell= True)
        # print(subprocess.check_output('cat /tmp/file.txt', shell = True))

        output = subprocess.check_output('export LD_LIBRARY_PATH=/var/task/lib', stderr=subprocess.STDOUT, shell=True)
        output = subprocess.check_output('export TESSDATA_PREFIX=/var/task', stderr=subprocess.STDOUT, shell=True)
        print('export paths set')

        command = 'TESSDATA_PREFIX=/var/task /tmp/tesseract {} {} > /tmp/stdout.txt'.format(
            tiffname,
            exportfile)


        try:

            ## attempt at using Popen instead of check_output
            #proc = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)
            #errors = proc.stderr.read()
            #print("ERRORS: ", errors)

            print("Trying command: ", command)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            print(subprocess.check_output('cat /tmp/stdout.txt', shell = True))
            print('command executed, attempting upload to tesseract-output')

            s3.upload_file(exportfile + '.txt', "tesseract-output", exportfile)
            print("upload complete")
        except subprocess.CalledProcessError as e: 
            print(sys.stderr)                                                                                                  
            print("Status : FAIL  ---   Return Code: " , e.returncode, "Output: ", e.output, e)
        except FileNotFoundError as e:
            print("Other Error, upload fail possibly", e, "Output: ", sys.exc_info()[0])
        else: 
            print("Status : SUCCESS")                                                                                                  
            print("Output: \n{}\n".format(output))

    except Exception as e:
        print(e)
        print('Error processing object {} from bucket {}.'.format(key, bucket))
        raise e