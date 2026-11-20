package com.oopforge.example.calculator.config

import com.oopforge.example.calculator.adapter.persistence.CalculationStore
import com.oopforge.example.calculator.adapter.persistence.InMemoryCalculationRepository
import com.oopforge.example.calculator.adapter.persistence.InMemoryHistoryQueryRepository
import com.oopforge.example.calculator.application.command.Calculate
import com.oopforge.example.calculator.application.command.CalculateCommandService
import com.oopforge.example.calculator.application.command.CalculationRepository
import com.oopforge.example.calculator.application.query.CalculationHistory
import com.oopforge.example.calculator.application.query.HistoryQueryRepository
import com.oopforge.example.calculator.application.query.HistoryQueryService
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class CalculatorConfig {

    @Bean
    fun calculationStore(): CalculationStore = CalculationStore()

    @Bean
    fun calculationRepository(store: CalculationStore): CalculationRepository = InMemoryCalculationRepository(store)

    @Bean
    fun historyQueryRepository(store: CalculationStore): HistoryQueryRepository =
        InMemoryHistoryQueryRepository(store)

    @Bean
    fun calculate(calculationRepository: CalculationRepository): Calculate =
        CalculateCommandService(calculationRepository)

    @Bean
    fun calculationHistory(historyQueryRepository: HistoryQueryRepository): CalculationHistory =
        HistoryQueryService(historyQueryRepository)
}
