package com.oopforge.example.calculator.application.query;

import static org.assertj.core.api.Assertions.assertThat;

import com.oopforge.example.calculator.adapter.persistence.CalculationStore;
import com.oopforge.example.calculator.adapter.persistence.InMemoryCalculationRepository;
import com.oopforge.example.calculator.adapter.persistence.InMemoryHistoryQueryRepository;
import com.oopforge.example.calculator.application.command.Calculate;
import com.oopforge.example.calculator.application.command.CalculateCommandService;
import com.oopforge.example.calculator.domain.Operator;
import java.util.List;
import org.junit.jupiter.api.Test;

class HistoryQueryServiceTest {

    @Test
    void listsHistoryMostRecentFirstAfterCommands() {
        CalculationStore store = new CalculationStore();
        Calculate command = new CalculateCommandService(new InMemoryCalculationRepository(store));
        CalculationHistory query = new HistoryQueryService(new InMemoryHistoryQueryRepository(store));

        command.handle(new Calculate.CalculateCommand(1, Operator.ADD, 2));
        command.handle(new Calculate.CalculateCommand(5, Operator.MULTIPLY, 3));

        List<HistorySummary> history = query.listRecent(10);

        assertThat(history).hasSize(2);
        assertThat(history.get(0).result()).isEqualTo(15.0);
        assertThat(history.get(1).result()).isEqualTo(3.0);
    }
}
