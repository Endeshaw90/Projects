package com.endeshaw.erp.repository;

import com.endeshaw.erp.model.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long> {
}

