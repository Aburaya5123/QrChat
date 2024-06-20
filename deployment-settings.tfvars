# Please rename the file to "terraform.tfvars" 
#  and place it under "./terraform" directory for use.
#
# ------------------------------------------------------------
# CHANGE VALUES
# From here
#
# Do not use '_' for values

project_name  = "your-service-name"
gcp_project_id    = "your-project-id"
gcp_region        = "your-region"

dns_name          = "your-domain-name"

db_name           = "your-database-name"
db_user_name      = "your-database-user"
db_user_password  = "your-database-password"

# https://djecrety.ir/
django_secret_key = "generated-key"


# To here
# ------------------------------------------------------------

django_debug_mode = "False"

cloud_function_source      = "./cloud_function_source"
cloud_function_entry_point = "entry_point"