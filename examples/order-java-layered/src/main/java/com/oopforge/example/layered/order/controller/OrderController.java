package com.oopforge.example.layered.order.controller;

import com.oopforge.example.layered.order.controller.dto.OrderResponse;
import com.oopforge.example.layered.order.controller.dto.PlaceOrderRequest;
import com.oopforge.example.layered.order.domain.OrderId;
import com.oopforge.example.layered.order.service.OrderService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Order", description = "Order placement (layered 3-tier)")
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @Operation(summary = "Place a new order")
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse place(@RequestBody PlaceOrderRequest request) {
        OrderService.PlaceOrderCommand command = new OrderService.PlaceOrderCommand(
                request.customerId(),
                request.lines().stream()
                        .map(line -> new OrderService.LineCommand(
                                line.productId(), line.quantity(), line.unitPrice()))
                        .toList()
        );
        OrderId orderId = orderService.place(command);
        return new OrderResponse(orderId.value().toString());
    }
}
