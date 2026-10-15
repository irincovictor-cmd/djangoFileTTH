from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Department
from .forms import DepartmentForm


def department_list(request):
    q = (request.GET.get("q") or "").strip()
    departments = Department.objects.all()
    if q:
        departments = departments.filter(
            Q(code__icontains=q)
            | Q(name__icontains=q)
            | Q(head__icontains=q)
            | Q(office_location__icontains=q)
        )
    return render(
        request,
        "department_management/index.html",
        {
            "departments": departments,
            "q": q,
            "count": departments.count(),
        },
    )


def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect("department_list")
    else:
        form = DepartmentForm()
    return render(
        request,
        "department_management/create.html",
        {"form": form, "title": "Add Department"},
    )


def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(
        request,
        "department_management/detail.html",
        {"department": department},
    )


def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect("department_detail", pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    return render(
        request,
        "department_management/edit.html",
        {"form": form, "department": department, "title": "Edit Department"},
    )


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        name = department.name
        department.delete()
        messages.success(request, f'Department "{name}" deleted.')
        return redirect("department_list")
    return render(
        request,
        "department_management/delete.html",
        {"department": department},
    )
