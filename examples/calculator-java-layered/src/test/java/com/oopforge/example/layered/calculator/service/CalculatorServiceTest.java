package com.oopforge.example.layered.calculator.service;

import com.oopforge.example.layered.calculator.domain.Operator;
import com.oopforge.example.layered.calculator.repository.InMemoryCalculationRepository;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class CalculatorServiceTest {

    @Test
    void calculatesProduct() {
        CalculatorService service = new CalculatorService(new InMemoryCalculationRepository());

        CalculatorService.CalculationResult result =
                service.calculate(new CalculatorService.CalculateCommand(6, Operator.MULTIPLY, 7));

        assertThat(result.result()).isEqualTo(42.0);
        assertThat(result.calculationId()).isNotNull();
    }
}
