package com.endeshaw.erp.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class JwtFilter extends OncePerRequestFilter {

    private final String secretKey = "mySecretKey"; // ✅ use same key as JwtUtil

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String jwt = authHeader.substring(7);

            try {
                Claims claims = Jwts.parser()
                        .setSigningKey(secretKey)
                        .parseClaimsJws(jwt)
                        .getBody();

                String username = claims.getSubject();
                List<String> roles = claims.get("roles", List.class);

                if (username != null && roles != null) {
                    var authorities = roles.stream()
                            .map(role -> new SimpleGrantedAuthority("ROLE_" + role))
                            .collect(Collectors.toList());

                    UsernamePasswordAuthenticationToken auth =
                            new UsernamePasswordAuthenticationToken(username, null, authorities);

                    SecurityContextHolder.getContext().setAuthentication(auth);
                }
            } catch (Exception e) {
                // Invalid token → clear context
                SecurityContextHolder.clearContext();
            }
        }

        filterChain.doFilter(request, response);
    }
}
