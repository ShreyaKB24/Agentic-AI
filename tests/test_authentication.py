def test_student_login_success(client):
    res = client.post("/api/auth/student-login", json={"student_id": "S1001", "pin": "1111"})
    assert res.status_code == 200
    data = res.get_json()
    assert "/portal" in data["redirect"]

def test_student_login_invalid_pin(client):
    res = client.post("/api/auth/student-login", json={"student_id": "S1001", "pin": "wrong_pin"})
    assert res.status_code == 401
    assert "Incorrect" in res.get_json()["error"]

def test_student_login_invalid_id_format(client):
    res = client.post("/api/auth/student-login", json={"student_id": "INVALID", "pin": "1111"})
    assert res.status_code == 400
    assert "Student ID should look like" in res.get_json()["error"]

def test_student_login_nonexistent(client):
    res = client.post("/api/auth/student-login", json={"student_id": "S9999", "pin": "1111"})
    assert res.status_code == 401

def test_admin_login_success(client):
    res = client.post("/api/auth/admin-login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    data = res.get_json()
    assert "/admin" in data["redirect"]

def test_admin_login_wrong_password(client):
    res = client.post("/api/auth/admin-login", json={"username": "admin", "password": "wrongpassword"})
    assert res.status_code == 401

def test_logout(client):
    client.post("/api/auth/student-login", json={"student_id": "S1001", "pin": "1111"})
    res = client.post("/api/auth/logout")
    assert res.status_code == 200
    # Following request to protected endpoint should be unauthorized
    res_portal = client.get("/api/student/profile")
    assert res_portal.status_code == 401

def test_unauthenticated_access_denied(client):
    res = client.get("/api/student/profile")
    assert res.status_code == 401
    res_admin = client.get("/api/admin/audit")
    assert res_admin.status_code == 401

def test_student_cannot_access_admin(client):
    # Log in as student
    client.post("/api/auth/student-login", json={"student_id": "S1001", "pin": "1111"})
    # Attempt to access admin endpoints
    res_admin_page = client.get("/admin")
    assert res_admin_page.status_code == 302 # Redirected away from admin page
    res_admin_api = client.get("/api/admin/audit")
    assert res_admin_api.status_code == 401

