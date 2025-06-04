
from django.shortcuts import render
import json 
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.db import models
from .models import Product, Permission, Role, UserProfile
from .auth_decorators import require_api_key, require_permission
import secrets
from django.contrib.auth.models import User

@csrf_exempt
@require_api_key
@require_permission('admin_users')
def create_api_user(request):
    """Créer un utilisateur avec clé API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            role_id = data.get('role_id')
            
            if not username:
                return JsonResponse({'error': 'Username required'}, status=400)
            
            # Créer l'utilisateur
            user = User.objects.create_user(username=username, email=email)
            
            # Générer une clé API
            api_key = secrets.token_urlsafe(32)
            
            # Récupérer le rôle
            role = None
            if role_id:
                try:
                    role = Role.objects.get(id=role_id)
                except Role.DoesNotExist:
                    pass
            
            # Créer le profil utilisateur
            user_profile = UserProfile.objects.create(
                user=user,
                role=role,
                api_key=api_key
            )
            
            return JsonResponse({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'api_key': api_key,
                    'role': role.name if role else None
                }
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_api_key
@require_permission('admin_roles')
def create_role(request):
    """Créer un rôle avec permissions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
            permission_codes = data.get('permissions', [])
            
            if not name:
                return JsonResponse({'error': 'Role name required'}, status=400)
            
            # Créer le rôle
            role = Role.objects.create(name=name, description=description)
            
            # Ajouter les permissions
            for code in permission_codes:
                try:
                    permission = Permission.objects.get(code=code)
                    role.permissions.add(permission)
                except Permission.DoesNotExist:
                    pass
            
            return JsonResponse({
                'message': 'Role created successfully',
                'role': {
                    'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'permissions': list(role.permissions.values('code', 'name'))
                }
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Vue publique (pas d'autorisation)
def test_json_view(request): 
    data = { 
        'name': 'John Doe', 
        'age': 30, 
        'location': 'New York', 
        'is_active': True, 
        } 
    return JsonResponse(data)

@csrf_exempt
@require_api_key
@require_permission('create_user')
def post_user(request): 
    if request.method == 'POST': 
        try: 
            data = json.loads(request.body) 
            user = data.get('user')
            response_data = { 
                'message': 'User created successfully', 
                'user': { 
                    'user': user
                },
                'created_by': request.user.username
            } 
            return JsonResponse(response_data, status=201) 

        except json.JSONDecodeError: 
            return JsonResponse({'error': 'Invalid JSON'}, status=400) 

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_api_key
@require_permission('view_products')
def get_allproducts(request): 
    products = list(Product.objects.values('id', 'name', 'price', 'description', 'created_at', 'updated_at'))
    return JsonResponse({
        'products': products,
        'accessed_by': request.user.username
    }, safe=False)

@csrf_exempt
@require_api_key
@require_permission('view_products')
def get_maxprice(request): 
    try:
        most_expensive_product = Product.objects.order_by('-price').first()
        
        if most_expensive_product is not None:
            response_data = {
                'message': 'Most expensive product found',
                'product': {
                    'id': most_expensive_product.id,
                    'name': most_expensive_product.name,
                    'price': str(most_expensive_product.price),
                    'description': most_expensive_product.description,
                    'created_at': most_expensive_product.created_at.isoformat(),
                    'updated_at': most_expensive_product.updated_at.isoformat()
                },
                'accessed_by': request.user.username
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'No products found'}, status=404)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_api_key
@require_permission('create_products')
def post_product(request): 
    if request.method == 'POST': 
        try: 
            data = json.loads(request.body) 
            
            if isinstance(data, list):
                products_data = data
            elif isinstance(data, dict):
                products_data = [data]
            else:
                return JsonResponse({'error': 'Invalid data format'}, status=400)
            
            if len(products_data) > 3:
                return JsonResponse({'error': 'Maximum 3 products allowed per request'}, status=400)
            
            created_products = []
            errors = []
            
            for i, product_data in enumerate(products_data):
                name = product_data.get('name') 
                price = product_data.get('price') 
                description = product_data.get('description', '') 

                if not name or not price: 
                    errors.append(f'Product {i+1}: Name and price are required')
                    continue
                
                try:
                    product = Product.objects.create(name=name, price=price, description=description)
                    created_products.append({
                        'id': product.id, 
                        'name': product.name, 
                        'price': str(product.price), 
                        'description': product.description, 
                        'created_at': product.created_at.isoformat()
                    })
                except Exception as e:
                    errors.append(f'Product {i+1}: {str(e)}')
            
            response_data = {
                'message': f'{len(created_products)} product(s) created successfully',
                'products': created_products,
                'created_by': request.user.username
            }
            
            if errors:
                response_data['errors'] = errors
            
            if created_products:
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({'error': 'No products were created', 'errors': errors}, status=400)

        except json.JSONDecodeError: 
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_api_key
@require_permission('update_products')
def update_product(request, product_id):
    if request.method == 'PUT': 
        try: 
            data = json.loads(request.body) 
            
            try: 
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist: 
                return JsonResponse({'error': f'Product with id {product_id} not found'}, status=404)
            
            if 'name' in data:
                product.name = data['name']
            if 'price' in data:
                product.price = data['price']
            if 'description' in data:
                product.description = data['description']
            
            if not product.name or not product.price:
                return JsonResponse({'error': 'Name and price cannot be empty'}, status=400)
            
            product.save()
            
            response_data = { 
                'message': 'Product updated successfully', 
                'product': { 
                    'id': product.id, 
                    'name': product.name, 
                    'price': str(product.price), 
                    'description': product.description,
                    'created_at': product.created_at.isoformat(),
                    'updated_at': product.updated_at.isoformat()
                },
                'updated_by': request.user.username
            } 
            
            return JsonResponse(response_data, status=200) 

        except json.JSONDecodeError: 
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed. Use PUT method.'}, status=405)
