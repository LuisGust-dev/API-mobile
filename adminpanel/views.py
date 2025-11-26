import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_BASE = "http://127.0.0.1:8000/api"

# ---------------------------------------
# LOGIN DO ADMIN (usando JWT padrão)
# ---------------------------------------
def panel_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post(
            f"{API_BASE}/auth/login/",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            request.session['token'] = data['access']
            return redirect('dashboard')
        else:
            messages.error(request, "Login inválido.")

    return render(request, 'adminpanel/login.html')


# ---------------------------------------
# DASHBOARD
# ---------------------------------------
def dashboard(request):
    token = request.session.get("token")

    if not token:
        return redirect('panel_login')

    headers = {"Authorization": f"Bearer {token}"}
    users = requests.get(f"{API_BASE}/users/", headers=headers).json()

    context = {
        "total_users": len(users),
    }

    return render(request, 'adminpanel/dashboard.html', context)


# ---------------------------------------
# LISTAGEM DE USUÁRIOS
# ---------------------------------------
def users_page(request):
    token = request.session.get("token")
    if not token:
        return redirect('panel_login')

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/users/", headers=headers)

    if response.status_code == 401:
        # Token expirado → desloga
        request.session.flush()
        return redirect('panel_login')

    users = response.json()
    return render(request, 'adminpanel/users.html', {"users": users})

def user_details(request, user_id):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{API_BASE}/users/{user_id}/stats/", headers=headers)

    data = response.json()

    return render(request, "adminpanel/user_details.html", {"data": data})

