"""
Sample tests for Delphi Backend
Run with: pytest
"""
import pytest
from fastapi import status


class TestAuth:
    """Test authentication endpoints"""
    
    def test_create_user(self, client, test_user_data):
        """Test user registration"""
        response = client.post("/users/", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["user_name"] == test_user_data["user_name"]
        assert "password" not in data
    
    def test_login_success(self, client, test_user_data):
        """Test successful login"""
        # Create user first
        client.post("/users/", json=test_user_data)
        
        # Login
        login_data = {
            "username": test_user_data["email"],  # OAuth2 uses 'username' field
            "password": test_user_data["password"]
        }
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCourses:
    """Test course endpoints"""
    
    def test_list_courses(self, client):
        """Test listing courses (public endpoint)"""
        response = client.get("/courses/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


class TestHealthCheck:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"


class TestAI:
    """Test AI endpoints"""
    
    def test_ai_status(self, client):
        """Test AI service status endpoint"""
        response = client.get("/ai/status")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "ai_enabled" in data
