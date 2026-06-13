package com.endeshaw.erp.repository;

import com.endeshaw.erp.model.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRepository extends JpaRepository<Customer, Long> {
}

