package com.oopforge.example.calculator.application.command;

import static org.assertj.core.api.Assertions.assertThat;

import com.oopforge.example.calculator.adapter.persistence.CalculationStore;
import com.oopforge.example.calculator.adapter.persistence.InMemoryCalculationRepository;
import com.oopforge.example.calculator.domain.CalculationId;
import com.oopforge.example.calculator.domain.Operator;
import org.junit.jupiter.api.Test;

class CalculateCommandServiceTest {

    @Test
    void returnsIdNotReadModel() {
        Calculate service = new CalculateCommandService(
                new InMemoryCalculationRepository(new CalculationStore()));

        CalculationId id = service.handle(new Calculate.CalculateCommand(10, Operator.ADD, 5));

        assertThat(id).isNotNull();
        assertThat(id.value()).isNotNull();
    }
}
