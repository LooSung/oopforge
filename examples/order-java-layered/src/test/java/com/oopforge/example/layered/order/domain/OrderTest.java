package com.oopforge.example.layered.order.domain;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

class OrderTest {

    @Test
    void place_creates_order_and_emits_event() {
        OrderId id = OrderId.generate();
        CustomerId customerId = new CustomerId("cust-1");
        List<OrderLine> lines = List.of(new OrderLine("p-1", 2, 1000));

        Order order = Order.place(id, customerId, lines);

        assertEquals(OrderStatus.PLACED, order.status());
        assertEquals(2000, order.totalAmount());

        var events = order.popEvents();
        assertEquals(1, events.size());
        assertInstanceOf(OrderPlaced.class, events.get(0));
    }

    @Test
    void place_rejects_empty_lines() {
        assertThrows(IllegalArgumentException.class, () ->
                Order.place(OrderId.generate(), new CustomerId("cust-1"), List.of()));
    }
}
