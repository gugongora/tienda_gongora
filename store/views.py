from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    categoria_id = request.GET.get('categoria')
    marca_id = request.GET.get('marca')

    products = Product.objects.all()

    if categoria_id:
        products = products.filter(categoria_id=categoria_id)
    if marca_id:
        products = products.filter(marca_id=marca_id)

    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search_results.html', {'results': results, 'query': query})
from django.urls import reverse_lazy
