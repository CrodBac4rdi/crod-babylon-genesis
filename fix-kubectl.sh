#!/bin/bash
# FIX KUBECTL PERMANENTLY EVERYWHERE

# 1. Add to bashrc
echo 'export KUBECONFIG=/home/daniel/.kube/config' >> ~/.bashrc

# 2. Add to profile
echo 'export KUBECONFIG=/home/daniel/.kube/config' >> ~/.profile

# 3. Add to bash_profile if exists
if [ -f ~/.bash_profile ]; then
    echo 'export KUBECONFIG=/home/daniel/.kube/config' >> ~/.bash_profile
fi

# 4. Add to zshrc if using zsh
if [ -f ~/.zshrc ]; then
    echo 'export KUBECONFIG=/home/daniel/.kube/config' >> ~/.zshrc
fi

# 5. Create alias for safety
echo 'alias k="export KUBECONFIG=/home/daniel/.kube/config && kubectl"' >> ~/.bashrc

# 6. System-wide fix (run with sudo)
echo '# Add this to /etc/environment:'
echo 'KUBECONFIG="/home/daniel/.kube/config"'

echo ""
echo "✅ DONE! Run these commands:"
echo "1. source ~/.bashrc"
echo "2. sudo echo 'KUBECONFIG=\"/home/daniel/.kube/config\"' >> /etc/environment"
echo ""
echo "Then kubectl will work EVERYWHERE, ALWAYS!"