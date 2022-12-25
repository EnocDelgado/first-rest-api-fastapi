from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

# Create a array where we'll store our list of models
posts = []

# Post Model
class PostModel(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


@app.get('/')
def read_root():
    return {"welcome": "Welcome to my RESTful API"}


@app.get('/posts')
def read_posts():
    return posts

@app.post('/posts')
def save_post(post:PostModel):
    # Assign id
    post.id = str(uuid())

    # Convert our post to a json dict
    posts.append(post.dict())
    return post[-1]

@app.get('/posts/{post_id}')
def get_post(post_id:str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post no found")

@app.delete('/posts/{post_id}')
def delete_post(post_id:str):
    for index, post in  enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Post no found")


@app.put('/posts/{post_id}')
def update_post(post_id:str, update_post:PostModel):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = update_post.title
            posts[index]["author"] = update_post.author
            posts[index]["content"] = update_post.content
            return {"message": "Post has been updated successfully"}
    raise HTTPException(status_code=404, detail="Post no found")