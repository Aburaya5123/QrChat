#!/bin/bash

secret_folder_path="./local_container/secret_keys/"
root_password_fname="root_password.txt"
user_password_fname="user_password.txt"
django_secret_fname="django_secret.txt"

w_rp=false
w_up=false
w_ds=false
run_backgroud=false

function usage() {
  echo $1
  cat <<_EOT_
Usage:
  `basename $0` [--rootpw arg] [--userpw arg] [--djangosr arg] [-h] [-d]

Description:
  When starting for the first time, specify values with options --rootpw, --userpw, and --djangosr to create secret files.
  The secret files will be created under the directory ./secret_keys with the following file names:
    - $root_password_fname
    - $user_password_fname
    - $django_secret_fname
  If all secret files already exist, there is no need to specify options.
  The contents to be specified with options are as follows.
  
Options:
  -rootpw ROOT_PASSWORD for MySQL
  -userpw USER_PASSWORD for MySQL
  -djangosr SECRET_KEY for Django
  -h HELP
  -d run background

_EOT_
  exit 1
}

while getopts hd-: opt; do
    optarg="${!OPTIND}"
    [[ "$opt" = - ]] && opt="$OPTARG"

    case "$opt" in
        "rootpw")
            rootpw="$optarg"
            shift
            ;;
        "userpw")
            userpw="$optarg"
            shift
            ;;
        "djangosr")
            djangosr="$optarg"
            shift
            ;;
        "h")
            usage "[HELP]"
            ;;
        "d")
            run_backgroud=true
            shift
            ;;
        "")
            usage "[ERROR] Option argument is undefined."
            ;;
        *)
            usage "[ERROR] Undefined options ${opt##-}"
            ;;
    esac
done
shift $((OPTIND - 1))


if [ ! -f "$secret_folder_path$root_password_fname" ]; then
  if [ -n "$rootpw" ]; then
    w_rp=true
  else
    usage "[ERROR] Please specify --rootpw."
  fi
fi

if [ ! -f "$secret_folder_path$user_password_fname" ]; then
  if [ -n "$userpw" ]; then
    w_up=true
  else
    usage "[ERROR] Please specify --userpw."
  fi
fi

if [ ! -f "$secret_folder_path$django_secret_fname" ]; then
  if [ -n "$djangosr" ]; then
    w_ds=true
  else
    usage "[ERROR] Please specify --djangosr."
  fi
fi


if "${w_rp}"; then
  echo "$rootpw" > $secret_folder_path$root_password_fname
  echo "rootpw written to $secret_folder_path$root_password_fname."
fi

if "${w_up}"; then
  echo "$userpw" > $secret_folder_path$user_password_fname
  echo "userpw written to $secret_folder_path$user_password_fname."
fi

if "${w_ds}"; then
  echo "$djangosr" > $secret_folder_path$django_secret_fname
  echo "djangosr written to $secret_folder_path$django_secret_fname."
fi

chmod 0444 $secret_folder_path$root_password_fname
chmod 0444 $secret_folder_path$user_password_fname
chmod 0444 $secret_folder_path$django_secret_fname


cd local_container

if "${w_up}"; then
    docker compose up --build -d
else
    docker compose up --build
fi