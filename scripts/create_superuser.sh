#!/bin/bash
# Run this after deployment to create the superuser
python manage.py shell << EOF
from django.contrib.auth.models import User
from accounts.models import Profile, Role

username = 'rafy'
password = '1234'

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': f'{username}@kennedymoongrill.com',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    },
)

if created:
    user.set_password(password)
    user.save()
    Profile.objects.get_or_create(
        user=user,
        defaults={
            'role': Role.ADMIN,
            'full_name': 'Rafy Admin',
            'phone': '0300-0000000',
        },
    )
    print('✓ Superuser created: rafy / 1234')
else:
    user.set_password(password)
    user.save()
    print('✓ Superuser rafy updated with password 1234')
EOF

