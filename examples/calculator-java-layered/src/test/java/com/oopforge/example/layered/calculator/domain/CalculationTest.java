package com.oopforge.example.layered.calculator.domain;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class CalculationTest {

    @Test
    void performsAddition() {
        Calculation calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3);

        assertThat(calculation.result()).isEqualTo(5.0);
    }

    @Test
    void divideByZeroThrows() {
        assertThatThrownBy(() -> Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
