from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
import csv
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, 'dashboard.html')

def stocks(request):
    stock = Stock.objects.all()
    form = StockSearchForm(request.POST or None)

    if request.method == 'POST':
        category = form['category'].value()
        stock = Stock.objects.filter(
                                item_name__icontains=form['item_name'].value()
                                )
        if (category != ''):
            stock = stock.filter(category_id=category)
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Stocks.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            for i in stock:
                writer.writerow([i.category, str(i.item_name).upper(), i.quantity])
            return response
    
    context = {
        "form": form,
        "stock": stock,
    }
    return render(request, 'index.html', context)

def detail(request, pk):
    stock = Stock.objects.get(id=pk)
    context = {
        'stock' : stock,
    }
    return render(request, 'detail.html', context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/stocks_list')
    context = {
        "form": form,
    }
    return render(request, "add.html", context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/stocks_list')
    context = {
        'form':form
    }
    return render(request, 'add.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/stocks_list')
    context = {
        'queryset' : queryset,
    }
    return render(request, 'delete.html', context)

def issue_items(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    form = IssueForm(request.POST or None, instance = stock)
    if form.is_valid():
        instance = form.save(commit=False)
        issue_quantity = form.cleaned_data['issue_quantity']
        instance.quantity -= issue_quantity
        instance.save()
        
        #messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        

        return redirect('/stock_detail/'+str(stock.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = IssueForm()

    context = {
        "stock":stock,
        "form": form,
    }
    return render(request, "add.html", context)

def receive_items(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    form = ReceiveForm(request.POST or None)
    if form.is_valid():
        receive = form.save(commit=False)
        receive.stock = stock
        receive.save()
        #messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

        return redirect('/stock_detail/'+str(stock.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = ReceiveForm()

    context = {
        "stock":stock,
        "form": form,
        }
    return render(request, "add.html", context)

def receive_summary(request):
    y = 'attachment; ' + 'filename="Recieved Report (%s).csv"' %(datetime.datetime.now().date())
    form = ReceiveSearchForm(request.POST or None)
    receive = Receive.objects.all()
    if request.method == 'POST':
        stock = form['stock'].value()
        receive = Receive.objects.filter(
                                receive_from__icontains=form['receive_from'].value(),
                                time__range=[
                                                    form['start_date'].value(),
                                                    form['end_date'].value()]
                                )
        if (stock != ''):
            receive = receive.filter(stock_id=stock)
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = str(y)
            writer = csv.writer(response)
            writer.writerow(['STOCK', 'RECEIVE QUANTITY', 'RECEIVE FROM', 'DATE'])
            for i in receive:
                writer.writerow([i.stock, i.receive_quantity, str(i.receive_from).upper(), i.time])
            return response
    context = {
        'receive' : receive,
        "form": form,
    }
    return render(request, 'receive_summary.html', context)

def issue_summary(request):
    y = 'attachment; ' + 'filename="Sales Report (%s).csv"' %(datetime.datetime.now().date())
    form = IssueSearchForm(request.POST or None)
    issue = Issue.objects.all()
    if request.method == 'POST':
        stock = form['stock'].value()
        issue = Issue.objects.filter(
                                issue_to__icontains=form['issue_to'].value(),
                                time__range=[
                                                    form['start_date'].value(),
                                                    form['end_date'].value()]
                                )
        if (stock != ''):
            issue = issue.filter(stock_id=stock)
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = str(y)
            writer = csv.writer(response)
            writer.writerow(['STOCK', 'QUANTITY', 'ISSUE TO', 'DATE'])
            for i in issue:
                writer.writerow([i.stock, i.issue_quantity, str(i.issue_to).upper(), i.time])
            return response
    page = request.GET.get('page', 1)
    issues = issue
    paginator = Paginator(issues, 1)
    try:
        issue = paginator.page(page)
    except PageNotAnInteger:
        issue = paginator.page(1)
    except EmptyPage:
        issue = paginator.page(paginator.num_pages)
    
    context = {
        "form": form,
        "issue": issue,
    }
    
    return render(request, 'issue_summary.html', context)

def signin(request):
    return render(request, 'login.html')