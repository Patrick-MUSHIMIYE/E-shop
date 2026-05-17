#!/bin/bash
set -e

echo "=== JerseyDrop Setup ==="

# Install dependencies
pip install Django Pillow --break-system-packages -q

# Run migrations
python manage.py makemigrations store
python manage.py migrate

# Load sample data
python manage.py loaddata store/fixtures/initial_data.json

# Create superuser (non-interactive)
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@jerseydrop.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Run the dev server with:"
echo "  cd jerseydrop && python manage.py runserver"
echo ""
echo "Admin panel: http://127.0.0.1:8000/admin"
echo "  username: admin | password: admin123"
