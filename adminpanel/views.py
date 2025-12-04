from datetime import datetime
import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_BASE = "http://127.0.0.1:8000/api"

# ---------------------------------------
# LOGIN DO ADMIN (usando API LOGIN REAL)
# ---------------------------------------
def panel_login(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']

        # 🔥 ROTA CERTA (AppLoginView)
        response = requests.post(
            "http://127.0.0.1:8000/api/login/",
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            # salva o token corretamente
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
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    # ----- Usuários -----
    try:
        users = requests.get(f"{API_BASE}/users/", headers=headers).json()
    except:
        users = []

    # ----- Água -----
    try:
        water_logs = requests.get(f"{API_BASE}/water/logs/", headers=headers).json()
    except:
        water_logs = []

    water_by_day = {}
    for w in water_logs:
        day = w.get("date", "Sem data")
        water_by_day[day] = water_by_day.get(day, 0) + w.get("amount_ml", 0)

    chart_water = {
        "labels": list(water_by_day.keys()),
        "values": list(water_by_day.values()),
    }

    # ----- Exercício -----
    try:
        ex_logs = requests.get(f"{API_BASE}/exercise/logs/", headers=headers).json()
    except:
        ex_logs = []

    ex_by_day = {}
    for e in ex_logs:
        day = e.get("date", "Sem data")
        ex_by_day[day] = ex_by_day.get(day, 0) + e.get("duration_min", 0)

    chart_exercise = {
        "labels": list(ex_by_day.keys()),
        "values": list(ex_by_day.values()),
    }

    # ----- Hábitos -----
    try:
        habits = requests.get(f"{API_BASE}/habits/", headers=headers).json()
    except:
        habits = []

    # ----- Conquistas -----
    try:
        achievements = requests.get(f"{API_BASE}/achievements/", headers=headers).json()
    except:
        achievements = []

    context = {
        "total_users": len(users),
        "total_habits": len(habits),
        "total_achievements": len(achievements),
        "chart_water": chart_water,
        "chart_exercise": chart_exercise,
        "chart_users": {
            "labels": ["Ativos"],
            "values": [len(users)]
        }
    }

    return render(request, "adminpanel/dashboard.html", context)



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
        request.session.flush()
        return redirect('panel_login')
    
    users = response.json()

    context={
        "total_users": len(users),
        "users": users
    }

    return render(request, 'adminpanel/users.html', context)


# ---------------------------------------
# DETALHES DO USUÁRIO
# ---------------------------------------
def user_details(request, user_id):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    # Buscar dados do usuário
    user_resp = requests.get(f"{API_BASE}/users/{user_id}/", headers=headers)
    if user_resp.status_code != 200:
        messages.error(request, "Erro ao buscar dados do usuário.")
        return redirect("users_page")

    user_data = user_resp.json()

    # Buscar estatísticas
    stats_resp = requests.get(f"{API_BASE}/users/{user_id}/stats/", headers=headers)
    stats_data = stats_resp.json() if stats_resp.status_code == 200 else None

    return render(request, "adminpanel/user_details.html", {
        "user": user_data,
        "stats": stats_data,
    })


# ---------------------------------------
# EDITAR USUÁRIO
# ---------------------------------------
def user_edit(request, user_id):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_BASE}/users/{user_id}/", headers=headers)
    if resp.status_code != 200:
        messages.error(request, "Usuário não encontrado")
        return redirect("users_page")

    user = resp.json()

    if request.method == "POST":
        update_resp = requests.put(
            f"{API_BASE}/users/{user_id}/",
            headers=headers,
            json={
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
            }
        )

        if update_resp.status_code in (200, 204):
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("users_page")
        else:
            messages.error(request, "Erro ao atualizar usuário")

    return render(request, "adminpanel/user_edit.html", {"user": user})


# ---------------------------------------
# DELETAR USUÁRIO
# ---------------------------------------
def user_delete(request, user_id):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{API_BASE}/users/{user_id}/", headers=headers)

    if resp.status_code in (200, 204):
        messages.success(request, "Usuário excluído com sucesso!")
    else:
        messages.error(request, "Erro ao excluir usuário.")

    return redirect("users_page")


# ---------------------------------------
# CRUD - HÁBITOS
# ---------------------------------------
def habits_list(request):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_BASE}/habits/", headers=headers)
    habits = resp.json() if resp.status_code == 200 else []

    return render(request, "adminpanel/habits_list.html", {"habits": habits, })


