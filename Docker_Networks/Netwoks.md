# Docker Networks Guide

## What are Docker Networks and Why Do We Need Them?

Docker networks provide communication pathways between containers and between containers and the external world. By default, Docker creates a virtual network infrastructure that allows containers to communicate securely and efficiently.

### Understanding Network Components:

#### **eth0 (Ethernet Interface)**
- The primary network interface on the host system
- Connects the host to the external network (internet/LAN)
- Physical or virtual network adapter

#### **docker0 (Docker Bridge)**
- Default bridge network created by Docker daemon
- Acts as a virtual switch connecting containers
- IP range typically: 172.17.0.0/16
- All containers connect to this bridge by default

#### **veth (Virtual Ethernet Pairs)**
- Virtual network interfaces created for each container
- Come in pairs: one end inside container, one end on host
- Enable communication between container and docker0 bridge
- Example: veth123abc (host side) ↔ eth0 (container side)

### Why Secure Networks Matter:

1. **Isolation**: Separate different application tiers (database, web, cache)
2. **Security**: Control which containers can communicate with each other
3. **Compliance**: Meet regulatory requirements for network segmentation
4. **Performance**: Reduce network traffic and improve performance
5. **Debugging**: Easier to troubleshoot network issues in isolated environments

## Practical Network Demonstration

### Step 1: Create and Test Default Network Communication

#### Create the first container:
```bash
docker run -d --name login nginx:latest
```

#### Access the container and install network tools:
```bash
docker exec -it login /bin/bash
```

Inside the container, install ping utility:
```bash
apt update
apt-get install iputils-ping -y
ping -V
```

This installs the ping command to test network connectivity.

#### Create a second container (in a new terminal):
```bash
docker run -d --name logout nginx:latest
```

#### Check the logout container's IP address:
```bash
docker inspect logout
```

Look for the `IPAddress` field in the output. You'll see something like:
```json
"IPAddress": "172.17.0.3"
```

#### Optional: Check login container IP:
```bash
docker inspect login
```

You'll notice both containers are in the same subnet (172.17.0.0/16 - the default docker0 bridge).

#### Test connectivity between containers:
Go back to the login container terminal and ping the logout container:
```bash
ping 172.17.0.3
```

**Result**: The ping works because both containers are on the same default bridge network!

## Docker Network Management Commands

### List all networks:
```bash
docker network ls
```

Shows all available networks:
```
NETWORK ID     NAME      DRIVER    SCOPE
abc123def456   bridge    bridge    local
def456ghi789   host      host      local
ghi789jkl012   none      null      local
```

### Remove a network:
```bash
docker network rm <network_name>
```

**Note**: You cannot remove a network that has containers attached to it.

### Create a custom secure network:
```bash
docker network create secure-network
```

This creates an isolated network separate from the default bridge.

## Implementing Network Isolation

### Create a container on the secure network:
```bash
docker run -d --name finance --network=secure-network nginx:latest
```

### Inspect the finance container:
```bash
docker inspect finance
```

You'll see detailed network information in the `NetworkSettings` section:

```json
"NetworkSettings": {
    "Bridge": "",
    "SandboxID": "6527860063d4ef48078d7f2f5dac3151c8a94d6797b36c60bd891629ccc45ba4",
    "SandboxKey": "/var/run/docker/netns/6527860063d4",
    "Ports": {
        "80/tcp": null
    },
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
    "EndpointID": "",
    "Gateway": "",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "",
    "IPPrefixLen": 0,
    "IPv6Gateway": "",
    "MacAddress": "",
    "Networks": {
        "secure-network": {
            "IPAMConfig": null,
            "Links": null,
            "Aliases": null,
            "MacAddress": "02:42:ac:13:00:02",
            "NetworkID": "0618d2288902b1f6618f104a8face73c0156c66c64cd4de02985a309020b116c",
            "EndpointID": "ad6d69a5f1c8f1fccb2790d50f4fdd0e5f889117c5094173ebe4c0b0eae8f0fe",
            "Gateway": "172.19.0.1",
            "IPAddress": "172.19.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "DriverOpts": null,
            "DNSNames": [
                "finance",
                "82c76408885e"
            ]
        }
    }
}
```

