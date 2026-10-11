from django.shortcuts import render, get_object_or_404,redirect

from .models import Item 

from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import NewItemForm,EditItemForm
from .models import Item, Category
def items(request):
    query = request.GET.get('query', '').strip()
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    sort = request.GET.get('sort', 'newest')

    item_list = Item.objects.filter(is_sold=False)

    categories = Category.objects.all()

    if query:
        item_list = item_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        try:
            item_list = item_list.filter(
                Category_id=int(category_id)
            )
        except (ValueError, TypeError):
            category_id = ''

    if min_price:
        try:
            item_list = item_list.filter(
                price__gte=float(min_price)
            )
        except ValueError:
            min_price = ''

    if max_price:
        try:
            item_list = item_list.filter(
                price__lte=float(max_price)
            )
        except ValueError:
            max_price = ''

    sort_options = {
        'newest': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
    }

    if sort not in sort_options:
        sort = 'newest'

    item_list = item_list.order_by(sort_options[sort])

    paginator = Paginator(item_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'item/items.html', {
        'items': page_obj,
        'query': query,
        'categories': categories,
        'category_id': (
            int(category_id) if category_id.isdigit() else None
        ),
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    })
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(Category=item.Category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, "item/detail.html",{"item":item , "related_items":  related_items })

@login_required
def new(request):
    if request.method=='POST': #utilisateuer dar submit 
        form=NewItemForm(request.POST,request.FILES) # ghan5do les donner o tswira 
        if form.is_valid(): #ila 7tarmat ga3 les condition
            item=form.save(commit=False)#save walakin machi f data base hitach ba9i ma3ndhach lcreated by 
            item.created_by=request.user#created by= id dluser 
            item.save()#db save f data base 
            return redirect("item:detail",pk=item.id)#afficher l page detail dyal hadi lsawbna
    else:                       
     form=NewItemForm()

    return render(request,'item/form.html',{'form':form,'title': 'New Product',})
@login_required 
@require_POST
def delete(request, pk):
    item = get_object_or_404(
        Item,
        pk=pk,
        created_by=request.user
    )

    item.delete()

    return redirect("dashboard:index")
@login_required
def edit(request, pk):
    item = get_object_or_404(
        Item,
        pk=pk,
        created_by=request.user
    )

    if request.method == 'POST':
        form = EditItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():
            form.save()
            return redirect("item:detail", pk=item.id)

    else:
        form = EditItemForm(instance=item)

    return render(
        request,
        'item/form.html',
        {
            'form': form,
            'item': item,
            'title': 'Edit Product'
        }
    )

