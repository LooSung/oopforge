package com.oopforge.example.calculator.domain

import org.assertj.core.api.Assertions.assertThat
import org.assertj.core.api.Assertions.assertThatThrownBy
import org.junit.jupiter.api.Test

class CalculationTest {

    @Test
    fun performsAddition() {
        val calculation = Calculation.perform(CalculationId.generate(), 2.0, Operator.ADD, 3.0)

        assertThat(calculation.result).isEqualTo(5.0)

        val events = calculation.popEvents()
        assertThat(events).hasSize(1)
        assertThat(events[0]).isInstanceOf(CalculationPerformed::class.java)
        val event = events[0] as CalculationPerformed
        assertThat(event.calculationId).isEqualTo(calculation.id)
        assertThat(event.result).isEqualTo(5.0)
        assertThat(calculation.popEvents()).isEmpty()
    }

    @Test
    fun divideByZeroThrows() {
        assertThatThrownBy { Calculation.perform(CalculationId.generate(), 1.0, Operator.DIVIDE, 0.0) }
            .isInstanceOf(IllegalArgumentException::class.java)
    }
}
