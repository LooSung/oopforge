package com.oopforge.example.order.adapter.web;

import com.oopforge.example.order.application.provided.PlaceOrder;
import com.oopforge.example.order.domain.OrderId;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final PlaceOrder placeOrder;

    public OrderController(PlaceOrder placeOrder) {
        this.placeOrder = placeOrder;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse place(@RequestBody PlaceOrderRequest request) {
        PlaceOrder.PlaceOrderCommand command = new PlaceOrder.PlaceOrderCommand(
                request.customerId(),
                request.lines().stream()
                        .map(line -> new PlaceOrder.LineCommand(
                                line.productId(), line.quantity(), line.unitPrice()))
                        .toList()
        );
        OrderId orderId = placeOrder.handle(command);
        return new OrderResponse(orderId.value().toString());
    }
}
