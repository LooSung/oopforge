package com.oopforge.example.calculator.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class CalculationTest {

    @Test
    void performsAddition() {
        Calculation calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3);

        assertThat(calculation.result()).isEqualTo(5.0);
        assertThat(calculation.performedAt()).isNotNull();
    }

    @Test
    void divideByZeroThrows() {
        assertThatThrownBy(() -> Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
