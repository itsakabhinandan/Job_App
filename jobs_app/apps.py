from django.apps import AppConfig


def create_groups_with_permissions():
    from jobs_app.models import Job
    from django.contrib.auth.models import Group, Permission
    from django.db.models.signals import post_migrate
    from django.contrib.contenttypes.models import ContentType

    permissions = (
        ('can_access_recruiter_dashboard', 'Can Access Recruiter Dashboard'),
        ('can_create_job', 'Can Create Job'),
    )
    perm_objs = []
    ct = ContentType.objects.get_for_model(Job)
    for perm in permissions:
        try:
            p = Permission.objects.get(
                codename=perm[0],
                name=perm[1]
            )
            perm_objs.append(p)
        except Permission.DoesNotExist:
            p = Permission.objects.create(
                codename=perm[0],
                name=perm[1],
                content_type=ct
            )
            perm_objs.append(p)
    
    try:
        group = Group.objects.get(
            name='recruiter'
        )
        group.permissions.set(perm_objs)
    except Group.DoesNotExist:
        group = Group.objects.create(
            name='recruiter'
        )
        Group.permissions.set(perm_objs)


class JobsAppConfig(AppConfig):
    name = 'jobs_app'

    def ready(self):
        print(self, 'ready')
        create_groups_with_permissions()