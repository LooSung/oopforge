package com.oopforge.example.layered.order.repository;

import com.oopforge.example.layered.order.domain.Order;
import com.oopforge.example.layered.order.domain.OrderId;

import java.util.Optional;

public interface OrderRepository {

    void save(Order order);

    Optional<Order> findById(OrderId id);
}
