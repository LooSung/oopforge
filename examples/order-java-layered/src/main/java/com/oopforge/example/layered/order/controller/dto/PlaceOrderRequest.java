package com.oopforge.example.layered.order.controller.dto;

import java.util.List;

public record PlaceOrderRequest(String customerId, List<LineRequest> lines) {

    public record LineRequest(String productId, int quantity, long unitPrice) {
    }
}
