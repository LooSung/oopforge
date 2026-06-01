package com.oopforge.example.layered.order.domain;

public final class OrderPlaced extends DomainEvent {

    private final OrderId orderId;
    private final CustomerId customerId;
    private final long totalAmount;

    public OrderPlaced(OrderId orderId, CustomerId customerId, long totalAmount) {
        super();
        this.orderId = orderId;
        this.customerId = customerId;
        this.totalAmount = totalAmount;
    }

    public OrderId orderId() {
        return orderId;
    }

    public CustomerId customerId() {
        return customerId;
    }

    public long totalAmount() {
        return totalAmount;
    }
}
