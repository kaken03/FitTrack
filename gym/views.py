from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, Plan
from django.db.models import Sum

def home(request):
    query = request.GET.get('q')
    if query:
        members = Member.objects.filter(name__icontains=query) | Member.objects.filter(email__icontains=query)
    else:
        members = Member.objects.all()

    # Dashboard Statistics
    total_members = members.count()
    # Sum the price of the plan associated with each member
    total_revenue = members.aggregate(Sum('plan__price'))['plan__price__sum'] or 0

    context = {
        'members': members,
        'query': query,
        'total_members': total_members,
        'total_revenue': total_revenue,
    }
    return render(request, 'gym/home.html', context)

def add_member(request):
    plans = Plan.objects.all() # Get all plans for the dropdown
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
            expiry_date=expiry_date
        )
        return redirect('home')
    return render(request, 'gym/add_member.html', {'plans': plans})

def edit_member(request, id):
    member = Member.objects.get(id=id)
    if request.method == 'POST':
        member.name = request.POST['name']
        member.email = request.POST['email']
        member.plan = request.POST['plan']
        member.start_date = request.POST['start_date']
        member.expiry_date = request.POST['expiry_date']
        member.save()
        return redirect('home')
    return render(request, 'gym/edit_member.html', {'member': member})

def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    
    if request.method == 'POST':
        member.delete()
        return redirect('home')
        
    return render(request, 'gym/delete_member.html', {'member': member})