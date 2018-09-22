#Menu for application to add/update/delete settings in CPM
import cpm
import sys

def menu(host,api_key):
    """Offer menu to user.
    Global Changes:
    1. List All cpm policies
    2. List All ec2 instances protected
    3. Update all policies with extra options
    Individual policy
    1.List ec2 instances protected in a policy
    2.Create policy, add  ec2 instances to policy.
    """
    option = None

    while option != "q":
        option=str(raw_input("""Please choose from the following menu:
           1. List all CPM policies
           2. List all EC2 instance protected
           3. Search for a policy
           4. Update All polices with choosen option
           5. List EC2 protected in a policy_id
           6. Create policy, add ec2 instances to policy
           Press "q" to quit.. \n """ ))
        if option == "1":
            cpm.get_all_policies(host, api_key)
        elif option == "2":
            cpm.list_all_ec2(host, api_key)
        elif option == "3":
            search= str(raw_input("Please enter your policy name that you want to search: "))
            cpm.search_policy(host,api_key,search)
        elif option == "4":
            option= int(raw_input("""Select the Policy Option that you want to update for all Policies :
            1. Update Linux Backup Scripts enabled/disabled"
            2. Script Timeout Value \n """))
            cpm.policy_options(host,api_key,option)
        elif option == "6":
            cpm.create_policy(host, api_key)
        else:
            print("Please choose valid option!!!")



if __name__ == "__main__":
    host = cpm.set_cpm_host_ip()
    api_key = cpm.set_cpm_api()
    menu(host,api_key)
