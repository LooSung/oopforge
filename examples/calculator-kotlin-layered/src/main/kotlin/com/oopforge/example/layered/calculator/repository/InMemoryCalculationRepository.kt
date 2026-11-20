package com.oopforge.example.layered.calculator.repository

import com.oopforge.example.layered.calculator.domain.Calculation
import com.oopforge.example.layered.calculator.domain.CalculationId
import org.springframework.stereotype.Repository
import java.util.concurrent.ConcurrentHashMap

@Repository
class InMemoryCalculationRepository : CalculationRepository {

    private val store = ConcurrentHashMap<CalculationId, Calculation>()

    override fun save(calculation: Calculation) {
        TODO("Implement stage")
    }

    override fun findById(id: CalculationId): Calculation? = TODO("Implement stage")
}
