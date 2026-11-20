package com.oopforge.example.layered.calculator.service

import com.oopforge.example.layered.calculator.domain.Operator
import com.oopforge.example.layered.calculator.repository.InMemoryCalculationRepository
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test

class CalculatorServiceTest {

    @Test
    fun calculatesProduct() {
        val service = CalculatorService(InMemoryCalculationRepository())

        val result = service.calculate(CalculatorService.CalculateCommand(6.0, Operator.MULTIPLY, 7.0))

        assertThat(result.result).isEqualTo(42.0)
        assertThat(result.calculationId).isNotNull()
    }
}
