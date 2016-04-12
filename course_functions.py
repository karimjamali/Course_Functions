import json
import yaml
from ciscoconfparse import CiscoConfParse
import os
import string
import random
import time
from telnetlib import Telnet

def Save_Output_to_File(file_name,output):
  with open(file_name,'w') as f:
     f.write(output)

class Device_Attributes(object):
   def __init__(self,ip_addr,TELNET_PORT,TELNET_TIMEOUT,username,password):
      self.ip_addr=ip_addr
      self.TELNET_PORT=TELNET_PORT
      self.TELNET_TIMEOUT=TELNET_TIMEOUT
      self.username=username
      self.password=password
   def Login_to_device(self):
      telnet_conn=Telnet(self.ip_addr,self.TELNET_PORT,self.TELNET_TIMEOUT)
      telnet_conn.read_until('sername:')
      telnet_conn.write(self.username + '\n')
      telnet_conn.read_until('assword:')
      telnet_conn.write(self.password + '\n')
      time.sleep(1)
      output=telnet_conn.read_very_eager()
      return  telnet_conn,output
   def Send_Commands(self,telnet_conn,cmd):
      telnet_conn.write(cmd  + '\n')
      time.sleep(1)
      output=telnet_conn.read_very_eager()
      return output,cmd
   def Find_Hostname(self,telnet_conn):

def Create_Directory(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)     
  
def File_Name_Generator():
   file_name='log_file' + str(random.randint(1,100000)) + '.txt'
   return file_name

def Random_File(size=6, chars=string.ascii_uppercase + string.digits):
    random_file_name= ''.join(random.choice(chars) for _ in range(size))
    random_file=random_file_name + ".txt"
    return random_file

def Check_File_Exists(filename):
    if os.path.isfile(filename):
     return True
    else:
     return False
def Cisco_Parser(filename):
    cisco_cfg=CiscoConfParse(filename)
    interfaces=cisco_cfg.find_objects(r"^interface")
    vtys=cisco_cfg.find_objects(r"^line vty ")
    for intf in interfaces:
        output= str(intf)
        output+= '\n' +  str(intf.children)
    for vty in vtys:
        output+= '\n' + '#' * 80
        output+= "Configuration for Line vty is: \n {}".format(vty.children)
    l2_interfaces=cisco_cfg.find_objects_w_child(parentspec=r"^interface",                                                            childspec="no ip address")
    l3_interfaces=cisco_cfg.find_objects_wo_child(parentspec=r"^interface",                                                           childspec="no ip address")
    output+= '\n' +'#' * 80
    output+= "\nL2 Interfaces are {}".format(l2_interfaces)
    output+= '\n' +'#' * 80
    output+= "\nL3 Interfaces are {}".format(l3_interfaces)
    return output
def yaml_to_list(filename):
    with open(filename) as f:
        new_list=yaml.load(f)
    return new_list

def json_to_list(filename):
    with open(filename) as f:
      new_list=json.load(f)
    return new_list

def list_to_yaml(a_list):
    file_name=raw_input('What is the file you want to write to?')
    while (len(file_name)==0 or file_name.isspace()):
        file_name=raw_input('What is the file you want to write to?')
     
    file_w_ext=file_name + '.yaml'
    with open(file_w_ext, 'w') as f:
        f.write(yaml.dump(a_list,default_flow_style=False))
    return file_w_ext

def list_to_json(a_list):
    file_name=raw_input('What is the file you want to write to?')
    while (len(file_name)==0 or file_name.isspace()):
        file_name=raw_input('What is the file you want to write to?')
    file_w_ext=file_name + '.json'
    with open(file_w_ext, 'w') as f:
        json.dump(a_list,f)
    return file_w_ext

def main():
    my_list=range(8)
    my_list.append('whatever')
    my_list.append('hello')
    my_list.append({})
    my_list[-1]['ip_address']='10.1.1.1'
    my_list[-1]['attribs']=range(11)
    #Testing Conversions JSON/YAML to List & Viceversa   
    yaml_file=list_to_yaml(my_list)
    json_file=list_to_json(my_list)
    new_list_yaml=yaml_to_list(yaml_file)
    new_list_json=json_to_list(json_file)
    #print "new_list_yaml is {}" .format(new_list_yaml)
    #print "new_list_json is {}" .format(new_list_json)

    #Testing CiscoConfParse
    Parsed_Configuration=Cisco_Parser("config-file.txt")
    #print Parsed_Configuration
    rf_name=Random_File() 
    fname_generator=File_Name_Generator() 
    #print rf_name
    #print Check_File_Exists(rf_name)
    if not(Check_File_Exists(rf_name)):
      Save_Output_to_File(rf_name,Parsed_Configuration)
      
    if not(Check_File_Exists(fname_generator)):
      Save_Output_to_File(fname_generator,Parsed_Configuration)

if __name__ == '__main__':
    main() 


