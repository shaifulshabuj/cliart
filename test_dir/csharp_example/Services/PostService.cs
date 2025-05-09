using System;
using System.Collections.Generic;
using System.Linq;
using BlogApp.Models;

namespace BlogApp.Services
{
    public class PostService
    {
        private Dictionary<int, Post> _posts = new Dictionary<int, Post>();
        private int _nextId = 1;
        private readonly UserService _userService;
        
        public PostService(UserService userService)
        {
            _userService = userService;
        }
        
        public Post CreatePost(string title, string content, int authorId)
        {
            var user = _userService.GetUser(authorId);
            if (user == null)
            {
                throw new ArgumentException($"User with ID {authorId} not found");
            }
            
            var post = new Post(_nextId, title, content, authorId);
            _posts[_nextId] = post;
            _nextId++;
            return post;
        }
        
        public Post GetPost(int id)
        {
            return _posts.ContainsKey(id) ? _posts[id] : null;
        }
        
        public IEnumerable<Post> GetAllPosts()
        {
            return _posts.Values;
        }
        
        public IEnumerable<Post> GetPostsByAuthorId(int authorId)
        {
            return _posts.Values.Where(p => p.AuthorId == authorId);
        }
    }
}
