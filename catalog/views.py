from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from .models import Tool, Category
from .forms import OrderForm, RegisterForm, ToolForm

def tool_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    
    tools = Tool.objects.all()
    categories = Category.objects.all()
    popular_tools = Tool.objects.filter(is_popular=True)[:3]
    
    if category_id:
        tools = tools.filter(category_id=category_id)
    if search_query:
        tools = tools.filter(name__icontains=search_query)
    
    paginator = Paginator(tools, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/tool_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'popular_tools': popular_tools,
        'selected_category': category_id,
        'search_query': search_query
    })

def tool_detail(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    return render(request, 'catalog/tool_detail.html', {'tool': tool})

def add_to_cart(request):
    if request.method == 'POST':
        tool_id = request.POST.get('tool_id')
        tool = get_object_or_404(Tool, id=tool_id)
        cart = request.session.get('cart', {})
        
        new_quantity = cart.get(tool_id, 0) + 1
        if new_quantity > tool.stock:
            return JsonResponse({'status': 'error', 'message': f'Недостаточно товара "{tool.name}" на складе (в наличии: {tool.stock} шт.)'})
        
        cart[tool_id] = new_quantity
        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart_count': sum(cart.values())})
    return JsonResponse({'status': 'error'})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('catalog:tool_list')
    else:
        form = RegisterForm()
    return render(request, 'catalog/register.html', {'form': form})

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for tool_id, quantity in cart.items():
        tool = get_object_or_404(Tool, id=tool_id)
        item_total = tool.price * quantity
        cart_items.append({
            'tool': tool,
            'quantity': quantity,
            'total': item_total
        })
        total_price += item_total
    
    return render(request, 'catalog/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def update_cart(request):
    if request.method == 'POST':
        tool_id = request.POST.get('tool_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})
        
        if action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart[tool_id] = quantity
            else:
                cart.pop(tool_id, None)
        elif action == 'remove':
            cart.pop(tool_id, None)
        
        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart_count': sum(cart.values())})
    return JsonResponse({'status': 'error'})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for tool_id, quantity in cart.items():
        tool = get_object_or_404(Tool, id=tool_id)
        if quantity > tool.stock:
            return render(request, 'catalog/checkout.html', {
                'error': f'Недостаточно товара "{tool.name}" на складе (в наличии: {tool.stock} шт.)',
                'cart_items': cart_items,
                'total_price': total_price
            })
        item_total = tool.price * quantity
        cart_items.append({
            'tool': tool,
            'quantity': quantity,
            'total': item_total
        })
        total_price += item_total
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_details = "Новый заказ:\n\n"
            order_details += f"Имя: {form.cleaned_data['name']}\n"
            order_details += f"Email: {form.cleaned_data['email']}\n"
            order_details += f"Телефон: {form.cleaned_data['phone']}\n"
            order_details += f"Адрес: {form.cleaned_data['address']}\n\n"
            order_details += "Товары:\n"
            for item in cart_items:
                order_details += f"- {item['tool'].name} ({item['quantity']} шт.) - {item['total']} руб.\n"
            order_details += f"\nИтого: {total_price} руб."

            send_mail(
                'Новый заказ в ToolShop',
                order_details,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Уменьшаем количество на складе
            for item in cart_items:
                item['tool'].stock -= item['quantity']
                item['tool'].save()
            
            request.session['cart'] = {}
            return redirect('catalog:order_success')
    else:
        form = OrderForm()
    
    return render(request, 'catalog/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })

def order_success(request):
    return render(request, 'catalog/order_success.html')

@login_required
def add_tool(request):
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:tool_list')
    else:
        form = ToolForm()
    return render(request, 'catalog/add_tool.html', {'form': form})