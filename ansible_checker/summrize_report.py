import os
import csv
import subprocess

def main():
    # List of files reports
    txt_files = [file for file in os.listdir("reports") if file.endswith(".txt")]
    # List of IP in inventory
    temp = open("iptemp.txt","r")
    iptemps = temp.split(";")
    create_sumarize_report(txt_files,iptemps)
    print("CSV file 'summarize_report.csv' has been created with the extracted data.")

def ipdiffer(files,iptemps):
    #Filter difference IP
    ipds= [x for x in iptemps if x not in files]
    
    #Write data return
    name=""
    splunk=""
    splunk_status=""
    cbr=""
    cbr_status=""
    for ipd in ipds:
        ip=ipd
        if ping(ip):
            pingstat="OK"
        else:
            pingstat="FAIL"
    
    return [name, ip, splunk, splunk_status, cbr, cbr_status, pingstat]

def ping(ipaddress):
    try:
        # Run the "ping" command with a timeout of 5 seconds
        result = subprocess.run(['ping', '-c', '1', ipaddress], capture_output=True, text=True, timeout=5)

        # Check the return code
        if result.returncode == 0:
            return True  # Ping was successful
        else:
            return False  # Ping failed
    except subprocess.TimeoutExpired:
        return False  # Ping timed out
   
# Define a function to extract information from a text file
def extract_info_from_file(file_path):
    with open("reports/"+file_path, 'r') as file:
        data = file.read()
        lines = data.split('\n')
        name = None
        ipraw = os.path.basename(file_path)
        ip = ipraw.split(".txt")[0]
        splunk = ""
        splunk_status = ""
        cbr = ""
        cbr_status = ""
        pingstat = "OK"

        for line in lines:
            if line.startswith("Static Hostname:"):
                name = line.split(":")[1].strip()
            if "Splunk Existence:" in line:
                raw = line.split(":")
                splunk=raw[1].split(" ")[2]
                splunk_status=raw[2].split(" ")[1]
            if "Carbonblack Existence:" in line:
                raw = line.split(":")
                cbr=raw[1].split(" ")[2]
                cbr_status=raw[2].split(" ")[1]

        return [name, ip, splunk, splunk_status, cbr, cbr_status, pingstat]

def create_sumarize_report(files,iptemps):
    with open('summarize_report.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Name', 'IP', 'Splunk', 'Splunk status', 'CBR', 'CBR status', 'ping status'])
        for file in files:
            data = extract_info_from_file(file)
            csv_writer.writerow(data)
        if len(iptemps)>len(files):
            datad=ipdiffer(files)
            csv_writer.writerow(datad)

if __name__ == "__main__":
    main()

