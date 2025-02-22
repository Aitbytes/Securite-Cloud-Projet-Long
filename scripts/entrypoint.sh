#!/bin/bash

# Start SSH agent and add key
eval $(ssh-agent -s)
if [ -f "/home/appuser/.ssh/id_rsa" ]; then
    chmod 600 /home/appuser/.ssh/id_rsa
    ssh-add /home/appuser/.ssh/id_rsa
fi

# Configure Git if environment variables are provided
if [ ! -z "$GIT_EMAIL" ]; then
    git config --global user.email "$GIT_EMAIL"
fi

if [ ! -z "$GIT_NAME" ]; then
    git config --global user.name "$GIT_NAME"
fi

# Add GitHub to known hosts
ssh-keyscan github.com >> /home/appuser/.ssh/known_hosts

git clone git@github.com:Aitbytes/Securite-Cloud-Projet-Long.git
# Execute the Python script with provided arguments
exec python /app/script.py --credentials-file /app/creds.json --output /app/Securite-Cloud-Projet-Long/content/docs/ --process "$@"