def habit_create(request):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        payload = {
            "title": request.POST["name"],
            "description": request.POST["description"],
            "user": request.POST["user_id"],
        }

        requests.post(f"{API_BASE}/habits/", json=payload, headers=headers)
        return redirect("habits_list")

    try:
        response = requests.get(f"{API_BASE}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
        else:
            users = []
    except:
        users = []

    return render(request, "adminpanel/habit_form.html", {"habit": None, 'users': users})


def habit_edit(request, habit_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_BASE}/habits/{habit_id}/", headers=headers)
    if resp.status_code != 200:
        return redirect("habits_list")

    habit = resp.json()

    if request.method == "POST":
        payload = {
            "title": request.POST["name"],
            "description": request.POST["description"],
        }

        requests.put(f"{API_BASE}/habits/{habit_id}/", json=payload, headers=headers)
        return redirect("habits_list")

    return render(request, "adminpanel/habit_form.html", {"habit": habit})


def habit_delete(request, habit_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    requests.delete(f"{API_BASE}/habits/{habit_id}/", headers=headers)
    return redirect("habits_list")


# ---------------------------------------
# LOGOUT
# ---------------------------------------
def logout_view(request):
    request.session.flush()
    return redirect("panel_login")


# ---------------------------------------
# CRUD - CONQUISTAS
# ---------------------------------------

def achievements_list(request):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_BASE}/achievements/", headers=headers)
    achievements = resp.json() if resp.status_code == 200 else []

    return render(request, "adminpanel/achievements_list.html", {
        "achievements": achievements
    })


def achievement_create(request):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    if request.method == "POST":
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "code": request.POST["code"],
            "title": request.POST["title"],
            "description": request.POST["description"],
            "icon": request.POST["icon"],
            "color": request.POST["color"],
            "goal": request.POST["goal"],
        }

        requests.post(f"{API_BASE}/achievements/", json=payload, headers=headers)
        return redirect("achievements_list")

    return render(request, "adminpanel/achievement_form.html", {"achievement": None})


def achievement_edit(request, ach_id):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_BASE}/achievements/{ach_id}/", headers=headers)
    if resp.status_code != 200:
        return redirect("achievements_list")

    achievement = resp.json()

    if request.method == "POST":
        payload = {
            "code": request.POST["code"],
            "title": request.POST["title"],
            "description": request.POST["description"],
            "icon": request.POST["icon"],
            "color": request.POST["color"],
            "goal": request.POST["goal"],
        }

        requests.put(f"{API_BASE}/achievements/{ach_id}/", json=payload, headers=headers)
        return redirect("achievements_list")

    return render(request, "adminpanel/achievement_form.html", {
        "achievement": achievement
    })


def achievement_delete(request, ach_id):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")

    headers = {"Authorization": f"Bearer {token}"}

    requests.delete(f"{API_BASE}/achievements/{ach_id}/", headers=headers)

    return redirect("achievements_list")

# ---------------------------------------
# CRUD - WATER
# ---------------------------------------
def water_create(request):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")
    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        date_str = request.POST.get("datetime")
        dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        timestamp_ms = int(dt_obj.timestamp() * 1000)

        payload = {
            "user": request.POST["user_id"],
            "amount_ml": request.POST["amount_ml"],
            "timestamp_ms": timestamp_ms
        }
        
        requests.post(f"{API_BASE}/water/logs/", json=payload, headers=headers)
        return redirect("water_list")

    try:
        response = requests.get(f"{API_BASE}/users/", headers=headers)
        users = response.json() if response.status_code == 200 else []
    except:
        users = []

    default_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    
    return render(request, "adminpanel/water_form.html", {
        "water": None, 
        "users": users,
        "formatted_date": default_date
    })

def water_list(request):
    token = request.session.get("token")
    if not token:
        return redirect("panel_login")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{API_BASE}/water/logs/", headers=headers)
    if response.status_code == 200:
        water_logs = response.json()
    else:
        water_logs = []

    total_ml = sum(item.get('amount_ml', 0) for item in water_logs)
    
    total_liters = total_ml / 1000
    total_records = len(water_logs)

    context = {
        "water_logs": water_logs,
        "total_liters": total_liters,
        "total_records": total_records
    }

    return render(request, "adminpanel/water_list.html", context)

def water_edit(request, log_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_BASE}/water/logs/{log_id}/", headers=headers)
    if resp.status_code != 200:
        return redirect("water_list")

    log = resp.json()

    if request.method == "POST":
        payload = {
            "user": request.POST["user"],
            "amount_ml": request.POST["amount_ml"],
            "timestamp_ms": request.POST["timestamp_ms"]
        }
        requests.put(f"{API_BASE}/water/logs/{log_id}/", json=payload, headers=headers)
        return redirect("water_list")

    return render(request, "adminpanel/water_form.html", {"water": log})


def water_delete(request, log_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(f"{API_BASE}/water/logs/{log_id}/", headers=headers)
    return redirect("water_list")

# ---------------------------------------
# CRUD - EXERCISE
# ---------------------------------------
def exercise_list(request):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_BASE}/exercise/logs/", headers=headers)
    logs = resp.json() if resp.status_code == 200 else []
    return render(request, "adminpanel/exercise_list.html", {"logs": logs})


def exercise_edit(request, log_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_BASE}/exercise/logs/{log_id}/", headers=headers)
    if resp.status_code != 200:
        return redirect("exercise_list")

    log = resp.json()

    if request.method == "POST":
        payload = {
            "user": request.POST["user"],
            "type": request.POST["type"],
            "intensity": request.POST["intensity"],
            "duration_min": request.POST["duration_min"],
            "timestamp_ms": request.POST["timestamp_ms"]
        }
        requests.put(f"{API_BASE}/exercise/logs/{log_id}/", json=payload, headers=headers)
        return redirect("exercise_list")

    return render(request, "adminpanel/exercise_form.html", {"log": log})

def exercise_delete(request, log_id):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(f"{API_BASE}/exercise/logs/{log_id}/", headers=headers)
    return redirect("exercise_list")