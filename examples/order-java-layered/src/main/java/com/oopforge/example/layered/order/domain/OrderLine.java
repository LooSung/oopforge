package com.oopforge.example.layered.order.domain;

import java.util.Objects;

public record OrderLine(String productId, int quantity, long unitPrice) {

    public OrderLine {
        Objects.requireNonNull(productId, "productId");
        if (productId.isBlank()) {
            throw new IllegalArgumentException("product id must not be blank");
        }
        if (quantity <= 0) {
            throw new IllegalArgumentException("quantity must be positive");
        }
        if (unitPrice < 0) {
            throw new IllegalArgumentException("unit price must not be negative");
        }
    }

    public long lineTotal() {
        return (long) quantity * unitPrice;
    }
}
