from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Seed default groups (Supervisor, Worker) and sample users'

    def handle(self, *args, **options):
        # Create groups
        supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created group: Supervisor'))
        else:
            self.stdout.write(self.style.WARNING('→ Group already exists: Supervisor'))

        worker_group, created = Group.objects.get_or_create(name='Worker')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created group: Worker'))
        else:
            self.stdout.write(self.style.WARNING('→ Group already exists: Worker'))

        manager_group, created = Group.objects.get_or_create(name='Manager')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created group: Manager'))
        else:
            self.stdout.write(self.style.WARNING('→ Group already exists: Manager'))

        # Create sample users
        users_data = [
            ('supervisor1', 'supervisor1@taskflow.com', 'Super@123', 'Supervisor', 'Alice', 'Johnson'),
            ('worker1', 'worker1@taskflow.com', 'Worker@123', 'Worker', 'Bob', 'Smith'),
            ('worker2', 'worker2@taskflow.com', 'Worker@123', 'Worker', 'Carol', 'Williams'),
            ('manager1', 'manager1@taskflow.com', 'Manager@123', 'Manager', 'David', 'Brown'),
        ]

        for username, email, password, group_name, first_name, last_name in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'→ User already exists: {username}'))

            # Add user to group
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'  → Added {username} to group {group_name}'))

        # Summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Groups & Users Summary:'))
        for group in Group.objects.all():
            members = ', '.join([u.username for u in group.user_set.all()]) or 'No members'
            self.stdout.write(f'  {group.name}: {members}')

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Login credentials:'))
        for username, email, password, group_name, first_name, last_name in users_data:
            self.stdout.write(f'  {username} / {password} ({group_name})')
