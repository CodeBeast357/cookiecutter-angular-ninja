# Install tilt
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash

# Install angular CLI and it's dependencies
curl -sL https://deb.nodesource.com/setup_18.x | bash
apt update
apt install -y nodejs
npm install -g @angular/cli

# Install python requirements
apt install -y python-is-python3 python3-pip python3-venv
