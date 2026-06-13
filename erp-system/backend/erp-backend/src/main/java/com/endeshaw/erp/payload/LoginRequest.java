package com.endeshaw.erp.payload;

public class LoginRequest {
    private String username;
    private String password;

    // ✅ No-args constructor (needed for JSON deserialization)
    public LoginRequest() {}

    // ✅ Optional all-args constructor
    public LoginRequest(String username, String password) {
        this.username = username;
        this.password = password;
    }

    // Getters and setters
    public String getUsername() { 
        return username; 
    }
    public void setUsername(String username) { 
        this.username = username; 
    }

    public String getPassword() { 
        return password; 
    }
    public void setPassword(String password) { 
        this.password = password; 
    }
}


