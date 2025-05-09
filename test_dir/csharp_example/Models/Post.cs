using System;
using System.Collections.Generic;

namespace BlogApp.Models
{
    public class Post
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Content { get; set; }
        public int AuthorId { get; set; }
        
        public Post(int id, string title, string content, int authorId)
        {
            Id = id;
            Title = title;
            Content = content;
            AuthorId = authorId;
        }
    }
}
