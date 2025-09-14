# HTTPS Deployment Guide for Django Library Management System

## Overview

This guide provides step-by-step instructions for deploying the Django Library Management System with HTTPS and secure redirects. The deployment includes comprehensive security configurations for both development and production environments.

## Prerequisites

- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- Django 5.2+
- Nginx or Apache web server
- SSL certificate (Let's Encrypt recommended)
- Domain name configured

## Quick Start

### 1. Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/advanced_features_and_security

# Run the automated setup script
sudo ./deployment/setup_https.sh
```

### 2. Manual Setup

Follow the detailed steps below for manual configuration.

## Detailed Deployment Steps

### Step 1: Environment Setup

#### 1.1 Create Application Directory
```bash
sudo mkdir -p /opt/django-app
sudo chown $USER:$USER /opt/django-app
```

#### 1.2 Set Up Python Virtual Environment
```bash
cd /opt/django-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 1.3 Configure Environment Variables
```bash
cat > .env << EOF
# Django HTTPS Configuration
DEBUG=False
HTTPS_ENABLED=True
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost,127.0.0.1
SECRET_KEY=your-secret-key-here-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///opt/django-app/db.sqlite3

# SSL Certificate Paths
SSL_CERT_PATH=/opt/django-app/ssl/certificate.crt
SSL_KEY_PATH=/opt/django-app/ssl/private.key
EOF
```

### Step 2: SSL Certificate Setup

#### 2.1 Using Let's Encrypt (Recommended for Production)

```bash
# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

#### 2.2 Self-Signed Certificate (Development Only)

```bash
# Create SSL directory
sudo mkdir -p /opt/django-app/ssl

# Generate self-signed certificate
sudo openssl req -x509 -newkey rsa:4096 -keyout /opt/django-app/ssl/private.key \
    -out /opt/django-app/ssl/certificate.crt -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"

# Set proper permissions
sudo chmod 600 /opt/django-app/ssl/private.key
sudo chmod 644 /opt/django-app/ssl/certificate.crt
```

### Step 3: Web Server Configuration

#### 3.1 Nginx Configuration

```bash
# Copy Nginx configuration
sudo cp deployment/nginx_https.conf /etc/nginx/sites-available/django-https

# Update paths in configuration
sudo sed -i 's|/path/to/your/certificate.crt|/opt/django-app/ssl/certificate.crt|g' /etc/nginx/sites-available/django-https
sudo sed -i 's|/path/to/your/private.key|/opt/django-app/ssl/private.key|g' /etc/nginx/sites-available/django-https
sudo sed -i 's|/path/to/your/django/project|/opt/django-app|g' /etc/nginx/sites-available/django-https
sudo sed -i 's|your-domain.com|your-actual-domain.com|g' /etc/nginx/sites-available/django-https

# Enable site
sudo ln -sf /etc/nginx/sites-available/django-https /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

#### 3.2 Apache Configuration

```bash
# Copy Apache configuration
sudo cp deployment/apache_https.conf /etc/apache2/sites-available/django-https.conf

# Update paths in configuration
sudo sed -i 's|/path/to/your/certificate.crt|/opt/django-app/ssl/certificate.crt|g' /etc/apache2/sites-available/django-https.conf
sudo sed -i 's|/path/to/your/private.key|/opt/django-app/ssl/private.key|g' /etc/apache2/sites-available/django-https.conf
sudo sed -i 's|/path/to/your/django/project|/opt/django-app|g' /etc/apache2/sites-available/django-https.conf
sudo sed -i 's|your-domain.com|your-actual-domain.com|g' /etc/apache2/sites-available/django-https.conf

# Enable required modules
sudo a2enmod ssl rewrite headers

# Enable site
sudo a2ensite django-https
sudo a2dissite 000-default

# Test configuration
sudo apache2ctl configtest

# Reload Apache
sudo systemctl reload apache2
```

### Step 4: Django Application Setup

#### 4.1 Deploy Application Code
```bash
# Copy application files
sudo cp -r LibraryProject /opt/django-app/
sudo cp manage.py /opt/django-app/
sudo cp requirements.txt /opt/django-app/

# Set proper ownership
sudo chown -R www-data:www-data /opt/django-app
```

#### 4.2 Database Setup
```bash
cd /opt/django-app
sudo -u www-data python manage.py migrate
sudo -u www-data python manage.py collectstatic --noinput
sudo -u www-data python manage.py createsuperuser
```

#### 4.3 Create Systemd Service
```bash
sudo cp deployment/django-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable django-app
sudo systemctl start django-app
```

### Step 5: Security Configuration

#### 5.1 Firewall Configuration
```bash
# Allow HTTPS traffic
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp
sudo ufw enable
```

#### 5.2 Set Up Monitoring
```bash
# Create monitoring script
cat > /opt/django-app/monitor.sh << 'EOF'
#!/bin/bash
# Monitor HTTPS status and security headers

echo "=== HTTPS Status Check ==="
curl -I https://your-domain.com 2>/dev/null | grep -E "(HTTP|Strict-Transport-Security|X-Frame-Options)"

echo "=== SSL Certificate Check ==="
openssl s_client -connect your-domain.com:443 -servername your-domain.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

echo "=== Security Headers Check ==="
curl -I https://your-domain.com 2>/dev/null | grep -E "(X-|Strict-|Content-Security)"
EOF

chmod +x /opt/django-app/monitor.sh
```

## Testing and Validation

### 1. HTTPS Redirection Test
```bash
# Test HTTP to HTTPS redirection
curl -I http://your-domain.com
# Should return: HTTP/1.1 301 Moved Permanently
# Location: https://your-domain.com/
```

### 2. SSL Certificate Validation
```bash
# Test SSL certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

### 3. Security Headers Validation
```bash
# Test security headers
curl -I https://your-domain.com | grep -E "(Strict-Transport-Security|X-Frame-Options|X-Content-Type-Options)"
```

### 4. Online Security Testing
- **SSL Labs**: https://www.ssllabs.com/ssltest/
- **Security Headers**: https://securityheaders.com/
- **Mozilla Observatory**: https://observatory.mozilla.org/

## Maintenance and Monitoring

### 1. Automated Backups
```bash
# Set up automated backups (already configured in setup script)
crontab -l | grep backup
```

### 2. Certificate Renewal
```bash
# For Let's Encrypt certificates
sudo certbot renew --dry-run
```

### 3. Security Updates
```bash
# Regular security updates
sudo apt update && sudo apt upgrade
pip install --upgrade -r requirements.txt
```

### 4. Log Monitoring
```bash
# Monitor application logs
sudo journalctl -u django-app -f

# Monitor web server logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Troubleshooting

### Common Issues

#### 1. HTTPS Redirection Not Working
```bash
# Check Nginx configuration
sudo nginx -t

# Check if site is enabled
ls -la /etc/nginx/sites-enabled/

# Restart Nginx
sudo systemctl restart nginx
```

#### 2. SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in /opt/django-app/ssl/certificate.crt -text -noout

# Check certificate chain
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

#### 3. Django Application Not Starting
```bash
# Check service status
sudo systemctl status django-app

# Check logs
sudo journalctl -u django-app -n 50

# Test Django configuration
cd /opt/django-app
python manage.py check --deploy
```

## Security Checklist

### Pre-Deployment
- [ ] SSL certificate obtained and configured
- [ ] Domain name properly configured
- [ ] Environment variables set correctly
- [ ] Database migrations completed
- [ ] Static files collected

### Post-Deployment
- [ ] HTTPS redirection working
- [ ] Security headers present
- [ ] SSL Labs test passed (A+ rating)
- [ ] Application accessible over HTTPS
- [ ] Monitoring and logging configured
- [ ] Backup system tested

## Support and Resources

### Documentation
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Nginx SSL Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Apache SSL Configuration](https://httpd.apache.org/docs/2.4/ssl/)

### Security Resources
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---

**Deployment Guide Version**: 1.0  
**Last Updated**: $(date)  
**Compatible with**: Django 5.2+, Python 3.8+
