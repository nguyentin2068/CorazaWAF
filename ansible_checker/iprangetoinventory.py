import ipaddress

def main():
    #global ipfile
    #ipfile=input("Please input full path file IP_range: ")
    createinventoty()
    print("Done")

def caculate_ip(ipblock):
    ip_range=[]
    address_block = ipaddress.IPv4Network(ipblock)
    for subnet in address_block:
        ip_range.append(str(subnet))
    return ip_range

def getaddressblock():
    address_block=[]
    text= open("ip.txt", 'r')
    for addbl in text:
        address_block.append(addbl.strip())
    return address_block

def createinventoty():
    no=1
    list_ip_range=getaddressblock()
    for ipblock in list_ip_range:
        if no > 0:
            inventory="host/batch"+str(no)+".conf"
            with open(inventory, "w") as invent:
                invent.write("[host]\n")
                for ip in caculate_ip(ipblock):
                    invent.write(ip + "\n")
                invent.writelines(["[host:vars]\n","ansible_user=audit"])
            no+=1
    with open("iptemp.txt","w") as temp:
        for ipblock in list_ip_range:
            for ip in caculate_ip(ipblock):
                temp.write(ip + ";")

if __name__ == "__main__":
    main()