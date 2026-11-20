package com.oopforge.example.calculator.application.required

import com.oopforge.example.calculator.domain.Calculation
import com.oopforge.example.calculator.domain.CalculationId

interface CalculationRepository {

    fun save(calculation: Calculation)

    fun findById(id: CalculationId): Calculation?
}
