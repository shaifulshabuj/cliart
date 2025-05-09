// Rust example file

use std::collections::HashMap;

// A struct
pub struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// An enum
pub enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

// A trait
pub trait Summary {
    fn summarize(&self) -> String;
    
    fn default_summary(&self) -> String {
        String::from("(Read more...)")
    }
}

// Implementation of trait for struct
impl Summary for User {
    fn summarize(&self) -> String {
        format!("{} ({})", self.username, self.email)
    }
}

// A function
pub fn create_user(username: String, email: String) -> User {
    User {
        username,
        email,
        sign_in_count: 1,
        active: true,
    }
}

// Main function
fn main() {
    let mut user = create_user(
        String::from("johndoe"),
        String::from("john@example.com"),
    );
    
    let message = Message::Write(String::from("Hello, world!"));
    
    println!("User summary: {}", user.summarize());
}
