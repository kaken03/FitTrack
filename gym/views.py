from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, Plan
from django.db.models import Sum
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    from django.utils import timezone
    
    query = request.GET.get('q')
    status_filter = request.GET.get('status')  # Get status filter (all, active, expired)
    
    if query:
        members = Member.objects.filter(owner=request.user, name__icontains=query) | Member.objects.filter(owner=request.user, email__icontains=query)
    else:
        members = Member.objects.filter(owner=request.user)

    # Filter by status if provided (using expiry_date since status is a property)
    today = timezone.now().date()
    if status_filter == 'active':
        members = [m for m in members if m.expiry_date >= today]
    elif status_filter == 'expired':
        members = [m for m in members if m.expiry_date < today]

    # Dashboard Statistics (count only current user's members)
    all_members = Member.objects.filter(owner=request.user)
    total_members = all_members.count()
    total_active = sum(1 for m in all_members if m.expiry_date >= today)
    total_expired = sum(1 for m in all_members if m.expiry_date < today)
    # Sum the price of the plan associated with each member
    total_revenue = all_members.aggregate(Sum('plan__price'))['plan__price__sum'] or 0
    plans = Plan.objects.filter(owner=request.user)

    context = {
        'members': members,
        'query': query,
        'status_filter': status_filter,
        'total_members': total_members,
        'total_active': total_active,
        'total_expired': total_expired,
        'total_revenue': total_revenue,
        'plans': plans,
    }
    return render(request, 'gym/home.html', context)

@login_required
def add_member(request):
    plans = Plan.objects.filter(owner=request.user)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        plan_id = request.POST['plan']
        start_date = request.POST['start_date']
        expiry_date = request.POST['expiry_date']
        
        selected_plan = Plan.objects.get(id=plan_id)
        
        Member.objects.create(
            name=name, 
            email=email, 
            plan=selected_plan, 
            start_date=start_date, 
            expiry_date=expiry_date,
            owner=request.user
        )
        return redirect('home')
    return render(request, 'gym/add_member.html', {'plans': plans})

@login_required
def edit_member(request, id):
    member = get_object_or_404(Member, id=id, owner=request.user)
    plans = Plan.objects.filter(owner=request.user)
    if request.method == 'POST':
        member.name = request.POST['name']
        member.email = request.POST['email']
        plan_id = request.POST['plan']
        member.plan = Plan.objects.get(id=plan_id)
        member.start_date = request.POST['start_date']
        member.expiry_date = request.POST['expiry_date']
        member.save()
        return redirect('home')
    return render(request, 'gym/edit_member.html', {'member': member, 'plans': plans})

@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id, owner=request.user)
    
    if request.method == 'POST':
        member.delete()
        return redirect('home')
        
    return render(request, 'gym/delete_member.html', {'member': member})


@login_required
def add_plan(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        duration = request.POST.get('duration_months')
        Plan.objects.create(
            name=name,
            description=description,
            price=price,
            duration_months=int(duration or 1),
            owner=request.user
        )
        return redirect('home')
    return redirect('home')


@login_required
def edit_plan(request, id):
    plan = get_object_or_404(Plan, id=id, owner=request.user)
    if request.method == 'POST':
        plan.name = request.POST.get('name')
        plan.description = request.POST.get('description', '')
        plan.price = request.POST.get('price')
        plan.duration_months = int(request.POST.get('duration_months') or 1)
        plan.save()
        return redirect('home')
    return redirect('home')


@login_required
def delete_plan(request, id):
    plan = get_object_or_404(Plan, id=id, owner=request.user)
    if request.method == 'POST':
        plan.delete()
        return redirect('home')
    return redirect('home')


def login_view(request):
    """Simple username/password login view."""
    # Redirect already-logged-in users to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'gym/login.html', {'error': 'Invalid credentials'})
    return render(request, 'gym/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')