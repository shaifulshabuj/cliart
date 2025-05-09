#!/usr/bin/env python3
"""
Main application module for the project example.
"""

from services import UserService, PostService, CommentService

def initialize_services():
    """Initialize all services."""
    user_service = UserService()
    post_service = PostService(user_service)
    comment_service = CommentService(user_service, post_service)
    return user_service, post_service, comment_service

def create_sample_data(user_service, post_service, comment_service):
    """Create sample data for testing."""
    # Create users
    alice = user_service.create_user("alice", "alice@example.com")
    bob = user_service.create_user("bob", "bob@example.com")
    charlie = user_service.create_user("charlie", "charlie@example.com")
    
    # Create posts
    post1 = post_service.create_post("First Post", "This is Alice's first post", alice.user_id)
    post2 = post_service.create_post("Hello World", "Bob says hello!", bob.user_id)
    post3 = post_service.create_post("Python Tips", "Tips for Python programming", charlie.user_id)
    
    # Create comments
    comment1 = comment_service.create_comment("Great post!", bob.user_id, post1.post_id)
    comment2 = comment_service.create_comment("Thanks Bob!", alice.user_id, post1.post_id)
    comment3 = comment_service.create_comment("Useful tips!", alice.user_id, post3.post_id)
    comment4 = comment_service.create_comment("I agree with Alice", bob.user_id, post3.post_id)
    
    return {
        "users": [alice, bob, charlie],
        "posts": [post1, post2, post3],
        "comments": [comment1, comment2, comment3, comment4]
    }

def display_data(data):
    """Display the sample data."""
    print("=== Users ===")
    for user in data["users"]:
        print(user)
    
    print("\n=== Posts ===")
    for post in data["posts"]:
        print(post)
        print(f"  Author: {post.author.username}")
        print(f"  Comments: {len(post.comments)}")
    
    print("\n=== Comments ===")
    for comment in data["comments"]:
        print(comment)
        print(f"  On post: {comment.post.title}")
        print(f"  By user: {comment.author.username}")

def main():
    """Main function."""
    user_service, post_service, comment_service = initialize_services()
    data = create_sample_data(user_service, post_service, comment_service)
    display_data(data)
    
    # Example of using the services
    print("\n=== Example Operations ===")
    
    # Get all posts by Alice
    alice = user_service.get_user(1)
    alice_posts = post_service.get_posts_by_user(alice.user_id)
    print(f"Posts by {alice.username}: {len(alice_posts)}")
    
    # Get all comments on Charlie's post
    charlie_post = post_service.get_post(3)
    comments = comment_service.get_comments_by_post(charlie_post.post_id)
    print(f"Comments on '{charlie_post.title}': {len(comments)}")
    for comment in comments:
        print(f"  - {comment.author.username}: {comment.content}")

if __name__ == "__main__":
    main()
