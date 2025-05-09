using System;
using System.Collections.Generic;
using System.Linq;
using BlogApp.Models;

namespace BlogApp.Services
{
    public class CommentService
    {
        private Dictionary<int, Comment> _comments = new Dictionary<int, Comment>();
        private int _nextId = 1;
        private readonly UserService _userService;
        private readonly PostService _postService;
        
        public CommentService(UserService userService, PostService postService)
        {
            _userService = userService;
            _postService = postService;
        }
        
        public Comment CreateComment(string content, int authorId, int postId)
        {
            var user = _userService.GetUser(authorId);
            if (user == null)
            {
                throw new ArgumentException($"User with ID {authorId} not found");
            }
            
            var post = _postService.GetPost(postId);
            if (post == null)
            {
                throw new ArgumentException($"Post with ID {postId} not found");
            }
            
            var comment = new Comment(_nextId, content, authorId, postId);
            _comments[_nextId] = comment;
            _nextId++;
            return comment;
        }
        
        public Comment GetComment(int id)
        {
            return _comments.ContainsKey(id) ? _comments[id] : null;
        }
        
        public IEnumerable<Comment> GetAllComments()
        {
            return _comments.Values;
        }
        
        public IEnumerable<Comment> GetCommentsByPostId(int postId)
        {
            return _comments.Values.Where(c => c.PostId == postId);
        }
        
        public IEnumerable<Comment> GetCommentsByAuthorId(int authorId)
        {
            return _comments.Values.Where(c => c.AuthorId == authorId);
        }
    }
}
