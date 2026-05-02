# note: there might be the error due to different system
# Kubernetes Tools Setup on WSL2 Ubuntu

Complete guide for installing Kubernetes CLI tools and Minikube cluster on WSL2 Ubuntu with Docker Desktop backend.

## 📋 Overview

This setup includes:

| Tool | Purpose |
|------|---------|
| **kubectl** | Official Kubernetes CLI for cluster management |
| **Minikube** | Local single-node Kubernetes cluster (uses Docker driver) |
| **k9s** | Terminal UI for Kubernetes (visual cluster management) |
| **kubecolor** | Colorful kubectl output for better readability |
| **Helm** | Kubernetes package manager (like apt for K8s) |
| **Kustomize** | Template-free Kubernetes configuration management |

## 🎯 Why This Setup?

- **Minikube with Docker driver** uses Docker Desktop's container runtime from WSL2
- **Docker Desktop Kubernetes should be DISABLED** (use Minikube instead)
- Perfect for **AI/ML development**, local testing, and learning Kubernetes
- Suitable for your AI solution architect career progression

## ⚙️ Prerequisites

Before starting:

1. **Docker Desktop installed on Windows** (with WSL2 backend enabled)
2. **WSL2 Ubuntu installed** (e.g., Ubuntu 22.04)
3. **Docker Desktop Kubernetes DISABLED** (Settings → Kubernetes → Uncheck "Enable Kubernetes")

---

## 🚀 Installation Steps

### Step 1: Update System & Install Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget ca-certificates gnupg apt-transport-https
```

### Step 2: Install kubectl

```bash
# Download latest kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make executable and install
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify installation
kubectl version --client
```

### Step 3: Install Minikube

```bash
# Download latest Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install to system path
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

