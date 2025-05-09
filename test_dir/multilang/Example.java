package com.example.demo;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Example Java class to test CLIArt
 */
public class Example {
    private String name;
    private int age;
    private List<String> tags;
    
    public Example(String name, int age) {
        this.name = name;
        this.age = age;
        this.tags = new ArrayList<>();
    }
    
    public void addTag(String tag) {
        tags.add(tag);
    }
    
    public List<String> getTags() {
        return tags;
    }
    
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    public String getInfo() {
        return String.format("%s (%d) - Tags: %s", 
            name, 
            age, 
            tags.stream().collect(Collectors.joining(", "))
        );
    }
    
    // Static utility method
    public static Example createDefault() {
        return new Example("Default", 0);
    }
    
    // Inner class example
    public class Tag {
        private String value;
        
        public Tag(String value) {
            this.value = value;
        }
        
        public String getValue() {
            return value;
        }
    }
    
    // Interface example
    public interface Identifiable {
        String getId();
        
        default boolean hasId() {
            return getId() != null && !getId().isEmpty();
        }
    }
    
    // Enum example
    public enum Status {
        ACTIVE,
        INACTIVE,
        PENDING,
        DELETED
    }
    
    public static void main(String[] args) {
        Example example = new Example("John Doe", 30);
        example.addTag("java");
        example.addTag("example");
        
        System.out.println(example.getInfo());
    }
}
