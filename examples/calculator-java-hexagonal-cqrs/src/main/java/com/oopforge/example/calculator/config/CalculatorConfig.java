package com.oopforge.example.calculator.config;

import com.oopforge.example.calculator.adapter.persistence.CalculationStore;
import com.oopforge.example.calculator.adapter.persistence.InMemoryCalculationRepository;
import com.oopforge.example.calculator.adapter.persistence.InMemoryHistoryQueryRepository;
import com.oopforge.example.calculator.application.command.Calculate;
import com.oopforge.example.calculator.application.command.CalculateCommandService;
import com.oopforge.example.calculator.application.command.CalculationRepository;
import com.oopforge.example.calculator.application.query.CalculationHistory;
import com.oopforge.example.calculator.application.query.HistoryQueryRepository;
import com.oopforge.example.calculator.application.query.HistoryQueryService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CalculatorConfig {

    @Bean
    CalculationStore calculationStore() {
        return new CalculationStore();
    }

    @Bean
    CalculationRepository calculationRepository(CalculationStore store) {
        return new InMemoryCalculationRepository(store);
    }

    @Bean
    HistoryQueryRepository historyQueryRepository(CalculationStore store) {
        return new InMemoryHistoryQueryRepository(store);
    }

    @Bean
    Calculate calculate(CalculationRepository calculationRepository) {
        return new CalculateCommandService(calculationRepository);
    }

    @Bean
    CalculationHistory calculationHistory(HistoryQueryRepository historyQueryRepository) {
        return new HistoryQueryService(historyQueryRepository);
    }
}
