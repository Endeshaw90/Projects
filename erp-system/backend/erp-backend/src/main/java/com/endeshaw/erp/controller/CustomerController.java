package com.endeshaw.erp.controller;

import com.endeshaw.erp.model.Customer;
import com.endeshaw.erp.repository.CustomerRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/customers")
public class CustomerController {

    private final CustomerRepository repo;

    public CustomerController(CustomerRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public ResponseEntity<List<Customer>> getAllCustomers() {
        return ResponseEntity.ok(repo.findAll());
    }

    @PostMapping
    public ResponseEntity<Customer> addCustomer(@RequestBody Customer customer) {
        return ResponseEntity.ok(repo.save(customer));
    }
}

