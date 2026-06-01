package com.oopforge.example.layered.order.domain;

import java.util.Objects;

public record CustomerId(String value) {

    public CustomerId {
        Objects.requireNonNull(value, "value");
        if (value.isBlank()) {
            throw new IllegalArgumentException("customer id must not be blank");
        }
    }
}
