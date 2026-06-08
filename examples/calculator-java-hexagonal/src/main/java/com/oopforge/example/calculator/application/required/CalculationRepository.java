package com.oopforge.example.calculator.application.required;

import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;

import java.util.Optional;

public interface CalculationRepository {

    void save(Calculation calculation);

    Optional<Calculation> findById(CalculationId id);
}
