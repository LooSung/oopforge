package com.oopforge.example.calculator.adapter.persistence;

import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryCalculationRepository implements CalculationRepository {

    private final Map<CalculationId, Calculation> store = new ConcurrentHashMap<>();

    @Override
    public void save(Calculation calculation) {
        store.put(calculation.id(), calculation);
    }

    @Override
    public Optional<Calculation> findById(CalculationId id) {
        return Optional.ofNullable(store.get(id));
    }
}
