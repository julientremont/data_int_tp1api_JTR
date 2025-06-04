from .models import Permission, Role

def init_permissions():
    """Script pour initialiser les permissions de base"""
    permissions_data = [
        {'name': 'Voir les produits', 'code': 'view_products', 'description': 'Permet de consulter la liste des produits'},
        {'name': 'Créer des produits', 'code': 'create_products', 'description': 'Permet de créer de nouveaux produits'},
        {'name': 'Modifier des produits', 'code': 'update_products', 'description': 'Permet de modifier les produits existants'},
        {'name': 'Supprimer des produits', 'code': 'delete_products', 'description': 'Permet de supprimer des produits'},
        {'name': 'Créer des utilisateurs', 'code': 'create_user', 'description': 'Permet de créer de nouveaux utilisateurs'},
        {'name': 'Administration des utilisateurs', 'code': 'admin_users', 'description': 'Gestion complète des utilisateurs'},
        {'name': 'Administration des rôles', 'code': 'admin_roles', 'description': 'Gestion des rôles et permissions'},
    ]
    
    for perm_data in permissions_data:
        Permission.objects.get_or_create(
            code=perm_data['code'],
            defaults={
                'name': perm_data['name'],
                'description': perm_data['description']
            }
        )
    
    # Créer des rôles par défaut
    admin_role, created = Role.objects.get_or_create(
        name='Admin',
        defaults={'description': 'Administrateur avec tous les droits'}
    )
    if created:
        admin_role.permissions.set(Permission.objects.all())
    
    user_role, created = Role.objects.get_or_create(
        name='User',
        defaults={'description': 'Utilisateur standard avec droits limités'}
    )
    if created:
        user_role.permissions.set(Permission.objects.filter(code__in=['view_products']))
    
    manager_role, created = Role.objects.get_or_create(
        name='Manager',
        defaults={'description': 'Gestionnaire avec droits sur les produits'}
    )
    if created:
        manager_role.permissions.set(Permission.objects.filter(code__in=[
            'view_products', 'create_products', 'update_products'
        ]))
    
    print("Permissions et rôles initialisés avec succès!")