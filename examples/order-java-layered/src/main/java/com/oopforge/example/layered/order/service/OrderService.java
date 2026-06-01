package com.oopforge.example.layered.order.service;

import com.oopforge.example.layered.order.domain.CustomerId;
import com.oopforge.example.layered.order.domain.Order;
import com.oopforge.example.layered.order.domain.OrderId;
import com.oopforge.example.layered.order.domain.OrderLine;
import com.oopforge.example.layered.order.repository.OrderRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public OrderId place(PlaceOrderCommand command) {
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

    public record PlaceOrderCommand(String customerId, List<LineCommand> lines) {
    }

    public record LineCommand(String productId, int quantity, long unitPrice) {
    }
}
