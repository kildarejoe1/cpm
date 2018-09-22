import sys
import requests

VERIFY_SSL = False
URL_API = "https://{host}/api/"
URL_TOKEN_OBTAIN = URL_API + "token/obtain/api_key/"
URL_TOKEN_REFRESH = URL_API + "token/refresh/"
URL_POLICIES = URL_API + "policies/"
HEADER_ACCEPT = "application/json; version=1.0"
HEADER_AUTHORIZATION = "Bearer {access_token}"
URL_GET_EC2_INSTANCE = URL_API + "policies/{policy_id}/targets/instances/"
URL_SEARCH = URL_API + "resources/?search={search}"
URL_OPTIONS = URL_API + "policies/{id}/options/"

def set_cpm_api():
  cpm_api_key= str(raw_input("Please enter your CPM API key: "))
  return cpm_api_key

def set_cpm_host_ip():
  cpm_host= str(raw_input("Please FQDN/IP address of CPM Backup server: "))
  return cpm_host

def post_obtain_token(host, api_key):
  """ Post obtain token Methood """
  url = URL_TOKEN_OBTAIN.format(host=host)
  headers = {'Accept': HEADER_ACCEPT}
  data = {'api_key': api_key}
  response = requests.post(url=url, headers=headers, data=data, verify=VERIFY_SSL)
  assert response.status_code == 200
  response_json = response.json()
  access_token = response_json['access']
  refresh_token = response_json['refresh']
  return access_token, refresh_token

def post_refresh_token(host, refresh_token):
  url = URL_TOKEN_REFRESH.format(host=host)
  headers = {'Accept': HEADER_ACCEPT}
  data = {'refresh': refresh_token}
  response = requests.post(url=url, headers=headers, data=data, verify=VERIFY_SSL)
  assert response.status_code == 200
  response_json = response.json()
  access_token = response_json['access']
  return access_token

def get_all_policies(host, access_token):
  url = URL_POLICIES.format(host=host)
  authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
  headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
  response = requests.get(url=url, headers=headers, verify=VERIFY_SSL)
  #assert response.status_code == 200
  all_policies = response.json()
  # Getting list of users with the first access token
  print("Printing the list of policies in CPM on host: {}".format(host))
  for dict in all_policies:
      print(dict["name"])
  return all_policies


def get_all_policies_id(host, access_token):
  url = URL_POLICIES.format(host=host)
  authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
  headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
  response = requests.get(url=url, headers=headers, verify=VERIFY_SSL)
  #assert response.status_code == 200
  all_policies = response.json()
  # Getting list of users with the first access token
  policies_ids=[]
  for dict in all_policies:
      policies_ids.append(dict["id"])
  return policies_ids


def list_all_ec2(host, access_token):
  url = URL_POLICIES.format(host=host)
  authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
  headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
  response = requests.get(url=url, headers=headers, verify=VERIFY_SSL)
  #assert response.status_code == 200
  all_policies = response.json()
  policies_ids=[] #empty list
  ec2_inst_list=[]
  for dict in all_policies:
       policies_ids.append(dict["id"])
  for policy_id in policies_ids:
             url = URL_GET_EC2_INSTANCE.format(host=host,policy_id=policy_id)
             authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
             headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
             response = requests.get(url=url, headers=headers, verify=VERIFY_SSL)
             response_json = response.json()
             for ec2 in response_json:
                 ec2_inst_list.append(ec2["name"])
  print("Printing the CPM Protected Instances")
  for instance in ec2_inst_list:
      print(instance)

def search_policy(host,access_token,search):
  url = URL_SEARCH.format(host=host,search=search)
  authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
  headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
  response = requests.get(url=url, headers=headers, verify=VERIFY_SSL)
  print(response)

def create_policy(host,access_token):
  account_id=str(raw_input("Please enter your account id: "))
  policy_name=str(raw_input("Please enter policy_name: "))
  policy_description=str(raw_input("Please enter policy_description: "))
  enabled=str(raw_input("Should policy be enabled/disabled: "))
  if enabled == "enabled":
      enabled = True
  else:
      enabled = False
  print(enabled)
  url = URL_POLICIES.format(host=host)
  authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
  headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
  data = {"account" : account_id, "description" : policy_description, "enabled" : enabled, "name" : policy_name }
  response = requests.post(url=url, headers=headers, data=data, verify=VERIFY_SSL)
  print(response)
  assert response.status_code == 201
  response_json = response.json()

def set_backup_script_option(host,api_key):
    pass

def set_timeout_option(host,access_token):
    timeout=int(raw_input("Input the minimum timeout value to set all policies too : \n"))
    policy_id_list=get_all_policies_id(host, api_key)
    for id in policy_id_list:
        url = URL_OPTIONS.format(host=host,id=id)
        authorization = HEADER_AUTHORIZATION.format(access_token=access_token)
        headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}
        data = {"agent_script_timeout" : timeout,"collect_script_output" : True, "enable_agent_scripts" : True   }
        response = requests.put(url=url, headers=headers, data=data, verify=VERIFY_SSL)
        response_json = response.json()
    print("Returning to menu...")


def policy_options(host,api_key,option):
  if option == 1:
      set_backup_script_option(host,api_key)
  elif option == 2:
      set_timeout_option(host,api_key)
  else:
      print("No valid option selected, returning")
      return

  access_token, refresh_token = post_obtain_token(host=host, api_key=api_key)
