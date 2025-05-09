using System;
using System.Collections.Generic;
using System.Linq;
using BlogApp.Models;
using BlogApp.Services;

namespace BlogApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Blog Application Demo");
            
            // Initialize services
            var userService = new UserService();
            var postService = new PostService(userService);
            var commentService = new CommentService(userService, postService);
            
            // Create sample data
            CreateSampleData(userService, postService, commentService);
            
            // Display data
            DisplayData(userService, postService, commentService);
        }
        
        static void CreateSampleData(UserService userService, PostService postService, CommentService commentService)
        {
            // Create users
            var alice = userService.CreateUser("alice", "alice@example.com");
            var bob = userService.CreateUser("bob", "bob@example.com");
            var charlie = userService.CreateUser("charlie", "charlie@example.com");
            
            // Create posts
            var post1 = postService.CreatePost("First Post", "This is Alice's first post", alice.Id);
            var post2 = postService.CreatePost("Hello World", "Bob says hello!", bob.Id);
            var post3 = postService.CreatePost("C# Tips", "Tips for C# programming", charlie.Id);
            
            // Create comments
            commentService.CreateComment("Great post!", bob.Id, post1.Id);
            commentService.CreateComment("Thanks Bob!", alice.Id, post1.Id);
            commentService.CreateComment("Useful tips!", alice.Id, post3.Id);
            commentService.CreateComment("I agree with Alice", bob.Id, post3.Id);
        }
        
        static void DisplayData(UserService userService, PostService postService, CommentService commentService)
        {
            Console.WriteLine("\n=== Users ===");
            foreach (var user in userService.GetAllUsers())
            {
                Console.WriteLine($"User: {user.Username} ({user.Email})");
            }
            
            Console.WriteLine("\n=== Posts ===");
            foreach (var post in postService.GetAllPosts())
            {
                var author = userService.GetUser(post.AuthorId);
                Console.WriteLine($"Post: {post.Title} by {author.Username}");
                Console.WriteLine($"  Content: {post.Content}");
                
                var comments = commentService.GetCommentsByPostId(post.Id);
                Console.WriteLine($"  Comments: {comments.Count()}");
                foreach (var comment in comments)
                {
                    var commenter = userService.GetUser(comment.AuthorId);
                    Console.WriteLine($"    - {commenter.Username}: {comment.Content}");
                }
            }
        }
    }
}
