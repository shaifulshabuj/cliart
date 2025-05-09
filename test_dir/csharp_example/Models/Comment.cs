using System;

namespace BlogApp.Models
{
    public class Comment
    {
        public int Id { get; set; }
        public string Content { get; set; }
        public int AuthorId { get; set; }
        public int PostId { get; set; }
        
        public Comment(int id, string content, int authorId, int postId)
        {
            Id = id;
            Content = content;
            AuthorId = authorId;
            PostId = postId;
        }
    }
}
