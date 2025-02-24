import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.models.Profile import Base, Profile
from src.main.python.Application import app

# Configuración de base de datos para pruebas
os.environ["DATABASE_URL"] = "mysql+pymysql://root:1234@localhost:3306/profiles_db"
os.environ["DATABASE_POOL_SIZE"] = "5"

# Crear engine y sesión de prueba
engine = create_engine(os.environ["DATABASE_URL"])
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia de la base de datos en FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def clear_profiles():
    """
    Limpia la tabla Profile antes y después de cada test.
    """
    db = TestingSessionLocal()
    db.query(Profile).delete()
    db.commit()
    db.close()
    yield
    db = TestingSessionLocal()
    db.query(Profile).delete()
    db.commit()
    db.close()

def test_get_profile_by_id():
    """
    Prueba para obtener un perfil por ID.
    """
    db = TestingSessionLocal()
    new_profile = Profile(
        keycloak_user_id="test_keycloak_id",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        restricted_foods="None",
        profile_photo="http://example.com/photo.jpg",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    db.close()

    response = client.get(f"/profiles/{new_profile.profile_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["profile_id"] == new_profile.profile_id
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

def test_list_all_profiles():
    """
    Prueba para listar todos los perfiles.
    """
    db = TestingSessionLocal()
    profile1 = Profile(
        keycloak_user_id="test_keycloak_1",
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        phone="1111111111",
        restricted_foods="Nuts",
        profile_photo="http://example.com/alice.jpg",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    profile2 = Profile(
        keycloak_user_id="test_keycloak_2",
        first_name="Bob",
        last_name="Brown",
        email="bob@example.com",
        phone="2222222222",
        restricted_foods="Gluten",
        profile_photo="http://example.com/bob.jpg",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(profile1)
    db.add(profile2)
    db.commit()
    db.refresh(profile1)
    db.refresh(profile2)
    db.close()

    response = client.get("/profiles/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    profile_ids = {p["profile_id"] for p in data}
    assert profile1.profile_id in profile_ids
    assert profile2.profile_id in profile_ids

def test_delete_profile_by_id():
    """
    Prueba para eliminar un perfil por ID.
    """
    db = TestingSessionLocal()
    profile = Profile(
        keycloak_user_id="test_delete_1",
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        phone="5555555555",
        restricted_foods="Dairy",
        profile_photo="http://example.com/jane.jpg",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    db.close()

    # Verificar que el perfil existe antes de eliminarlo
    response = client.get(f"/profiles/{profile.profile_id}")
    assert response.status_code == 200

    # Enviar la solicitud DELETE
    delete_response = client.delete(f"/profiles/{profile.profile_id}")
    assert delete_response.status_code == 204  # "No Content" indica eliminación exitosa

    # Verificar que el perfil ya no existe en la base de datos
    response_after_delete = client.get(f"/profiles/{profile.profile_id}")
    assert response_after_delete.status_code == 404  # "Not Found" indica que ya no está
