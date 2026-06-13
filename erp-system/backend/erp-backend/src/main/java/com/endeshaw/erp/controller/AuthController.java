package com.endeshaw.erp.controller;

import com.endeshaw.erp.payload.LoginRequest;
import com.endeshaw.erp.payload.JwtResponse;
import com.endeshaw.erp.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;

    @Autowired
    public AuthController(AuthenticationManager authenticationManager, JwtUtil jwtUtil) {
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/login")
    public JwtResponse authenticateUser(@RequestBody LoginRequest loginRequest) {
        // ✅ Authenticate user credentials
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        loginRequest.getUsername(),
                        loginRequest.getPassword()
                )
        );

        // ✅ Extract roles from authentication
        List<String> roles = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .map(auth -> auth.replace("ROLE_", "")) // store clean role names
                .collect(Collectors.toList());

        // ✅ Generate JWT token with roles
        String jwt = jwtUtil.generateToken(authentication.getName(), roles);

        // ✅ Return token in JSON response
        return new JwtResponse(jwt);
    }
}
