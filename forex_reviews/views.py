from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg

from .models import Company, Review
from .forms import ReviewForm, CompanyForm


def main_page(request):
    companies = Company.objects.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = Company(name=form.cleaned_data['name'],description=form.cleaned_data['description'],slug=form.cleaned_data['slug'])
            company.save()
            return redirect('main_page')
    else:
        form = CompanyForm()

    context = {'companies': companies,'form':form}
    return render(request, 'forex_reviews/main_page.html', context)

def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = CompanyForm()

    context = {'form': form}
    return render(request, 'forex_reviews/add_company.html', context)


def company_page(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    reviews = Review.objects.filter(company=company)

    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(company=company, text=form.cleaned_data['text'], rating=form.cleaned_data['rating'], username=form.cleaned_data['username'])
            review.save()
            return redirect('company_page', company_slug=company.slug)
    else:
        form = ReviewForm()

    context = {'company': company, 'reviews': reviews, 'form': form}
    return render(request, 'forex_reviews/company_page.html', context)
