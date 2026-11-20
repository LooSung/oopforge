package com.oopforge.example.calculator.application.command

import com.oopforge.example.calculator.adapter.persistence.CalculationStore
import com.oopforge.example.calculator.adapter.persistence.InMemoryCalculationRepository
import com.oopforge.example.calculator.domain.CalculationId
import com.oopforge.example.calculator.domain.Operator
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test

class CalculateCommandServiceTest {

    @Test
    fun returnsIdNotReadModel() {
        val service: Calculate = CalculateCommandService(
            InMemoryCalculationRepository(CalculationStore()),
        )

        val id: CalculationId = service.handle(Calculate.CalculateCommand(10.0, Operator.ADD, 5.0))

        assertThat(id).isNotNull()
        assertThat(id.value).isNotNull()
    }
}