# Verify installation
minikube version
```

### Step 4: Install Helm

```bash
# Download and install Helm (official script method)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version
```

### Step 5: Install Kustomize

```bash
# Download latest Kustomize automatically
VERSION=$(curl -s https://api.github.com/repos/kubernetes-sigs/kustomize/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
curl -LO "https://github.com/kubernetes-sigs/kustomize/releases/download/${VERSION}/kustomize_${VERSION#v}_linux_amd64.tar.gz"

# Extract and install
tar -xzf kustomize_${VERSION#v}_linux_amd64.tar.gz
sudo mv kustomize /usr/local/bin/kustomize
sudo chmod +x /usr/local/bin/kustomize
rm kustomize_${VERSION#v}_linux_amd64.tar.gz

# Verify installation
kustomize version
```

### Step 6: Install k9s (GUI Terminal UI)

**Option A: Install via snap (recommended)**
```bash
sudo snap install k9s
```

**Option B: Install via symlink (if already installed via snap)**
```bash
sudo ln -s /snap/k9s/current/bin/k9s /usr/bin/k9s
```

**Verify installation**
```bash
k9s version
```

### Step 7: Install kubecolor (Colorful kubectl output)

```bash
# Download latest version
VERSION=$(curl -s https://api.github.com/repos/kubecolor/kubecolor/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
curl -LO "https://github.com/kubecolor/kubecolor/releases/download/${VERSION}/kubecolor_${VERSION#v}_linux_amd64.tar.gz"

# Extract and install
tar -xzf kubecolor_${VERSION#v}_linux_amd64.tar.gz
sudo mv kubecolor /usr/local/bin/
rm kubecolor_${VERSION#v}_linux_amd64.tar.gz

# Verify installation
kubecolor version
```

### Step 8: Enable Docker Access in WSL2

```bash
# Add current user to docker group
sudo usermod -aG docker $USER

# Apply group changes without logout
newgrp docker
```

### Step 9: Start Minikube Cluster

**First, delete any existing cluster (clean start)**
```bash
minikube delete
```

**Start Minikube with Docker driver**
```bash
minikube start --driver=docker --cpus=4 --memory=4g --kubernetes-version=v1.30.0
```

> **Note**: First start takes 3-5 minutes. The command creates a Docker container running Kubernetes.

### Step 10: Configure kubectl with kubecolor (Optional but Recommended)

```bash
# Add kubecolor alias to ~/.bashrc
echo '' >> ~/.bashrc
echo '# Use kubecolor for colored kubectl output' >> ~/.bashrc
echo 'alias kubectl="kubecolor"' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc
```

### Step 11: Install Bash Completion (Optional)

```bash
# Install bash-completion package
sudo apt install -y bash-completion

# Add completions to ~/.bashrc
echo '' >> ~/.bashrc
echo '# Kubernetes tools completion' >> ~/.bashrc
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'source <(helm completion bash)' >> ~/.bashrc
echo 'source <(k9s completion bash)' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc
```

---

## ✅ Verification Checklist

Run these commands to verify everything is working:

```bash
# Check all tool versions
echo "=== kubectl ==="
kubectl version --client

echo "=== minikube ==="
minikube version

echo "=== helm ==="
helm version

echo "=== kustomize ==="
kustomize version

echo "=== k9s ==="
k9s version

echo "=== kubecolor ==="
kubecolor version

# Check cluster status
echo "=== Cluster Nodes ==="
kubectl get nodes

# Check system pods
echo "=== System Pods ==="
kubectl get pods -A
```

Expected output:
- **kubectl**: Client Version: v1.x.x
- **minikube**: v1.x.x
- **Cluster**: minikube node should be READY
- **Pods**: All kube-system pods should be Running

---

## 📖 Quick Usage Guide

### Basic kubectl Commands

```bash
# View cluster nodes
kubectl get nodes

# View all pods in all namespaces (colored with kubecolor alias)
kubectl get pods -A

# Deploy an application
kubectl apply -f deployment.yaml

# View logs
kubectl logs <pod-name>

# Execute into pod
kubectl exec -it <pod-name> -- bash

# Delete a pod
kubectl delete pod <pod-name>
```

### k9s (Interactive Terminal UI)

```bash
# Launch k9s GUI
k9s

# Common k9s keyboard shortcuts
# :pods - View pods
# :deployments - View deployments
# :logs - View logs
# namespace/<name> - Switch namespace
# q - Quit
```

### Helm Commands

```bash
# Search for charts
helm search repo

# Install a chart (e.g., PostgreSQL)
helm install my-db bitnami/postgresql

# List installed releases
helm list

# Uninstall release
helm uninstall my-db

# Add custom repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Kustomize Commands

```bash
# Build Kustomize manifests
kustomize build ./overlays/dev

# Apply Kustomize manifests
kubectl apply -k ./overlays/production

# With kubectl (built-in kustomize)
kubectl kustomize ./base
kubectl apply -k ./overlays/dev
```

### Minikube Commands

```bash
# Start cluster
minikube start --driver=docker --cpus=4 --memory=4g

# Stop cluster
minikube stop

# Delete cluster
minikube delete

# View cluster status
minikube status

# Open dashboard
minikube dashboard
```

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Desktop (Windows)               │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Docker Engine (Container Runtime)               │   │
│  │  - Minikube uses this via Docker driver          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   WSL2 Ubuntu                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Minikube Cluster (Docker container)             │   │
│  │  ┌─────────────────────────────────────────┐   │   │
│  │  │  Kubernetes Control Plane               │   │   │
│  │  │  • kube-apiserver, etcd, scheduler       │   │   │
│  │  │  • coreDNS, kube-proxy                   │   │   │
│  │  └─────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  CLI Tools: kubectl, k9s, helm, kustomize, kubecolor    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### kubectl can't connect to cluster
```bash
# Check Minikube is running
minikube status

# Restart Minikube
minikube stop
minikube start --driver=docker --cpus=4 --memory=4g

# Check kubectl context
kubectl config current-context
# Should show: minikube
```

### Permission denied when accessing Docker
```bash
# Re-add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or restart WSL2
wsl --shutdown
```

### k9s not found after snap install
```bash
# Create symlink
sudo ln -s /snap/k9s/current/bin/k9s /usr/bin/k9s

# Or use full path
/snap/k9s/current/bin/k9s
```

### kubecolor not showing colors
```bash
# Check alias is set
alias kubectl
# Should show: alias kubectl='kubecolor'

# Reload bashrc
source ~/.bashrc
```

---

## 📚 Additional Resources

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [k9s Documentation](https://k9scli.io/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kustomize Documentation](https://kustomize.io/)
- [Kubernetes Official Docs](https://kubernetes.io/docs/)

---

## 🗑️ Uninstall/Reset Everything

```bash
# Stop and delete Minikube cluster
minikube delete --all --purge

# Remove CLI tools (optional)
sudo rm /usr/local/bin/kubectl
sudo rm /usr/local/bin/minikube
sudo rm /usr/local/bin/helm
sudo rm /usr/local/bin/kustomize
sudo rm /usr/local/bin/kubecolor
sudo rm /usr/bin/k9s  # if symlink

# Remove user directories
rm -rf ~/.minikube
rm -rf ~/.kube
rm -rf ~/.helm

# Clean Docker containers (optional - WARNING: deletes all containers)
docker system prune -a
```

---

## 👤 Author

**Janak** - AI/ML Engineer & Data Scientist  
Location: Darmstadt, Germany  
Project: AI Solution Architecture & Kubernetes Learning

---

## 📝 License

This setup guide is open source and free to use for learning and development purposes.

---

**Last Updated**: May 2026  
**Kubernetes Version**: v1.30.0  
**Minikube Version**: Latest  
**Docker Driver**: docker-desktop
