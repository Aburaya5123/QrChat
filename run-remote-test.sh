#!/bin/bash
set -e

apt-get install google-cloud-sdk-gke-gcloud-auth-plugin --assume-yes

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


cd ./remote_container/terraform
terraform init
terraform plan
terraform apply -auto-approve
export STATIC_IP=$(terraform output -raw static_ip_address)


gcloud container clusters get-credentials $PROJECT_NAME-container-cluster --zone $GCP_REGION --project $GCP_PROJECT_ID


try() {
  set +e
  "$@"
  local exit_status=$?
  set -e
  return $exit_status
}
catch() {
  helm upgrade external-secrets external-secrets/external-secrets -n external-secrets
}

helm repo add external-secrets https://charts.external-secrets.io
try helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace || catch

cd ../../
tmpfile=$(mktemp)
envsubst < ./cloudbuild.yaml > "$tmpfile"
gcloud builds submit --config "$tmpfile" .
rm "$tmpfile"


cd ./remote_container/kubernetes/external-secrets
envsubst < cluster-secret-store.yaml | kubectl apply -f -
sleep 5
kubectl apply -f external-secret.yaml
sleep 10

cd ../deploy
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