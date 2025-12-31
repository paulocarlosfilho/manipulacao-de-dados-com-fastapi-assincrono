import pytest
import uuid

async def test_create_post(client, auth_token):
    title = f"Post de Teste {uuid.uuid4().hex[:8]}"
    new_post = {"title": title, "content": "Conteúdo do teste"}
    response = await client.post("/posts/", json=new_post, headers={"Authorization": f"Bearer {auth_token}"})
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == title
    assert "id" in data

async def test_read_posts(client, auth_token):
    response = await client.get("/posts/", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_read_single_post(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    title = f"Busca {uuid.uuid4().hex[:8]}"
    create_res = await client.post("/posts/", json={"title": title, "content": "Teste"}, headers=headers)
    post_id = create_res.json()["id"]
    
    response = await client.get(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == title

async def test_update_post(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    title_old = f"Antigo {uuid.uuid4().hex[:8]}"
    create_res = await client.post("/posts/", json={"title": title_old, "content": "Antigo"}, headers=headers)
    post_id = create_res.json()["id"]
    
    title_new = f"Novo {uuid.uuid4().hex[:8]}"
    response = await client.put(f"/posts/{post_id}", json={"title": title_new, "content": "Novo"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == title_new

async def test_delete_post(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    title = f"Deletar {uuid.uuid4().hex[:8]}"
    create_res = await client.post("/posts/", json={"title": title, "content": "Deletar"}, headers=headers)
    post_id = create_res.json()["id"]
    
    response = await client.delete(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 204
    
    check = await client.get(f"/posts/{post_id}", headers=headers)
    assert check.status_code == 404
