package com.oopforge.example.order.adapter.web;

import java.util.List;

public record PlaceOrderRequest(String customerId, List<LineRequest> lines) {

    public record LineRequest(String productId, int quantity, long unitPrice) {
    }
}
