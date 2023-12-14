import json
import ndjson
import os
import csv
import pysftp

#Create folder to savr summarize report
def check_output_folder(output_folder):
    try:
        os.mkdir(output_folder)
        return output_folder
    except FileExistsError:
        return output_folder
    except Exception as e:
        print(f"An error occurred: {e}")

#Find Hostname and OS        
def find_nameos_ip(ip):
    file_path= "./vm_info.csv"
    with open(file_path,  newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            if row['IP Address'] == ip:
                return row['Name'], row['Guest OS']
        return None, None

#Add cis level in Window
def check_key(data):
    global os_type
    if data is None or data['meta'] is None:
        return 0
    if "meta" in data and "workstation" in data["meta"]:
        os_type=1
    elif "meta" in data and "Domain_Controller" in data["meta"]:
        os_type=2
    elif "meta" in data and "domain_controller" in data["meta"]:
        os_type=3
    elif "meta" in data and "benchmark_os" in data["meta"]:
        os_type=4
    else:
        os_type=5
    return os_type

#Read json report and add fields
def read_json_file(file_path,file_name):
    hostname, os = find_nameos_ip(file_name)
    with open(file_path, 'rb') as json_file:
        data = json.load(json_file)
    for result in data["results"]:
        result["level"] = result.pop("human")
        # print(check_key(result))
        if check_key(result)==1:
            if result["meta"]["server"] == 2 or result["meta"]["workstation"] == 2 :
                result["level"]= 2
            else:
                result["level"]= 1
        elif check_key(result)==2:
            if result["meta"]["Domain_Controller"] == 2 or result["meta"]["Member_Server"] == 2:
                result["level"]= 2
            else:
                result["level"]= 1
        elif check_key(result)==3:
            if result["meta"]["Member_Server"] == 2 or result["meta"]["domain_controller"] == 2:
                result["level"]= 2
            else:
                result["level"]= 1
        elif check_key(result)==5:
            if result["meta"]["Member_Server"] == 2:
                result["level"]= 2
            else:
                result["level"]= 1
        rtitle= result["title"].split("|")
        cis_id=rtitle[0]
        if len(rtitle)>2:
            title=rtitle[1]+rtitle[int(len(rtitle)-1)]
        elif len(rtitle)==2:
            title=rtitle[1]
        else:
            title=''
        result["os"] = result.pop("err")
        result["meta"]={"ip": file_name}
        result["os"]= os
        result["meta"]["hostname"] = hostname
        result["meta"]["cisid"] = cis_id
        result["title"]= title
    return data

#Change type of report form json to ndjson
def cover(json_files,folder_path):
    for json_file in json_files:
        finame=json_file[:len(json_file)-5]
        json_file_path = os.path.join(folder_path, json_file)
        data = read_json_file(json_file_path,finame)
        with open(json_file_path, 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for result in data['results']:
                writer.writerow(result)

def main():
    folders_path = "./CIS_report_raw/"
    files = os.listdir(folders_path)
    #Change type of report for Splunk can read
    cover(files,folders_path)
    print(f'Cover Completed')
    
    #Send report to splunk
    usr = input("Please input username:")
    pwd = input("Please input password:")
    folder= input("Please input folder report in Splunk:")
    with pysftp.Connection('10.96.102.112', username=usr, password=pwd) as sftp:
        with sftp.cd(folder):
            sftp.put(files) 

if __name__ == "__main__":
    main()