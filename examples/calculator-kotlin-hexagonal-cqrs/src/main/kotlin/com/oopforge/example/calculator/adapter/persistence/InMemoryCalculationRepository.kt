package com.oopforge.example.calculator.adapter.persistence

import com.oopforge.example.calculator.application.command.CalculationRepository
import com.oopforge.example.calculator.domain.Calculation

/**
 * Write adapter: persists the aggregate and projects the read model.
 */
class InMemoryCalculationRepository(private val store: CalculationStore) : CalculationRepository {

    override fun save(calculation: Calculation) {
        TODO("Implement stage")
    }
}
