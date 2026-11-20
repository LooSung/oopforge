package com.oopforge.example.calculator.config

import com.oopforge.example.calculator.adapter.persistence.CalculationStore
import com.oopforge.example.calculator.application.command.Calculate
import com.oopforge.example.calculator.application.command.CalculationRepository
import com.oopforge.example.calculator.application.query.CalculationHistory
import com.oopforge.example.calculator.application.query.HistoryQueryRepository
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class CalculatorConfig {

    @Bean
    fun calculationStore(): CalculationStore = TODO("Implement stage")

    @Bean
    fun calculationRepository(store: CalculationStore): CalculationRepository = TODO("Implement stage")

    @Bean
    fun historyQueryRepository(store: CalculationStore): HistoryQueryRepository = TODO("Implement stage")

    @Bean
    fun calculate(calculationRepository: CalculationRepository): Calculate = TODO("Implement stage")

    @Bean
    fun calculationHistory(historyQueryRepository: HistoryQueryRepository): CalculationHistory =
        TODO("Implement stage")
}
