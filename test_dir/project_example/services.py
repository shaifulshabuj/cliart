#!/usr/bin/env python3
"""
Services module for the project example.
"""

from models import User, Post, Comment

class UserService:
    """Service for user-related operations."""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, username, email):
        """Create a new user."""
        user = User(self.next_id, username, email)
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def get_user(self, user_id):
        """Get a user by ID."""
        return self.users.get(user_id)
    
    def get_all_users(self):
        """Get all users."""
        return list(self.users.values())


class PostService:
    """Service for post-related operations."""
    
    def __init__(self, user_service):
        self.posts = {}
        self.next_id = 1
        self.user_service = user_service
    
    def create_post(self, title, content, author_id):
        """Create a new post."""
        author = self.user_service.get_user(author_id)
        if not author:
            raise ValueError(f"User with ID {author_id} not found")
        
        post = Post(self.next_id, title, content, author)
        self.posts[self.next_id] = post
        author.add_post(post)
        self.next_id += 1
        return post
    
    def get_post(self, post_id):
        """Get a post by ID."""
        return self.posts.get(post_id)
    
    def get_all_posts(self):
        """Get all posts."""
        return list(self.posts.values())
    
    def get_posts_by_user(self, user_id):
        """Get all posts by a specific user."""
        user = self.user_service.get_user(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user.get_posts()


class CommentService:
    """Service for comment-related operations."""
    
    def __init__(self, user_service, post_service):
        self.comments = {}
        self.next_id = 1
        self.user_service = user_service
        self.post_service = post_service
    
    def create_comment(self, content, author_id, post_id):
        """Create a new comment."""
        author = self.user_service.get_user(author_id)
        if not author:
            raise ValueError(f"User with ID {author_id} not found")
        
        post = self.post_service.get_post(post_id)
        if not post:
            raise ValueError(f"Post with ID {post_id} not found")
        
        comment = Comment(self.next_id, content, author, post)
        self.comments[self.next_id] = comment
        post.add_comment(comment)
        self.next_id += 1
        return comment
    
    def get_comment(self, comment_id):
        """Get a comment by ID."""
        return self.comments.get(comment_id)
    
    def get_all_comments(self):
        """Get all comments."""
        return list(self.comments.values())
    
    def get_comments_by_post(self, post_id):
        """Get all comments on a specific post."""
        post = self.post_service.get_post(post_id)
        if not post:
            raise ValueError(f"Post with ID {post_id} not found")
        return post.get_comments()
