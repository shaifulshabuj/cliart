using System;
using System.Collections.Generic;
using System.Linq;
using BlogApp.Models;

namespace BlogApp.Services
{
    public class UserService
    {
        private Dictionary<int, User> _users = new Dictionary<int, User>();
        private int _nextId = 1;
        
        public User CreateUser(string username, string email)
        {
            var user = new User(_nextId, username, email);
            _users[_nextId] = user;
            _nextId++;
            return user;
        }
        
        public User GetUser(int id)
        {
            return _users.ContainsKey(id) ? _users[id] : null;
        }
        
        public IEnumerable<User> GetAllUsers()
        {
            return _users.Values;
        }
    }
}
