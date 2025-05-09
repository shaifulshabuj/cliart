#!/usr/bin/env python3
"""
Models module for the project example.
"""

class User:
    """User model class."""
    
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.posts = []
    
    def add_post(self, post):
        """Add a post to the user's posts."""
        self.posts.append(post)
        return post
    
    def get_posts(self):
        """Get all posts by the user."""
        return self.posts
    
    def __str__(self):
        return f"User(id={self.user_id}, username={self.username})"


class Post:
    """Post model class."""
    
    def __init__(self, post_id, title, content, author):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.comments = []
    
    def add_comment(self, comment):
        """Add a comment to the post."""
        self.comments.append(comment)
        return comment
    
    def get_comments(self):
        """Get all comments on the post."""
        return self.comments
    
    def __str__(self):
        return f"Post(id={self.post_id}, title={self.title})"


class Comment:
    """Comment model class."""
    
    def __init__(self, comment_id, content, author, post):
        self.comment_id = comment_id
        self.content = content
        self.author = author
        self.post = post
    
    def __str__(self):
        return f"Comment(id={self.comment_id}, author={self.author.username})"
