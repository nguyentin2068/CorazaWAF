#!/bin/bash
# Step 1: Run Python file to create new inventory
python3 iprangetoinventory.py

# Step 2: Run Ansible playbook
for inventory_file in host/*; do
  ansible-playbook -i "$inventory_file" playbook.yml --ask-pass --ask-become-pass
  sleep 5
done

# Step 3: Run Python file to create final report
python summrize_report.py

sudo rm -rf iptemp.txt