# Please rename the file to "terraform.tfvars" 
#  and place it under "./terraform" directory for use.
#
# ------------------------------------------------------------
# CHANGE VALUES
# From here
#
# Do not use "_" for values

project_name  = "your-service-name"
gcp_project_id    = "data-frame-427010-k5"
gcp_region        = "asia-northeast1"

dns_name          = "www.qrchat.aburaya5123.com"

db_name           = "your-database-name"
db_user_name      = "your-database-user"
db_user_password  = "your-database-password"

# https://djecrety.ir/
django_secret_key = "wd+(!srq4j46s%=bam3!2cvx^ni-#c+pa!sg4ob$j2d7yarj_)"


# To here
# ------------------------------------------------------------

django_debug_mode = "False"

cloud_function_source = "./cloud_function_source"
cloud_function_entry_point = "entry_point"