#!/bin/bash
# EC2 Production Deployment Script
# Run this on a fresh Ubuntu 22.04 LTS EC2 instance
# Usage: curl -fsSL https://your-domain/deploy.sh | bash

set -euo pipefail

echo "=========================================="
echo "Trading Backtester - EC2 Production Setup"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as ubuntu user
if [ "$USER" != "ubuntu" ]; then
    echo -e "${RED}Error: This script must be run as the 'ubuntu' user${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Updating system packages...${NC}"
sudo apt-get update && sudo apt-get upgrade -y

echo -e "${YELLOW}Step 2: Installing Docker and Docker Compose...${NC}"
sudo apt-get install -y \
    docker.io \
    docker-compose \
    git \
    curl \
    htop \
    wget \
    vim

echo -e "${YELLOW}Step 3: Adding ubuntu user to docker group...${NC}"
sudo usermod -aG docker ubuntu
newgrp docker

echo -e "${YELLOW}Step 4: Creating application directory...${NC}"
mkdir -p /app
cd /app

echo -e "${YELLOW}Step 5: Cloning repository...${NC}"
# Update this URL to your repository
git clone https://github.com/YOUR_USERNAME/algo-trading.git .

echo -e "${YELLOW}Step 6: Setting up production environment...${NC}"
# Check if .env already exists to avoid overwriting
if [ -f .env ]; then
    echo -e "${YELLOW}Warning: .env file already exists. Skipping creation.${NC}"
else
    # Copy example and show instructions
    cp .env.prod.example .env
    echo -e "${RED}=========================================="
    echo "IMPORTANT: Edit .env with your configuration:"
    echo "=========================================="
    echo "sudo nano .env"
    echo ""
    echo "Required fields:"
    echo "  - DB_ROOT_PASSWORD (strong password)"
    echo "  - DB_PASSWORD (strong password)"
    echo "  - KITE_API_KEY"
    echo "  - KITE_API_SECRET"
    echo "  - KITE_ACCESS_TOKEN"
    echo "=========================================="
    echo -e "${NC}"
    
    exit 1
fi

echo -e "${YELLOW}Step 7: Building Docker images...${NC}"
sudo docker-compose -f docker-compose.prod.yml build

echo -e "${YELLOW}Step 8: Starting services...${NC}"
sudo docker-compose -f docker-compose.prod.yml up -d

echo -e "${GREEN}=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Verify services are running:"
echo "   docker-compose -f docker-compose.prod.yml ps"
echo ""
echo "2. Check backend logs:"
echo "   docker-compose -f docker-compose.prod.yml logs backend"
echo ""
echo "3. Test the API:"
echo "   curl http://localhost/api/v1/stocks"
echo ""
echo "4. Setup domain and TLS (see PRODUCTION_DEPLOYMENT.md)"
echo ""
echo "5. Setup monitoring and backups"
echo -e "${GREEN}=========================================="
