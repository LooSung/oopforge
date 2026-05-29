package com.oopforge.example.order.application.required;

import com.oopforge.example.order.domain.Order;
import com.oopforge.example.order.domain.OrderId;

import java.util.Optional;

public interface OrderRepository {

    void save(Order order);

    Optional<Order> findById(OrderId id);
}
