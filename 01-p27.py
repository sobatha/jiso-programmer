@login_required
def item_list_view(request, shop_id):
    shop = get_object_or_404
