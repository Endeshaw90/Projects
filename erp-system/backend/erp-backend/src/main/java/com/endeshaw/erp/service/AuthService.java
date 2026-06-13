package com.endeshaw.erp.service;

import com.endeshaw.erp.model.User;
import com.endeshaw.erp.repository.UserRepository;
import com.endeshaw.erp.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AuthService {

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    // ✅ Login with username + password
    public String login(String username, String password) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        // ✅ Validate password
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("Invalid credentials");
        }

        // ✅ Collect roles from authorities
        List<String> roles = user.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .toList();

        // ✅ Pass both username and roles
        return jwtUtil.generateToken(user.getUsername(), roles);
    }
}
