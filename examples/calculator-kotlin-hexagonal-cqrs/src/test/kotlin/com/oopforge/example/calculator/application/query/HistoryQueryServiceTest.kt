package com.oopforge.example.calculator.application.query

import com.oopforge.example.calculator.adapter.persistence.CalculationStore
import com.oopforge.example.calculator.adapter.persistence.InMemoryCalculationRepository
import com.oopforge.example.calculator.adapter.persistence.InMemoryHistoryQueryRepository
import com.oopforge.example.calculator.application.command.Calculate
import com.oopforge.example.calculator.application.command.CalculateCommandService
import com.oopforge.example.calculator.domain.Operator
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test

class HistoryQueryServiceTest {

    @Test
    fun listsHistoryMostRecentFirstAfterCommands() {
        val store = CalculationStore()
        val command: Calculate = CalculateCommandService(InMemoryCalculationRepository(store))
        val query: CalculationHistory = HistoryQueryService(InMemoryHistoryQueryRepository(store))

        command.handle(Calculate.CalculateCommand(1.0, Operator.ADD, 2.0))
        command.handle(Calculate.CalculateCommand(5.0, Operator.MULTIPLY, 3.0))

        val history: List<HistorySummary> = query.listRecent(10)

        assertThat(history).hasSize(2)
        assertThat(history[0].result).isEqualTo(15.0)
        assertThat(history[1].result).isEqualTo(3.0)
    }
}
