package com.oopforge.example.layered.calculator.repository

import com.oopforge.example.layered.calculator.domain.Calculation
import com.oopforge.example.layered.calculator.domain.CalculationId

interface CalculationRepository {

    fun save(calculation: Calculation)

    fun findById(id: CalculationId): Calculation?
}
