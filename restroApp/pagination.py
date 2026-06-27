from rest_framework.pagination import PageNumberPagination

class Mypagination(PageNumberPagination):
    page_size = 9
    
    def get_page_size(self, request):
        # Check if limit is provided in query params (used by loadFoods on homepage)
        limit = request.query_params.get('limit')
        if limit:
            try:
                return int(limit)
            except (ValueError, TypeError):
                pass
        return super().get_page_size(request)
