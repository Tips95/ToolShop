$(document).ready(function() {
    console.log("Cart script loaded");

    if ($('.add-to-cart').length === 0) {
        console.log("No elements with class 'add-to-cart' found");
    }

    $('.add-to-cart').on('click', function(e) {
        e.preventDefault();
        console.log("Add to cart clicked");
        var toolId = $(this).data('tool-id');
        var addToCartUrl = $(this).data('add-to-cart-url');
        console.log("Tool ID:", toolId, "URL:", addToCartUrl);

        $.ajax({
            url: addToCartUrl,
            method: 'POST',
            data: {
                'tool_id': toolId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                console.log("AJAX success:", response);
                if (response.status === 'success') {
                    $('#cart-count').text(response.cart_count);
                    $('#successToast .toast-body').text('Товар добавлен в корзину!');
                    var toast = new bootstrap.Toast($('#successToast'));
                    toast.show();
                } else if (response.status === 'error') {
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.log("AJAX error:", status, error);
                console.log("Response text:", xhr.responseText);
                alert('Ошибка при добавлении товара в корзину: ' + error);
            }
        });
    });

    $('.quantity-input').on('change', function() {
        var toolId = $(this).data('tool-id');
        var quantity = $(this).val();
        var updateCartUrl = $(this).data('update-cart-url');
        console.log("Updating quantity for Tool ID:", toolId, "to:", quantity);

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
                console.log("Update success:", response);
                if (response.status === 'success') {
                    $('#cart-count').text(response.cart_count);
                    $('#total-price span').text(response.total_price.toFixed(2) + ' руб.');
                    $('#successToast .toast-body').text('Корзина обновлена!');
                    var toast = new bootstrap.Toast($('#successToast'));
                    toast.show();
                }
            },
            error: function(xhr, status, error) {
                console.log("Update error:", status, error);
            }
        });
    });

    $('.remove-from-cart').on('click', function(e) {
        e.preventDefault();
        var toolId = $(this).data('tool-id');
        var updateCartUrl = $(this).data('update-cart-url');
        var $row = $('#cart-item-' + toolId);
        console.log("Removing Tool ID:", toolId);

        $.ajax({
            url: updateCartUrl,
            method: 'POST',
            data: {
                'tool_id': toolId,
                'action': 'remove',
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                console.log("Remove success:", response);
                if (response.status === 'success') {
                    $('#cart-count').text(response.cart_count);
                    $('#total-price span').text(response.total_price.toFixed(2) + ' руб.');
                    $row.remove();
                    $('#successToast .toast-body').text('Товар удалён из корзины!');
                    var toast = new bootstrap.Toast($('#successToast'));
                    toast.show();

                    if ($('#cart-table tbody tr').length === 0) {
                        $('#cart-table').remove();
                        $('#total-price').remove();
                        $('.d-flex').remove();
                        var catalogUrl = $('.content-wrapper').data('catalog-url');
                        $('.content-wrapper').append('<div class="text-center py-5"><h3>Ваша корзина пуста</h3><a href="' + catalogUrl + '" class="btn btn-primary mt-3">Вернуться в каталог</a></div>');
                    }
                } else {
                    alert('Ошибка при удалении товара');
                }
            },
            error: function(xhr, status, error) {
                console.log("Remove error:", status, error);
                console.log("Response text:", xhr.responseText);
                alert('Ошибка запроса к серверу: ' + error);
            }
        });
    });
});