from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Reviews"""

    list_display = [
        "title",
        "tourist",
        "tour_title",
        "guide",
        "rating",
        "rating_stars",
        "is_approved",
        "has_response",
        "created_at",
    ]
    list_filter = ["rating", "is_approved", "created_at", "tour__wilaya"]
    search_fields = [
        "title",
        "comment",
        "tourist__user__username",
        "tourist__user__first_name",
        "tourist__user__last_name",
        "tour__title",
        "tour__guide__user__username",
    ]
    readonly_fields = ["created_at", "updated_at", "rating_stars"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Review Information", {"fields": ("tourist", "tour", "booking")}),
        ("Review Content", {"fields": ("rating", "rating_stars", "title", "comment")}),
        (
            "Guide Response",
            {
                "fields": ("guide_response", "guide_response_date"),
                "classes": ("collapse",),
            },
        ),
        ("Moderation", {"fields": ("is_approved",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def tour_title(self, obj):
        """Display tour title"""
        return obj.tour.title

    tour_title.short_description = "Tour"

    def guide(self, obj):
        """Display guide name"""
        return obj.tour.guide.user.get_full_name() or obj.tour.guide.user.username

    guide.short_description = "Guide"

    def rating_stars(self, obj):
        """Display rating as stars"""
        stars = "⭐" * obj.rating
        empty_stars = "☆" * (5 - obj.rating)
        return format_html(f'<span style="color: #ffc107;">{stars}</span>{empty_stars}')

    rating_stars.short_description = "Rating"

    def has_response(self, obj):
        """Check if guide has responded"""
        if obj.guide_response:
            return format_html('<span style="color: green;">✓ Responded</span>')
        return format_html('<span style="color: orange;">○ No Response</span>')

    has_response.short_description = "Guide Response"

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return (
            super()
            .get_queryset(request)
            .select_related(
                "tourist__user", "tour__guide__user", "tour__wilaya", "booking"
            )
        )

    actions = ["approve_reviews", "unapprove_reviews", "delete_selected"]

    def approve_reviews(self, request, queryset):
        """Action to approve selected reviews"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} reviews were approved successfully.")

    approve_reviews.short_description = "Approve selected reviews"

    def unapprove_reviews(self, request, queryset):
        """Action to unapprove selected reviews"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} reviews were unapproved.")

    unapprove_reviews.short_description = "Unapprove selected reviews"

    def changelist_view(self, request, extra_context=None):
        """Add review statistics to changelist"""
        extra_context = extra_context or {}

        # Get review statistics
        queryset = self.get_queryset(request)
        total_reviews = queryset.count()
        approved_reviews = queryset.filter(is_approved=True).count()
        pending_reviews = queryset.filter(is_approved=False).count()
        avg_rating = (
            queryset.filter(is_approved=True).aggregate(Avg("rating"))["rating__avg"]
            or 0
        )
        reviews_with_response = (
            queryset.exclude(guide_response__isnull=True)
            .exclude(guide_response="")
            .count()
        )

        extra_context["review_stats"] = {
            "total": total_reviews,
            "approved": approved_reviews,
            "pending": pending_reviews,
            "avg_rating": round(avg_rating, 1),
            "response_rate": round(
                (reviews_with_response / total_reviews * 100)
                if total_reviews > 0
                else 0,
                1,
            ),
        }

        return super().changelist_view(request, extra_context)

    class Media:
        css = {"all": ("admin/css/reviews.css",)}
