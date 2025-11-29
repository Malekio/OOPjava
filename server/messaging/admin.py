from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from .models import Conversation, Message, CustomTourRequest

class MessageInline(admin.TabularInline):
    """Inline admin for Messages in Conversation"""
    model = Message
    extra = 0
    fields = ('sender_type', 'content', 'is_read', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin interface for Conversations"""
    list_display = ['subject', 'tourist', 'guide', 'message_count', 'last_message_at', 
                    'has_unread_messages', 'created_at']
    list_filter = ['created_at', 'last_message_at']
    search_fields = ['subject', 'tourist__user__username', 'tourist__user__first_name', 
                     'tourist__user__last_name', 'guide__user__username', 
                     'guide__user__first_name', 'guide__user__last_name']
    readonly_fields = ['created_at', 'message_count', 'last_message_at']
    inlines = [MessageInline]
    ordering = ['-last_message_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('tourist', 'guide')
        }),
        ('Conversation Details', {
            'fields': ('subject',)
        }),
        ('Statistics', {
            'fields': ('message_count', 'last_message_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def message_count(self, obj):
        """Display number of messages in conversation"""
        if hasattr(obj, 'message_count_annotated'):
            return obj.message_count_annotated
        return obj.messages.count()
    message_count.short_description = 'Messages'
    
    def last_message_at_display(self, obj):
        """Display last message date"""
        return obj.last_message_at
    last_message_at_display.short_description = 'Last Message'
    
    def has_unread_messages(self, obj):
        """Check if conversation has unread messages"""
        unread_count = obj.messages.filter(is_read=False).count()
        if unread_count > 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">● {} unread</span>',
                unread_count
            )
        return format_html('<span style="color: green;">✓ All read</span>')
    has_unread_messages.short_description = 'Read Status'
    
    def get_queryset(self, request):
        """Optimize queryset with related data and annotations"""
        return super().get_queryset(request).select_related(
            'tourist__user', 'guide__user'
        ).prefetch_related('messages').annotate(
            message_count_annotated=Count('messages')
        )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Messages"""
    list_display = ['conversation_title', 'sender_type', 'content_preview', 'is_read', 
                    'read_status_icon', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['conversation__subject', 'content']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('conversation', 'sender_type', 'content')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def conversation_title(self, obj):
        """Display conversation title"""
        return obj.conversation.subject
    conversation_title.short_description = 'Conversation'
    
    def content_preview(self, obj):
        """Display truncated message content"""
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Message'
    
    def read_status_icon(self, obj):
        """Display read status with icon"""
        if obj.is_read:
            return format_html('<span style="color: green;">✓ Read</span>')
        return format_html('<span style="color: orange;">○ Unread</span>')
    read_status_icon.short_description = 'Status'
    
    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related(
            'conversation__tourist__user', 'conversation__guide__user'
        )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Action to mark selected messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages were marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_unread(self, request, queryset):
        """Action to mark selected messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} messages were marked as unread.')
    mark_as_unread.short_description = 'Mark as unread'

@admin.register(CustomTourRequest)
class CustomTourRequestAdmin(admin.ModelAdmin):
    """Admin interface for Custom Tour Requests"""
    list_display = ['title', 'tourist', 'guide', 'preferred_date', 'duration_hours', 
                    'budget', 'status', 'status_icon', 'created_at']
    list_filter = ['status', 'preferred_date', 'duration_hours', 'created_at']
    search_fields = ['title', 'description', 'tourist__user__username', 
                     'tourist__user__first_name', 'tourist__user__last_name',
                     'guide__user__username', 'guide__user__first_name', 'guide__user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'status_icon']
    ordering = ['-created_at']
    date_hierarchy = 'preferred_date'
    
    fieldsets = (
        ('Request Details', {
            'fields': ('tourist', 'guide', 'title', 'description')
        }),
        ('Tour Specifications', {
            'fields': ('preferred_date', 'duration_hours', 'group_size', 'budget')
        }),
        ('Special Requirements', {
            'fields': ('special_requirements',)
        }),
        ('Guide Response', {
            'fields': ('status', 'status_icon', 'proposed_price', 'alternative_date', 'guide_response'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_icon(self, obj):
        """Display status with appropriate icon and color"""
        status_icons = {
            'pending': '<span style="color: orange;">⏳ Pending</span>',
            'accepted': '<span style="color: green;">✅ Accepted</span>',
            'rejected': '<span style="color: red;">❌ Rejected</span>',
        }
        return format_html(status_icons.get(obj.status, obj.status))
    status_icon.short_description = 'Status'
    
    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related(
            'tourist__user', 'guide__user'
        )
    
    actions = ['accept_requests', 'reject_requests', 'reset_to_pending']
    
    def accept_requests(self, request, queryset):
        """Action to accept selected requests"""
        updated = queryset.filter(status='pending').update(status='accepted')
        self.message_user(request, f'{updated} requests were accepted.')
    accept_requests.short_description = 'Accept selected requests'
    
    def reject_requests(self, request, queryset):
        """Action to reject selected requests"""
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} requests were rejected.')
    reject_requests.short_description = 'Reject selected requests'
    
    def reset_to_pending(self, request, queryset):
        """Action to reset selected requests to pending"""
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} requests were reset to pending.')
    reset_to_pending.short_description = 'Reset to pending'
    
    def changelist_view(self, request, extra_context=None):
        """Add custom tour request statistics to changelist"""
        extra_context = extra_context or {}
        
        # Get request statistics
        queryset = self.get_queryset(request)
        total_requests = queryset.count()
        pending_requests = queryset.filter(status='pending').count()
        accepted_requests = queryset.filter(status='accepted').count()
        rejected_requests = queryset.filter(status='rejected').count()
        
        extra_context['request_stats'] = {
            'total': total_requests,
            'pending': pending_requests,
            'accepted': accepted_requests,
            'rejected': rejected_requests,
            'acceptance_rate': round((accepted_requests / total_requests * 100) if total_requests > 0 else 0, 1),
        }
        
        return super().changelist_view(request, extra_context)
