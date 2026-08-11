#!/bin/bash
# Ubuntu Development Environment Setup Script

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing common development tools..."
sudo apt install -y git curl wget build-essential python3-pip python3-venv nodejs npm zstd

echo "Installing Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

echo "Setting up GitHub CLI..."
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y

echo "Setup complete! You are ready to develop."
