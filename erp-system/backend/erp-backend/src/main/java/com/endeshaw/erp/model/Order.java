package com.endeshaw.erp.model;

import jakarta.persistence.*;

@Entity
@Table(name = "orders") // avoid conflict with SQL keyword
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String orderNumber;

    @ManyToOne
    @JoinColumn(name = "customer_id")
    private Customer customer;

    public Order() {}
    public Order(String orderNumber, Customer customer) {
        this.orderNumber = orderNumber;
        this.customer = customer;
    }

    // getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getOrderNumber() { return orderNumber; }
    public void setOrderNumber(String orderNumber) { this.orderNumber = orderNumber; }

    public Customer getCustomer() { return customer; }
    public void setCustomer(Customer customer) { this.customer = customer; }
}

