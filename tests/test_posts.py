from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res=authorized_client.get("/posts/")

    #to convert from list to a model
    def validate(post):
        return schemas.PostOut(**post)
    posts_map=map(validate, res.json())
    posts_list=list(posts_map)



    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

#test for making sure that only authenticated users can retrieve all posts
def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401

#test for making sure that only authenticated users can retrieve one post
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#test for retreieving a post that doesnt exitsts
def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get("/posts/6666666")
    assert res.status_code == 404

#test for retrieving a valid post
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post=schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome title", "contenttt", True),
    ("fav animal", "cat", False),
    ("current show", "dexter", True)
])
#creating a post
def test_create_post(authorized_client, test_user, title,content, published ):
    res= authorized_client.post("/posts/", json={"title":title, "content": content, "published": published })

    created_post=schemas.Post(**res.json())                                                     
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

#testing if piblished is defaulted to true
def test_create_post_default_published_true(authorized_client, test_user):
    res= authorized_client.post("/posts/", json={"title":"arb", "content": "dkdkd" })

    created_post=schemas.Post(**res.json())                                                     
    assert res.status_code == 201
    assert created_post.title == "arb"
    assert created_post.content == "dkdkd"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


#test if wer not logged in
def test_unauthorized_user_create_post(client):
    res= client.post("/posts/", json={"title":"arb", "content": "dkdkd" })
    assert res.status_code == 401



#DELETING POSTS


#testing unauthorized user deleting posts
def test_unaothorized_user_delete_post(client, test_posts):
    res= client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#test valid deletion
def test_delete_post_success(authorized_client, test_posts):
    res= authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

#test deleting non-existing post 
def test_delete_post_non_exist(authorized_client):
    res= authorized_client.delete("/posts/99")# we cannot write {test_posts[99].id} cause it will give uss out of range error
    assert res.status_code == 404


#test the case where the user trying to delete a post that isnt thers
def test_delete_other_user_post(authorized_client, test_posts ):#authorized_client will always be logged in as user one which is test_user and not test_user2
    res= authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


# TESTING UPDATE POST

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "udated title",
        "content": "updated content",
        "id":test_posts[0].id
    }
    res=authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post=schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']



#updating other user post

def test_update_other_user_post(authorized_client,test_posts, test_user,test_user2):
     data = {
        "title": "udated title",
        "content": "updated content",
        "id":test_posts[3].id
    }
     res=authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
     assert res.status_code == 403


def test_unaothorized_user_update_post(client, test_posts):
    res= client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

    
def test_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "udated title",
        "content": "updated content",
        "id":test_posts[3].id
    }
    res= authorized_client.put("/posts/99", json=data)# we cannot write {test_posts[99].id} cause it will give uss out of range error
    assert res.status_code == 404
