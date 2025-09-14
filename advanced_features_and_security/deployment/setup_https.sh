#!/bin/bash

# HTTPS Deployment Setup Script for Django Application
# This script helps set up HTTPS configuration for the Django application

set -e

echo "🔒 Setting up HTTPS for Django Application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Create necessary directories
print_status "Creating deployment directories..."
mkdir -p /opt/django-app/{ssl,logs,backups}
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/apache2/sites-available

# Set up environment variables
print_status "Setting up environment variables..."
cat > /opt/django-app/.env << EOF
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

print_warning "Please update the .env file with your actual values!"

# Generate self-signed certificate for testing (replace with real certificate in production)
print_status "Generating self-signed SSL certificate for testing..."
openssl req -x509 -newkey rsa:4096 -keyout /opt/django-app/ssl/private.key \
    -out /opt/django-app/ssl/certificate.crt -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"

# Set proper permissions
chmod 600 /opt/django-app/ssl/private.key
chmod 644 /opt/django-app/ssl/certificate.crt

# Copy configuration files
print_status "Copying configuration files..."
cp nginx_https.conf /etc/nginx/sites-available/django-https
cp apache_https.conf /etc/apache2/sites-available/django-https.conf

# Enable Nginx site
if command -v nginx &> /dev/null; then
    print_status "Enabling Nginx HTTPS site..."
    ln -sf /etc/nginx/sites-available/django-https /etc/nginx/sites-enabled/
    nginx -t && print_status "Nginx configuration is valid"
fi

# Enable Apache site
if command -v apache2 &> /dev/null; then
    print_status "Enabling Apache HTTPS site..."
    a2ensite django-https
    a2enmod ssl rewrite headers
    apache2ctl configtest && print_status "Apache configuration is valid"
fi

# Create systemd service for Django
print_status "Creating systemd service for Django..."
cat > /etc/systemd/system/django-app.service << EOF
[Unit]
Description=Django HTTPS Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/django-app
EnvironmentFile=/opt/django-app/.env
ExecStart=/opt/django-app/venv/bin/python manage.py runserver 127.0.0.1:8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Set up log rotation
print_status "Setting up log rotation..."
cat > /etc/logrotate.d/django-app << EOF
/opt/django-app/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload django-app
    endscript
}
EOF

# Create backup script
print_status "Creating backup script..."
cat > /opt/django-app/backup.sh << 'EOF'
#!/bin/bash
# Backup script for Django application
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/django-app/backups"
APP_DIR="/opt/django-app"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
cp "$APP_DIR/db.sqlite3" "$BACKUP_DIR/db_$DATE.sqlite3"

# Backup media files
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" -C "$APP_DIR" media/

# Backup configuration
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" -C "$APP_DIR" .env

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "*.sqlite3" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

chmod +x /opt/django-app/backup.sh

# Set up cron job for backups
print_status "Setting up automated backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/django-app/backup.sh") | crontab -

print_status "HTTPS setup completed!"
print_warning "Next steps:"
echo "1. Update /opt/django-app/.env with your actual values"
echo "2. Replace self-signed certificate with real SSL certificate"
echo "3. Update domain names in configuration files"
echo "4. Test the configuration:"
echo "   - For Nginx: sudo nginx -t && sudo systemctl reload nginx"
echo "   - For Apache: sudo apache2ctl configtest && sudo systemctl reload apache2"
echo "5. Start the Django service: sudo systemctl enable django-app && sudo systemctl start django-app"
echo "6. Test HTTPS access: curl -I https://your-domain.com"

print_status "Security checklist:"
echo "✅ HTTPS redirects configured"
echo "✅ HSTS headers enabled"
echo "✅ Secure cookies configured"
echo "✅ Security headers implemented"
echo "✅ SSL/TLS configuration optimized"
echo "✅ Rate limiting configured"
echo "✅ Backup system implemented"
