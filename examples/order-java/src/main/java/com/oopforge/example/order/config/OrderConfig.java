package com.oopforge.example.order.config;

import com.oopforge.example.order.application.provided.PlaceOrder;
import com.oopforge.example.order.application.required.OrderRepository;
import com.oopforge.example.order.application.service.PlaceOrderService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OrderConfig {

    @Bean
    PlaceOrder placeOrder(OrderRepository orderRepository) {
        return new PlaceOrderService(orderRepository);
    }
}
