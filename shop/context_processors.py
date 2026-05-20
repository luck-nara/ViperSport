def cart_context(request):
    cart = request.session.get('cart', {})
    count = sum(item.get('qty', 0) for item in cart.values())
    return {'cart_count': count}
