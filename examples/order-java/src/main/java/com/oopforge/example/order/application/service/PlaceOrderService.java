package com.oopforge.example.order.application.service;

import com.oopforge.example.order.application.provided.PlaceOrder;
import com.oopforge.example.order.application.required.OrderRepository;
import com.oopforge.example.order.domain.CustomerId;
import com.oopforge.example.order.domain.Order;
import com.oopforge.example.order.domain.OrderId;
import com.oopforge.example.order.domain.OrderLine;

import java.util.List;

public class PlaceOrderService implements PlaceOrder {

    private final OrderRepository orderRepository;

    public PlaceOrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Override
    public OrderId handle(PlaceOrderCommand command) {
        OrderId orderId = OrderId.generate();
        CustomerId customerId = new CustomerId(command.customerId());
        List<OrderLine> lines = command.lines().stream()
                .map(line -> new OrderLine(line.productId(), line.quantity(), line.unitPrice()))
                .toList();

        Order order = Order.place(orderId, customerId, lines);
        orderRepository.save(order);
        order.popEvents();
        return orderId;
    }
}
