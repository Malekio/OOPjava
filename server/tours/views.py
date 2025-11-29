from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg, Count, Min, Max, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Tour
from .serializers import (
    TourListSerializer,
    TourDetailSerializer,
    TourCreateUpdateSerializer,
    TourPriceCalculationSerializer
)
from profiles.models import GuideProfile
from locations.models import Wilaya
from bookings.models import Booking

class TourListCreateView(generics.ListCreateAPIView):
    """
    List tours with search, filter and sorting capabilities
    Create new tours (guides only)
    """
    queryset = Tour.objects.select_related('guide', 'wilaya')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['wilaya', 'status']
    search_fields = ['title', 'description', 'wilaya__name_en', 'guide__user__first_name', 'guide__user__last_name']
    ordering_fields = ['price', 'duration_hours', 'created_at', 'average_rating']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TourCreateUpdateSerializer
        return TourListSerializer
    
    def get_permissions(self):
        """
        Different permissions for different actions
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Only show active tours to general public
        if self.request.method == 'GET' and (
            not self.request.user.is_authenticated or 
            not hasattr(self.request.user, 'guide_profile')
        ):
            queryset = queryset.filter(status='active')
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by duration
        min_duration = self.request.query_params.get('min_duration')
        max_duration = self.request.query_params.get('max_duration')
        if min_duration:
            queryset = queryset.filter(duration_hours__gte=min_duration)
        if max_duration:
            queryset = queryset.filter(duration_hours__lte=max_duration)
        
        # Filter by group size
        min_group_size = self.request.query_params.get('min_group_size')
        max_group_size = self.request.query_params.get('max_group_size')
        if min_group_size:
            # Filter tours that can accommodate at least the minimum requested size
            queryset = queryset.filter(max_group_size__gte=min_group_size)
        if max_group_size:
            # Since there's no min_group_size field, we assume all tours accept 1+ people
            # So we don't need to filter further for max_group_size requests
            pass
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        
        return queryset.annotate(
            booking_count=Count('bookings'),
            review_count=Count('reviews')
        )
    
    def create(self, request, *args, **kwargs):
        # Check if user is a guide
        if not hasattr(request.user, 'guide_profile'):
            return Response(
                {'error': 'Only guides can create tours'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Set the guide to the current user's guide profile
        guide = self.request.user.guide_profile
        
        # Calculate price based on duration and guide's pricing
        duration = serializer.validated_data['duration_hours']
        price = guide.calculate_tour_price(float(duration))
        
        # Save the tour with guide and calculated price
        serializer.save(guide=guide, price=price)

class TourSearchView(generics.ListAPIView):
    """
    Advanced tour search with multiple criteria
    """
    serializer_class = TourListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['wilaya']
    search_fields = ['title', 'description', 'wilaya__name_en']
    ordering_fields = ['price', 'duration_hours', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Tour.objects.filter(status='active').select_related('guide', 'wilaya')
        
        # Additional filtering
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(wilaya__name_en__icontains=query) |
                Q(guide__user__first_name__icontains=query) |
                Q(guide__user__last_name__icontains=query)
            )
        
        # Price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.annotate(
            booking_count=Count('bookings'),
            review_count=Count('reviews')
        )

class MyToursView(generics.ListAPIView):
    """
    List tours created by the authenticated guide
    """
    serializer_class = TourListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'status', 'price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'guide_profile'):
            return Tour.objects.none()
        
        return Tour.objects.filter(
            guide=self.request.user.guide_profile
        ).select_related('wilaya').annotate(
            booking_count=Count('bookings'),
            review_count=Count('reviews')
        )

class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tour
    """
    queryset = Tour.objects.select_related('guide', 'wilaya').prefetch_related('reviews')
    serializer_class = TourDetailSerializer
    
    def get_permissions(self):
        """
        Different permissions for different actions
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TourCreateUpdateSerializer
        return TourDetailSerializer
    
    def update(self, request, *args, **kwargs):
        tour = self.get_object()
        
        # Check if user is the guide who owns this tour
        if not hasattr(request.user, 'guide_profile') or tour.guide != request.user.guide_profile:
            return Response(
                {'error': 'You can only edit your own tours'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        tour = self.get_object()
        
        # Check if user is the guide who owns this tour
        if not hasattr(request.user, 'guide_profile') or tour.guide != request.user.guide_profile:
            return Response(
                {'error': 'You can only delete your own tours'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if tour has any pending or confirmed bookings
        active_bookings = tour.bookings.filter(
            status__in=['pending', 'confirmed', 'in_progress']
        )
        if active_bookings.exists():
            return Response(
                {'error': 'Cannot delete tour with active bookings'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)

class TourPriceCalculationView(generics.RetrieveAPIView):
    """
    Calculate tour price based on group size and options
    """
    queryset = Tour.objects.filter(status='active')
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        tour = self.get_object()
        group_size = int(request.query_params.get('group_size', 1))
        
        # Validate group size (minimum is 1, maximum is from tour settings)
        min_group_size = 1
        if group_size < min_group_size or group_size > tour.max_group_size:
            return Response(
                {
                    'error': f'Group size must be between {min_group_size} and {tour.max_group_size}',
                    'min_group_size': min_group_size,
                    'max_group_size': tour.max_group_size
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        base_price = tour.price
        total_price = base_price * group_size
        
        # Apply group discounts (example business logic)
        from decimal import Decimal
        discount = Decimal('0')
        if group_size >= 10:
            discount = Decimal('0.15')  # 15% discount for groups of 10+
        elif group_size >= 6:
            discount = Decimal('0.10')  # 10% discount for groups of 6+
        elif group_size >= 4:
            discount = Decimal('0.05')  # 5% discount for groups of 4+
        
        discount_amount = total_price * discount
        final_price = total_price - discount_amount
        
        return Response({
            'tour_id': tour.id,
            'tour_title': tour.title,
            'group_size': group_size,
            'base_price_per_person': base_price,
            'subtotal': total_price,
            'discount_percentage': float(discount * 100),
            'discount_amount': round(discount_amount, 2),
            'final_price': round(final_price, 2),
            'currency': 'DZD',
            'min_group_size': 1,
            'max_group_size': tour.max_group_size
        })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_tours(request):
    """
    List popular tours based on bookings and ratings
    """
    tours = Tour.objects.filter(
        status='active'
    ).select_related('guide', 'wilaya').annotate(
        booking_count=Count('bookings', filter=Q(bookings__status='completed')),
        review_count=Count('reviews', filter=Q(reviews__is_approved=True))
    ).order_by('-booking_count', '-review_count')[:10]
    
    serializer = TourListSerializer(tours, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def guide_dashboard(request):
    """
    Dashboard view for guides to see their tours and statistics
    """
    if not hasattr(request.user, 'guide_profile'):
        return Response(
            {'error': 'Only guides can access this endpoint'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    guide = request.user.guide_profile
    tours = Tour.objects.filter(guide=guide).annotate(
        booking_count=Count('bookings'),
        completed_bookings=Count('bookings', filter=Q(bookings__status='completed'))
    )
    
    # Calculate statistics
    total_tours = tours.count()
    active_tours = tours.filter(status='active').count()
    total_bookings = Booking.objects.filter(tour__guide=guide).count()
    completed_bookings = Booking.objects.filter(tour__guide=guide, status='completed').count()
    
    # Recent activity
    recent_bookings = Booking.objects.filter(
        tour__guide=guide
    ).select_related('tour', 'tourist').order_by('-created_at')[:5]
    
    return Response({
        'guide_info': {
            'name': f"{guide.user.first_name} {guide.user.last_name}",
            'rating': guide.average_rating,
            'total_reviews': guide.review_count
        },
        'statistics': {
            'total_tours': total_tours,
            'active_tours': active_tours,
            'total_bookings': total_bookings,
            'completed_bookings': completed_bookings,
            'completion_rate': round((completed_bookings / total_bookings * 100) if total_bookings > 0 else 0, 2)
        },
        'tours': TourListSerializer(tours, many=True, context={'request': request}).data,
        'recent_bookings': [
            {
                'id': booking.id,
                'tour_title': booking.tour.title,
                'tourist_name': f"{booking.tourist.user.first_name} {booking.tourist.user.last_name}",
                'status': booking.status,
                'created_at': booking.created_at,
                'total_price': booking.total_price
            }
            for booking in recent_bookings
        ]
    })
