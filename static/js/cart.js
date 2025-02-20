$(document).ready(function() {
    $('.add-to-cart').click(function() {
        var toolId = $(this).data('tool-id');
        var addToCartUrl = $(this).data('add-to-cart-url');
        $.ajax({
            url: addToCartUrl,
            method: 'POST',
            data: {
                'tool_id': toolId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('#cart-count').text(response.cart_count);
                    $('#successToast .toast-body').text('Товар добавлен в корзину!');
                    var toast = new bootstrap.Toast($('#successToast'));
                    toast.show();
                } else if (response.status === 'error') {
                    alert(response.message);
                }
            }
        });
    });

    $('.quantity-input').change(function() {
        var toolId = $(this).data('tool-id');
        var quantity = $(this).val();
        var updateCartUrl = $(this).data('update-cart-url');
        $.ajax({
            url: updateCartUrl,
            method: 'POST',
            data: {
                'tool_id': toolId,
                'action': 'update',
                'quantity': quantity,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('#cart-count').text(response.cart_count);
                    $('#successToast .toast-body').text('Корзина обновлена!');
                    var toast = new bootstrap.Toast($('#successToast'));
                    toast.show();
                    location.reload();
                }
            }
        });
    });

    $('.remove-from-cart').click(function() {
        var toolId = $(this).data('tool-id');
        var updateCartUrl = $(this).data('update-cart-url');
        $.ajax({
            url: updateCartUrl,
            method: 'POST',
            data: {
                'tool_id': toolId,
                'action': 'remove',
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('#cart-count').text(response.cart_count);
                    $('#successToast .toast-body').text('Товар удален из корзины!');
                    var toast = new bootstrap.Toast($('#successToast'));
                    toast.show();
                    location.reload();
                }
            }
        });
    });
});