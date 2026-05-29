package com.oopforge.example.order.application.provided;

import com.oopforge.example.order.domain.OrderId;

public interface PlaceOrder {

    OrderId handle(PlaceOrderCommand command);

    record PlaceOrderCommand(String customerId, java.util.List<LineCommand> lines) {
    }

    record LineCommand(String productId, int quantity, long unitPrice) {
    }
}
