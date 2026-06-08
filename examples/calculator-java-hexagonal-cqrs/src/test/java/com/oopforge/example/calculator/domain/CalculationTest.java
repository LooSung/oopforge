package com.oopforge.example.calculator.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class CalculationTest {

    @Test
    void performsAddition() {
        Calculation calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3);

        assertThat(calculation.result()).isEqualTo(5.0);
        assertThat(calculation.performedAt()).isNotNull();

        List<DomainEvent> events = calculation.popEvents();
        assertThat(events).hasSize(1);
        assertThat(events.get(0)).isInstanceOf(CalculationPerformed.class);
        assertThat(((CalculationPerformed) events.get(0)).result()).isEqualTo(5.0);
    }

    @Test
    void divideByZeroThrows() {
        assertThatThrownBy(() -> Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
