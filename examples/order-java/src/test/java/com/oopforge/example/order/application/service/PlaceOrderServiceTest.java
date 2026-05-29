package com.oopforge.example.order.application.service;

import com.oopforge.example.order.adapter.persistence.InMemoryOrderRepository;
import com.oopforge.example.order.application.provided.PlaceOrder;
import com.oopforge.example.order.domain.OrderId;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotNull;

class PlaceOrderServiceTest {

    @Test
    void handle_persists_order() {
        PlaceOrder placeOrder = new PlaceOrderService(new InMemoryOrderRepository());
        PlaceOrder.PlaceOrderCommand command = new PlaceOrder.PlaceOrderCommand(
                "cust-1",
                List.of(new PlaceOrder.LineCommand("p-1", 1, 900))
        );

        OrderId orderId = placeOrder.handle(command);

        assertNotNull(orderId);
    }
}