### Key Observations:

1. **No IP in default network**: Notice that `"IPAddress": ""` is empty in the main NetworkSettings
2. **IP only in secure-network**: The IP address `172.19.0.2` appears only under `"secure-network"`
3. **Different subnet**: The secure network uses `172.19.0.0/16` instead of `172.17.0.0/16`
4. **Isolated environment**: This container is completely isolated from the default bridge network

### Test Network Isolation:

Go back to the login container terminal and try to ping the finance container:
```bash
ping 172.19.0.2
```

**Result**: The ping will **fail** because:
- `login` container is on the default bridge network (172.17.0.0/16)
- `finance` container is on the secure-network (172.19.0.0/16)
- These networks are isolated from each other

This demonstrates **complete network isolation** - containers on different custom networks cannot communicate with each other, providing security through network segmentation.

## Host Network Mode

### Connect container directly to host network:
```bash
docker run -d --name demo --network=host nginx:latest
```

### Inspect the demo container:
```bash
docker inspect demo
```

**Key Observation**: No IP address assigned because the container uses the host's network stack directly.

```json
"NetworkSettings": {
    "Bridge": "",
    "SandboxID": "",
    "SandboxKey": "",
    "Ports": {},
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
    "EndpointID": "",
    "Gateway": "",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "",
    "IPPrefixLen": 0,
    "IPv6Gateway": "",
    "MacAddress": "",
    "Networks": {}
}
```

## Network Types Explained

### 1. Bridge (Default)
- **Purpose**: Default network for containers
- **Isolation**: Containers can communicate with each other
- **Use Case**: Development, simple applications

### 2. Host
- **Purpose**: Container uses host's network stack
- **Isolation**: No network isolation from host
- **Use Case**: High-performance applications, network debugging

### 3. None
- **Purpose**: No network connectivity
- **Isolation**: Complete network isolation
- **Use Case**: Security-critical applications, batch processing

### 4. Custom Networks
- **Purpose**: User-defined networks for specific requirements
- **Isolation**: Complete isolation between different custom networks
- **Use Case**: Multi-tier applications, microservices

## Network Security Best Practices

1. **Principle of Least Privilege**: Only allow necessary network connections
2. **Network Segmentation**: Use separate networks for different application tiers
3. **Custom Networks**: Avoid using the default bridge for production
4. **Firewall Rules**: Implement host-level firewall rules
5. **Regular Audits**: Review network configurations regularly
6. **DNS Resolution**: Use container names instead of IP addresses
7. **Encrypted Communication**: Use TLS/SSL for inter-container communication

## Common Network Patterns

### Three-Tier Architecture:
```bash
# Frontend network
docker network create frontend-net

# Backend network  
docker network create backend-net

# Database network
docker network create database-net

# Web server (frontend + backend networks)
docker run -d --name web --network=frontend-net nginx:latest
docker network connect backend-net web

# Application server (backend + database networks)
docker run -d --name app --network=backend-net myapp:latest
docker network connect database-net app

# Database (database network only)
docker run -d --name db --network=database-net postgres:latest
```

This setup ensures:
- Web server can communicate with app server
- App server can communicate with database
- Web server **cannot** directly access database
- Each tier is properly isolated

## Troubleshooting Network Issues

### Check container connectivity:
```bash
# Test DNS resolution
docker exec container_name nslookup other_container

# Test port connectivity
docker exec container_name telnet target_ip port

# Check routing table
docker exec container_name route -n

# View network interfaces
docker exec container_name ip addr show
```

This comprehensive guide covers Docker networking fundamentals, practical implementation, and security considerations for containerized applications.