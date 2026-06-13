package com.endeshaw.erp.repository;

import com.endeshaw.erp.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // Custom query to find user by username
    Optional<User> findByUsername(String username);
}
