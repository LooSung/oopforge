package com.oopforge.example.order.domain;

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
        OrderPlaced placed = (OrderPlaced) events.get(0);
        assertEquals(id, placed.orderId());
        assertEquals(2000, placed.totalAmount());
    }

    @Test
    void place_rejects_empty_lines() {
        assertThrows(IllegalArgumentException.class, () ->
                Order.place(OrderId.generate(), new CustomerId("cust-1"), List.of()));
    }

    @Test
    void cancel_changes_status() {
        Order order = Order.place(
                OrderId.generate(),
                new CustomerId("cust-1"),
                List.of(new OrderLine("p-1", 1, 500))
        );
        order.popEvents();

        order.cancel();

        assertEquals(OrderStatus.CANCELLED, order.status());
    }
}
