// Custom JavaScript for Tours Admin
(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Auto-calculate price based on guide and duration
        var $guide = $('#id_guide');
        var $duration = $('#id_duration_hours');
        var $price = $('#id_price');
        
        function calculatePrice() {
            // This would be enhanced with actual guide pricing data
            var duration = parseFloat($duration.val()) || 0;
            if (duration > 0) {
                // Placeholder calculation - would fetch guide's actual rates
                var basePrice = duration <= 4 ? 5000 : 10000;
                var extraHours = Math.max(0, duration - 4);
                var extraCost = extraHours * 1500;
                $price.val((basePrice + extraCost).toFixed(2));
            }
        }
        
        $guide.change(calculatePrice);
        $duration.change(calculatePrice);
        
        // Status color coding
        $('.field-status select').change(function() {
            var $this = $(this);
            var status = $this.val();
            $this.removeClass('status-active status-inactive status-draft');
            if (status) {
                $this.addClass('status-' + status);
            }
        }).trigger('change');
        
        // Image preview enhancement
        $('.field-image input[type="file"]').change(function() {
            var input = this;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var $preview = $('.field-image_preview img');
                    if ($preview.length === 0) {
                        $('.field-image_preview').append('<img width="100" height="60" style="border-radius: 5px;" />');
                        $preview = $('.field-image_preview img');
                    }
                    $preview.attr('src', e.target.result);
                };
                reader.readAsDataURL(input.files[0]);
            }
        });
    });
    
})(django.jQuery);
