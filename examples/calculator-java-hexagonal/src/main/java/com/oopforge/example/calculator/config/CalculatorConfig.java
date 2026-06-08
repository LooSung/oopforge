package com.oopforge.example.calculator.config;

import com.oopforge.example.calculator.application.provided.Calculate;
import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.application.service.CalculateService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CalculatorConfig {

    @Bean
    Calculate calculate(CalculationRepository calculationRepository) {
        return new CalculateService(calculationRepository);
    }
}
