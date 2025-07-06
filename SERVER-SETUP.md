# SERVER_SETUP.md

This guide shows how to set up Neo4j + Flask on Hetzner Cloud.

---

## 🎯 Overview

- **Provider:** Hetzner Cloud
- **Plan:** CPX21 (3 vCPU / 4GB RAM)
- **OS:** Ubuntu 22.04
- **Components:**
  - Neo4j Community Edition
  - Python (Flask app)
  - Gunicorn
  - Nginx + Let's Encrypt

---

## 1️⃣ Provision Server

1. Create Hetzner Project.
2. Select CPX21.
3. Choose region.
4. Attach your SSH key.
5. Create server.

---

## 2️⃣ Initial Setup

SSH in:

```bash
ssh root@your.server.ip
```

Update & install essentials:

```bash
apt update && apt upgrade -y
apt install -y ufw fail2ban git curl htop
```

Create user:

```bash
adduser deploy
usermod -aG sudo deploy
```

Enable UFW:

```bash
ufw allow OpenSSH
ufw allow http
ufw allow https
ufw enable
```

Reconnect as deploy:

```bash
ssh deploy@your.server.ip
```

---

## 3️⃣ Install Neo4j

Add repo:

```bash
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg
echo "deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable 5" | sudo tee /etc/apt/sources.list.d/neo4j.list
```

Install Neo4j:

```bash
sudo apt update
sudo apt install -y neo4j
```

Enable and start:

```bash
sudo systemctl enable neo4j
sudo systemctl start neo4j
```

Edit `/etc/neo4j/neo4j.conf`:

```
dbms.connector.bolt.listen_address=127.0.0.1:7687
dbms.connector.http.listen_address=127.0.0.1:7474
dbms.memory.heap.initial_size=1G
dbms.memory.heap.max_size=1G
dbms.memory.pagecache.size=1G
dbms.default_listen_address=0.0.0.0
```

Restart:

```bash
sudo systemctl restart neo4j
```

Set new password:

```bash
cypher-shell -u neo4j -p neo4j
```

---

## 4️⃣ Install Python & Flask App

Install Python:

```bash
sudo apt install -y python3-pip python3-venv
```

Clone app:

```bash
mkdir -p ~/apps/baconometer
cd ~/apps/baconometer
git clone <your-repo-url> .
```

Install poetry

Configure poetry to use project venv:
```
poetry config virtualenvs.in-project true
```

Install dependencies:

```bash
make install-dependencies
```

Install docker
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

```

SCP .csv files to server

Stop Neo4j:
```bash
sudo systemctl restart neo4j
```

Import data:
```bash
sudo neo4j-admin database import full neo4j \
  --nodes=Actor="/home/deploy/apps/baconometer/baconometer/actors.csv" \
  --nodes=Film="/home/deploy/apps/baconometer/baconometer/films.csv" \
  --relationships=ACTED_IN="/home/deploy/apps/baconometer/baconometer/acted_in.csv" \
  --overwrite-destination=true
```

You may need to start neo4j manually via console to get into a good state for systemd. I had some issues with it coming up via systemd

Create `.env`:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=<yourpassword>
```

---

## 5️⃣ Set Up Gunicorn

Create systemd service:

```bash
sudo nano /etc/systemd/system/baconometer.service
```

Paste:

```
[Unit]
Description=baconometer Flask API
After=network.target

[Service]
User=deploy
WorkingDirectory=/home/deploy/apps/baconometer/baconometer
EnvironmentFile=/home/deploy/apps/baconometer/baconometer/.env
Environment="PATH=/home/deploy/apps/baconometer/baconometer/.venv/bin"
ExecStart=/home/deploy/apps/baconometer/baconometer/.venv/bin/gunicorn -w 3 -b localhost:8000 src.baconometer.wsgi:app


[Install]
WantedBy=multi-user.target
```

Reload and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable baconometer
sudo systemctl start baconometer
```

---

## 6️⃣ Install Nginx & TLS

Install Nginx:

```bash
sudo apt install -y nginx
```

Edit config:

```bash
sudo nano /etc/nginx/sites-available/default
```

Paste:

```
server {
    listen 80;
    server_name baconometer.foobarcat.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Test config and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Setup DNS Record:

1️⃣ **Log in to your DNS provider (e.g., Route53).**

2️⃣ **Create an A record:**

- **Name:** `baconometer`
- **Type:** A
- **Value:** *your server’s public IP*
- **TTL:** 300

Example:

| Name                        | Type | Value             |
|-----------------------------|------|-------------------|
| baconometer.foobarcat.com   | A    | 95.XX.XX.XX       |

---

3️⃣ **Verify the DNS record has propagated:**

Use `dig`:

```bash
dig +short baconometer.foobarcat.com

Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
```

Get certificate:

```bash
sudo certbot --nginx -d yourdomain.com
```

---

## 7️⃣ Set DNS Record

In Route53:

- Create A record:
  - Name: `baconometer.yourdomain.com`
  - Value: your server IP
  - TTL: 300

---

## 8️⃣ Verify

✅ Check Neo4j:

```bash
cypher-shell
```

✅ Check Flask:

```bash
curl localhost:8000
```

✅ Check HTTPS:

```
https://yourdomain.com
```

---

Check and secure your domain at:
https://securityheaders.com
https://www.ssllabs.com/ssltest/analyze.html

## 📘 Useful Commands

Restart Neo4j:

```bash
sudo systemctl restart neo4j
```

Restart app:

```bash
sudo systemctl restart baconometer
```

View logs:

```bash
journalctl -u baconometer -f
```

Check disk usage:

```bash
df -h
```

---

✅ Done! You have a production server ready to go.
