# 
# If you want to run Terraform without using 'run-remote.sh',
#   please rename the file to "terraform.tfvars" 
#     and place it under "./remote_container/terraform" directory for use.
#
# ------------------------------------------------------------
# CHANGE VALUES
# From here
#
# Do not use '_' for values

project_name      = "your-service-name"
gcp_project_id    = "mytest-427106"
gcp_region        = "asia-northeast2"

dns_name          = "www.qrchat.aburaya5123.com"

db_name           = "your-database-name"
db_user_name      = "your-database-user"
db_user_password  = "your-database-password"

# https://djecrety.ir/
django_secret_key = "d3vr*$a%y*zm0+9u2ly+a=e8ynja1xa(q70^d!-92rl8!hnx#%"


# To here
# ------------------------------------------------------------

django_debug_mode = "False"

cloud_function_source      = "./cloud_function_source"
cloud_function_entry_point = "entry_point"