package com.oopforge.example.layered.calculator.repository;

import com.oopforge.example.layered.calculator.domain.Calculation;
import com.oopforge.example.layered.calculator.domain.CalculationId;

import java.util.Optional;

public interface CalculationRepository {

    void save(Calculation calculation);

    Optional<Calculation> findById(CalculationId id);
}
