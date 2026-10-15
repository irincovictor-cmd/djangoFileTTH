from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm


def employee_list(request):
    q = (request.GET.get("q") or "").strip()
    employees = Employee.objects.select_related("department").all()
    if q:
        employees = employees.filter(
            Q(employee_id__icontains=q)
            | Q(name__icontains=q)
            | Q(email__icontains=q)
            | Q(position__icontains=q)
            | Q(department__name__icontains=q)
        )
    return render(
        request,
        "employee_management/index.html",
        {"employees": employees, "q": q, "count": employees.count()},
    )


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee created successfully.")
            return redirect("employee_list")
    else:
        form = EmployeeForm()
    return render(
        request,
        "employee_management/create.html",
        {"form": form, "title": "Add Employee"},
    )


def employee_detail(request, pk):
    employee = get_object_or_404(Employee.objects.select_related("department"), pk=pk)
    return render(request, "employee_management/detail.html", {"employee": employee})


def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect("employee_detail", pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(
        request,
        "employee_management/edit.html",
        {"form": form, "employee": employee},
    )


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        name = employee.name
        employee.delete()
        messages.success(request, f'Employee "{name}" deleted.')
        return redirect("employee_list")
    return render(request, "employee_management/delete.html", {"employee": employee})
