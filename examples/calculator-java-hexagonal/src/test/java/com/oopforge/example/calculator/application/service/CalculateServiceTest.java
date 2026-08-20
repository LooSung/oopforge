package com.oopforge.example.calculator.application.service;

import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter;
import com.oopforge.example.calculator.application.provided.Calculate;
import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.application.required.DomainEventDispatcher;
import com.oopforge.example.calculator.application.required.TransactionRunner;
import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;
import com.oopforge.example.calculator.domain.CalculationPerformed;
import com.oopforge.example.calculator.domain.DomainEvent;
import com.oopforge.example.calculator.domain.Operator;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Supplier;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class CalculateServiceTest {

    @Test
    void savesBeforeDrainingAndDispatchesEventsOnce() {
        List<String> calls = new ArrayList<>();
        RecordingRepository repository = new RecordingRepository(calls);
        RecordingDispatcher dispatcher = new RecordingDispatcher(calls);
        CalculateService service = new CalculateService(
                repository, new RecordingTransactionRunner(calls), dispatcher);

        service.handle(new Calculate.CalculateCommand(2, Operator.ADD, 3));

        assertThat(calls).containsExactly("transaction", "save", "dispatch");
        assertThat(dispatcher.invocationCount).isOne();
        assertThat(dispatcher.events).hasSize(1);
        assertThat(repository.saved.popEvents()).isEmpty();
    }

    @Test
    void appendsTheDrainedEventToTheOutbox() {
        InMemoryTransactionalAdapter store = new InMemoryTransactionalAdapter();
        DomainEventDispatcher dispatcher = dispatcherWith(new CalculationPerformedHandler(store));
        CalculateService service = new CalculateService(store, store, dispatcher);

        Calculate.CalculationResult result =
                service.handle(new Calculate.CalculateCommand(8, Operator.MULTIPLY, 4));

        Calculation saved = store.findById(CalculationId.of(result.calculationId())).orElseThrow();
        assertThat(saved.popEvents()).isEmpty();
        assertThat(store.unpublished()).hasSize(1);
    }

    @Test
    void rollsBackCalculationAndOutboxWhenAHandlerFails() {
        InMemoryTransactionalAdapter store = new InMemoryTransactionalAdapter();
        FailingHandler failingHandler = new FailingHandler();
        DomainEventDispatcher dispatcher = dispatcherWith(
                new CalculationPerformedHandler(store), failingHandler);
        CalculateService service = new CalculateService(store, store, dispatcher);

        assertThatThrownBy(() ->
                service.handle(new Calculate.CalculateCommand(8, Operator.DIVIDE, 2)))
                .isInstanceOf(IllegalStateException.class);

        assertThat(store.findById(failingHandler.event.calculationId())).isEmpty();
        assertThat(store.unpublished()).isEmpty();
    }

    private DomainEventDispatcher dispatcherWith(DomainEventHandler<?>... handlers) {
        return new SynchronousDomainEventDispatcher(List.of(handlers));
    }

    private static final class RecordingTransactionRunner implements TransactionRunner {
        private final List<String> calls;

        private RecordingTransactionRunner(List<String> calls) {
            this.calls = calls;
        }

        @Override
        public <T> T run(Supplier<T> work) {
            calls.add("transaction");
            return work.get();
        }
    }

    private static final class RecordingRepository implements CalculationRepository {
        private final List<String> calls;
        private Calculation saved;

        private RecordingRepository(List<String> calls) {
            this.calls = calls;
        }

        @Override
        public void save(Calculation calculation) {
            calls.add("save");
            saved = calculation;
        }

        @Override
        public Optional<Calculation> findById(CalculationId id) {
            return Optional.ofNullable(saved).filter(calculation -> calculation.id().equals(id));
        }
    }

    private static final class RecordingDispatcher implements DomainEventDispatcher {
        private final List<String> calls;
        private List<DomainEvent> events = List.of();
        private int invocationCount;

        private RecordingDispatcher(List<String> calls) {
            this.calls = calls;
        }

        @Override
        public void dispatch(List<DomainEvent> events) {
            this.calls.add("dispatch");
            this.events = List.copyOf(events);
            invocationCount++;
        }
    }

    private static final class FailingHandler implements DomainEventHandler<CalculationPerformed> {
        private CalculationPerformed event;

        @Override
        public Class<CalculationPerformed> eventType() {
            return CalculationPerformed.class;
        }

        @Override
        public void handle(CalculationPerformed event) {
            this.event = event;
            throw new IllegalStateException("handler failed");
        }
    }
}
