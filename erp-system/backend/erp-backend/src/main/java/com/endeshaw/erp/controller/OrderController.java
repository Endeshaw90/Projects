package com.endeshaw.erp.controller;

import com.endeshaw.erp.model.Order;
import com.endeshaw.erp.repository.OrderRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderRepository repo;

    public OrderController(OrderRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public ResponseEntity<List<Order>> getAllOrders() {
        return ResponseEntity.ok(repo.findAll());
    }

    @PostMapping
    public ResponseEntity<Order> addOrder(@RequestBody Order order) {
        return ResponseEntity.ok(repo.save(order));
    }
}
