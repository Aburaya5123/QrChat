#!/bin/bash
set -e


while IFS="=" read -r key value; do
  [[ $key == \#* || -z $key || -z $value ]] && continue

  value=$(echo "$value" | tr -d  ' "'"'"'\t\r\n')
  key=$(echo "$key" | tr -d  ' "'"'"'\t\r\n')                         
 
  if [[ -n $key && -n $value ]]; then
    key="${key^^}" 
    export "$key=$value"
  else
    echo "Error: Invalid format in ./deployment-settings.tfvars." >&2
    exit 1
  fi
done < ./deployment-settings.tfvars


cp -f ./deployment-settings.tfvars ./remote_container/terraform/terraform.tfvars


gcloud init

if which sudo > /dev/null; then
  sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin --assume-yes
else 
  apt-get install google-cloud-sdk-gke-gcloud-auth-plugin --assume-yes
fi

gcloud auth application-default login
gcloud auth application-default set-quota-project ${GCP_PROJECT_ID}

terraform_version=$(terraform -version | head -1 | awk '{print $2}')
if [[ "$terraform_version" < "v1.9.2" ]]; then
        wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
        sudo apt update && sudo apt install terraform
fi

cd ./remote_container/terraform
terraform init
terraform plan
terraform apply -auto-approve
export REDIS_HOST_IP=$(terraform output -raw redis_ip_address)
export STATIC_BUCKET_NAME=$(terraform output -raw static_bucket_name)
export MEDIA_BUCKET_NAME=$(terraform output -raw media_bucket_name) 


gcloud container clusters get-credentials $PROJECT_NAME-container-cluster --zone $GCP_REGION --project $GCP_PROJECT_ID


cd ../../
tmpfile=$(mktemp)
envsubst < ./cloudbuild.yaml > "$tmpfile"
gcloud builds submit --config "$tmpfile" .
rm "$tmpfile"


cd remote_container/kubernetes/deploy
kubectl apply -f frontend-config.yaml
kubectl apply -f backend-config.yaml
envsubst < managed-cert.yaml | kubectl apply -f -
sleep 15

set +e 
service_name=$(yq -r '.metadata.name' service.yaml)
ingress_name=$(yq -r '.metadata.name' managed-cert-ingress.yaml)
deploy_name=$(yq -r '.metadata.name' deployment.yaml)
namespace="default"

if kubectl get service $service_name -n $namespace > /dev/null 2>&1; then
  kubectl delete -f service.yaml
fi
if kubectl get ingress $ingress_name -n $namespace > /dev/null 2>&1; then
  kubectl delete -f managed-cert-ingress.yaml
fi
if kubectl get deployments $deploy_name -n $namespace > /dev/null 2>&1; then
  kubectl delete -f deployment.yaml
fi
set -e 

envsubst < deployment.yaml | kubectl apply -f -
sleep 5
kubectl apply -f service.yaml
sleep 10
envsubst < managed-cert-ingress.yaml | kubectl apply -f -