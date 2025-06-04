from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

class PaginationHelper:
    @staticmethod
    def paginate_queryset(queryset, page_number, page_size=3):
        """
        Paginer un queryset avec gestion d'erreurs
        
        Args:
            queryset: Le queryset Django à paginer
            page_number: Numéro de la page demandée
            page_size: Nombre d'éléments par page (défaut: 3)
        
        Returns:
            dict: Données paginées avec métadonnées
        """
        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.get_page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.get_page(1)
        
        return {
            'items': list(page_obj),
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'items_per_page': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'start_index': page_obj.start_index(),
                'end_index': page_obj.end_index()
            }
        }

    @staticmethod
    def create_pagination_response(data, message="Data retrieved successfully"):
        """
        Créer une réponse JSON standardisée avec pagination
        
        Args:
            data: Données retournées par paginate_queryset
            message: Message de succès
        
        Returns:
            JsonResponse: Réponse formatée
        """
        response_data = {
            'message': message,
            'data': data['items'],
            'pagination': data['pagination']
        }
        return JsonResponse(response_data)