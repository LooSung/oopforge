package com.oopforge.example.layered.order.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public final class Order {

    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderLine> lines;
    private OrderStatus status;
    private final List<DomainEvent> events = new ArrayList<>();

    private Order(OrderId id, CustomerId customerId, List<OrderLine> lines, OrderStatus status) {
        this.id = id;
        this.customerId = customerId;
        this.lines = List.copyOf(lines);
        this.status = status;
    }

    public static Order place(OrderId id, CustomerId customerId, List<OrderLine> lines) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(customerId, "customerId");
        Objects.requireNonNull(lines, "lines");
        if (lines.isEmpty()) {
            throw new IllegalArgumentException("order must have at least one line");
        }

        Order order = new Order(id, customerId, lines, OrderStatus.PLACED);
        order.record(new OrderPlaced(id, customerId, order.totalAmount()));
        return order;
    }

    public void cancel() {
        if (status == OrderStatus.CANCELLED) {
            throw new IllegalStateException("order is already cancelled");
        }
        status = OrderStatus.CANCELLED;
    }

    public OrderId id() {
        return id;
    }

    public CustomerId customerId() {
        return customerId;
    }

    public List<OrderLine> lines() {
        return Collections.unmodifiableList(lines);
    }

    public OrderStatus status() {
        return status;
    }

    public long totalAmount() {
        return lines.stream().mapToLong(OrderLine::lineTotal).sum();
    }

    public List<DomainEvent> popEvents() {
        List<DomainEvent> published = List.copyOf(events);
        events.clear();
        return published;
    }

    private void record(DomainEvent event) {
        events.add(event);
    }
}
