# Social Media API - Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Social Media API to production. Multiple deployment options are covered including Heroku, AWS, DigitalOcean, and Docker.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Heroku Deployment](#heroku-deployment)
3. [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
4. [DigitalOcean with Docker](#digitalocean-with-docker)
5. [Manual VPS Deployment](#manual-vps-deployment)
6. [Post-Deployment Tasks](#post-deployment-tasks)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### 1. Environment Setup

- [ ] Copy `ENV_TEMPLATE.txt` to `.env` and fill in production values
- [ ] Generate a strong SECRET_KEY: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure email service (SMTP)
- [ ] Set up Redis for caching (optional but recommended)

### 2. Code Preparation

```bash
# Install production dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```

### 3. Security Configuration

Ensure these settings are configured in production:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
```

---

## Heroku Deployment

### Prerequisites

- Heroku account
- Heroku CLI installed
- Git repository initialized

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Or use existing app
heroku git:remote -a your-app-name
```

### Step 3: Configure Environment Variables

```bash
# Set SECRET_KEY
heroku config:set SECRET_KEY="your-secret-key-here"

# Set DEBUG
heroku config:set DEBUG=False

# Set ALLOWED_HOSTS
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"

# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Add Redis (optional)
heroku addons:create heroku-redis:mini

# View all config
heroku config
```

### Step 4: Configure Django for Heroku

Ensure you have these files in your project root:
- `Procfile` ✅ (already created)
- `runtime.txt` ✅ (already created)
- `requirements.txt` ✅ (already updated)

### Step 5: Deploy

```bash
# Add changes
git add .
git commit -m "Configure for Heroku deployment"

# Push to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open app
heroku open
```

### Step 6: View Logs

```bash
# View logs
heroku logs --tail

# View specific log
heroku logs --source app --tail
```

---

## AWS Elastic Beanstalk

### Prerequisites

- AWS account
- AWS CLI installed and configured
- EB CLI installed

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB Application

```bash
# Initialize EB
eb init -p python-3.11 social-media-api --region us-east-1

# Create environment
eb create production-env
```

### Step 3: Configure Environment

Create `.ebextensions/django.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: social_media_api.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: social_media_api.settings_production
    SECRET_KEY: "your-secret-key-here"
    DEBUG: "False"
    ALLOWED_HOSTS: ".elasticbeanstalk.com"
```

### Step 4: Configure RDS Database

```bash
# Create RDS instance from AWS console
# Then set environment variables
eb setenv DB_NAME=your_db_name
eb setenv DB_USER=your_db_user
eb setenv DB_PASSWORD=your_db_password
eb setenv DB_HOST=your-rds-endpoint
eb setenv DB_PORT=5432
```

### Step 5: Deploy

```bash
# Deploy
eb deploy

# View status
eb status

# Open app
eb open
```

---

## DigitalOcean with Docker

### Prerequisites

- DigitalOcean account
- Docker installed locally
- Docker Compose installed

### Step 1: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD gunicorn social_media_api.wsgi:application --bind 0.0.0.0:8000
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=social_media_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=your_password

  redis:
    image: redis:7-alpine
    
  web:
    build: .
    command: gunicorn social_media_api.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/mediafiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/mediafiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Step 3: Create Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/mediafiles/;
        }

        location / {
            proxy_pass http://web;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_redirect off;
        }
    }
}
```

### Step 4: Deploy to DigitalOcean

```bash
# Build and run locally first
docker-compose up --build

# Push to Docker Hub
docker tag social-media-api your-dockerhub-username/social-media-api
docker push your-dockerhub-username/social-media-api

# On DigitalOcean Droplet
docker-compose -f docker-compose.prod.yml up -d
```

---

## Manual VPS Deployment (Ubuntu)

### Prerequisites

- Ubuntu 20.04+ VPS
- Root or sudo access
- Domain name pointed to VPS

### Step 1: Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3.11 python3.11-venv python3-pip nginx postgresql postgresql-contrib redis-server -y

# Create application user
sudo adduser socialmedia
sudo usermod -aG sudo socialmedia
su - socialmedia
```

### Step 2: Setup Project

```bash
# Clone repository
cd /home/socialmedia
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure PostgreSQL

```bash
# Create database
sudo -u postgres psql
postgres=# CREATE DATABASE social_media_db;
postgres=# CREATE USER socialmedia WITH PASSWORD 'your_password';
postgres=# ALTER ROLE socialmedia SET client_encoding TO 'utf8';
postgres=# ALTER ROLE socialmedia SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE socialmedia SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE social_media_db TO socialmedia;
postgres=# \q
```

### Step 4: Configure Environment

```bash
# Create .env file
cp ENV_TEMPLATE.txt .env
nano .env
# Fill in production values

# Run migrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### Step 5: Configure Gunicorn

Create `/etc/systemd/system/socialmedia.service`:

```ini
[Unit]
Description=Social Media API Gunicorn daemon
After=network.target

[Service]
User=socialmedia
Group=www-data
WorkingDirectory=/home/socialmedia/Alx_DjangoLearnLab/social_media_api
ExecStart=/home/socialmedia/Alx_DjangoLearnLab/social_media_api/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/socialmedia/Alx_DjangoLearnLab/social_media_api/gunicorn.sock \
          social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable service
sudo systemctl start socialmedia
sudo systemctl enable socialmedia
sudo systemctl status socialmedia
```

### Step 6: Configure Nginx

Create `/etc/nginx/sites-available/socialmedia`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/socialmedia/Alx_DjangoLearnLab/social_media_api;
    }

    location /media/ {
        root /home/socialmedia/Alx_DjangoLearnLab/social_media_api;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/socialmedia/Alx_DjangoLearnLab/social_media_api/gunicorn.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/socialmedia /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Setup SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## Post-Deployment Tasks

### 1. Create Superuser

```bash
# Heroku
heroku run python manage.py createsuperuser

# VPS
python manage.py createsuperuser
```

### 2. Test API Endpoints

```bash
# Health check
curl https://your-domain.com/api/

# Test authentication
curl -X POST https://your-domain.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

### 3. Configure Domain and DNS

- Point your domain A record to server IP
- Configure CNAME for www subdomain
- Wait for DNS propagation (24-48 hours)

### 4. Setup Monitoring

```bash
# Configure error logging
# Set up application monitoring (New Relic, Sentry, etc.)
# Configure uptime monitoring
```

---

## Monitoring and Maintenance

### Logging

**Heroku:**
```bash
heroku logs --tail
```

**VPS:**
```bash
# Application logs
sudo journalctl -u socialmedia -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Database Backups

**Heroku:**
```bash
# Manual backup
heroku pg:backups:capture

# Schedule backups
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles'
```

**VPS:**
```bash
# Create backup script
sudo nano /usr/local/bin/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/socialmedia/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
pg_dump -U socialmedia social_media_db > $BACKUP_DIR/backup_$TIMESTAMP.sql
find $BACKUP_DIR -type f -mtime +7 -delete  # Keep 7 days
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-db.sh

# Add to crontab
crontab -e
0 2 * * * /usr/local/bin/backup-db.sh
```

### Updates and Maintenance

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart socialmedia
sudo systemctl restart nginx
```

---

## Troubleshooting

### Common Issues

**1. Static files not loading**
```bash
python manage.py collectstatic --clear --noinput
sudo systemctl restart nginx
```

**2. Database connection errors**
- Check database credentials in .env
- Verify database is running
- Check firewall rules

**3. Permission errors**
```bash
sudo chown -R socialmedia:www-data /home/socialmedia/
sudo chmod -R 755 /home/socialmedia/
```

**4. 502 Bad Gateway**
```bash
# Check gunicorn is running
sudo systemctl status socialmedia

# Check nginx configuration
sudo nginx -t

# Check socket file permissions
ls -l /path/to/gunicorn.sock
```

### Getting Help

- Check application logs
- Review Nginx error logs
- Check gunicorn logs
- Review PostgreSQL logs
- Check system resources (CPU, memory, disk)

---

## Security Best Practices

1. ✅ Never commit `.env` file to version control
2. ✅ Use strong, unique SECRET_KEY
3. ✅ Keep DEBUG=False in production
4. ✅ Configure ALLOWED_HOSTS properly
5. ✅ Use HTTPS (SSL/TLS)
6. ✅ Enable all security headers
7. ✅ Keep dependencies updated
8. ✅ Use environment variables for secrets
9. ✅ Regular security audits
10. ✅ Monitor for vulnerabilities

---

## Performance Optimization

1. **Database**
   - Use connection pooling
   - Optimize queries
   - Add database indexes
   - Regular VACUUM and ANALYZE

2. **Caching**
   - Enable Redis caching
   - Cache expensive queries
   - Use browser caching headers

3. **Static Files**
   - Use CDN for static files
   - Enable Gzip compression
   - Optimize images

4. **Application**
   - Use select_related and prefetch_related
   - Implement pagination
   - Enable API throttling

---

## Useful Commands

```bash
# Django management
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py shell

# Heroku
heroku logs --tail
heroku run python manage.py migrate
heroku ps:scale web=1
heroku restart

# Systemd (VPS)
sudo systemctl start socialmedia
sudo systemctl stop socialmedia
sudo systemctl restart socialmedia
sudo systemctl status socialmedia

# Nginx
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl reload nginx

# PostgreSQL
sudo -u postgres psql
\l  # List databases
\c database_name  # Connect to database
\dt  # List tables
```

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] SECRET_KEY changed
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configured
- [ ] Database setup and migrated
- [ ] Static files collected
- [ ] Media files storage configured
- [ ] SSL certificate installed
- [ ] Superuser created
- [ ] API endpoints tested
- [ ] Monitoring setup
- [ ] Backup system configured
- [ ] Documentation updated
- [ ] Error logging configured
- [ ] Performance tested

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Live URL:** _______________  
**Version:** 1.0.0

