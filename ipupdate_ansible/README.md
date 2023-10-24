# AUTO UPDATE BLACKLIST IP

### Install incron service

    sudo apt-get install incron 

### Configuration acces incron

- /etc/incron.allow : If this file exists only users listed here may use incron.
- /etc/incron.deny : If this file exists only users NOT listed here may use incron.

### Start

    systemctl start incron.service 

### Crearte incrontab

    incrontab -e

Add:

    < path of blacklist file > IN_CREATE < path of auto-update.sh >

### Note:

Event Symbols (Masks): 
- IN_ACCESS File was accessed (read). 
- IN_ATTRIB Metadata changed (permissions, timestamps, extended attributes, etc.). 
- IN_CLOSE_WRITE File opened for writing was closed. 
- IN_CLOSE_NOWRITE File not opened for writing was closed. 
- IN_CREATE File/directory created in watched directory. 
- IN_DELETE File/directory deleted from watched directory. 
- IN_DELETE_SELF Watched file/directory was itself deleted. 
- IN_MODIFY File was modified. 
- IN_MOVE_SELF Watched file/directory was itself moved. 
- IN_MOVED_FROM File moved out of watched directory. 
- IN_MOVED_TO File moved into watched directory. 
- IN_OPEN File was opened.

