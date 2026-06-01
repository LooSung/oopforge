package com.oopforge.example.layered.order.service;

import com.oopforge.example.layered.order.domain.OrderId;
import com.oopforge.example.layered.order.repository.InMemoryOrderRepository;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotNull;

class OrderServiceTest {

    @Test
    void place_returns_order_id() {
        OrderService service = new OrderService(new InMemoryOrderRepository());
        OrderId orderId = service.place(new OrderService.PlaceOrderCommand(
                "cust-1",
                List.of(new OrderService.LineCommand("p-1", 2, 1000))
        ));
        assertNotNull(orderId);
    }
}
