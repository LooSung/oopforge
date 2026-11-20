package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter
import com.oopforge.example.calculator.application.provided.Calculate
import com.oopforge.example.calculator.application.required.CalculationRepository
import com.oopforge.example.calculator.application.required.DomainEventDispatcher
import com.oopforge.example.calculator.application.required.TransactionRunner
import com.oopforge.example.calculator.domain.Calculation
import com.oopforge.example.calculator.domain.CalculationId
import com.oopforge.example.calculator.domain.CalculationPerformed
import com.oopforge.example.calculator.domain.DomainEvent
import com.oopforge.example.calculator.domain.Operator
import org.assertj.core.api.Assertions.assertThat
import org.assertj.core.api.Assertions.assertThatThrownBy
import org.junit.jupiter.api.Test

class CalculateServiceTest {

    @Test
    fun savesBeforeDrainingAndDispatchesEventsOnce() {
        val calls = mutableListOf<String>()
        val repository = RecordingRepository(calls)
        val dispatcher = RecordingDispatcher(calls)
        val service = CalculateService(repository, RecordingTransactionRunner(calls), dispatcher)

        service.handle(Calculate.CalculateCommand(2.0, Operator.ADD, 3.0))

        assertThat(calls).containsExactly("transaction", "save", "dispatch")
        assertThat(dispatcher.invocationCount).isOne()
        assertThat(dispatcher.events).hasSize(1)
        assertThat(repository.saved?.popEvents()).isEmpty()
    }

    @Test
    fun appendsTheDrainedEventToTheOutbox() {
        val store = InMemoryTransactionalAdapter()
        val dispatcher = dispatcherWith(CalculationPerformedHandler(store))
        val service = CalculateService(store, store, dispatcher)

        val result = service.handle(Calculate.CalculateCommand(8.0, Operator.MULTIPLY, 4.0))

        val saved = checkNotNull(store.findById(CalculationId.of(result.calculationId)))
        assertThat(saved.popEvents()).isEmpty()
        assertThat(store.unpublished()).hasSize(1)
    }

    @Test
    fun rollsBackCalculationAndOutboxWhenAHandlerFails() {
        val store = InMemoryTransactionalAdapter()
        val failingHandler = FailingHandler()
        val dispatcher = dispatcherWith(CalculationPerformedHandler(store), failingHandler)
        val service = CalculateService(store, store, dispatcher)

        assertThatThrownBy { service.handle(Calculate.CalculateCommand(8.0, Operator.DIVIDE, 2.0)) }
            .isInstanceOf(IllegalStateException::class.java)

        assertThat(store.findById(checkNotNull(failingHandler.event).calculationId)).isNull()
        assertThat(store.unpublished()).isEmpty()
    }

    private fun dispatcherWith(vararg handlers: DomainEventHandler<*>): DomainEventDispatcher =
        SynchronousDomainEventDispatcher(handlers.toList())

    private class RecordingTransactionRunner(private val calls: MutableList<String>) : TransactionRunner {
        override fun <T> run(work: () -> T): T {
            calls.add("transaction")
            return work()
        }
    }

    private class RecordingRepository(private val calls: MutableList<String>) : CalculationRepository {
        var saved: Calculation? = null
            private set

        override fun save(calculation: Calculation) {
            calls.add("save")
            saved = calculation
        }

        override fun findById(id: CalculationId): Calculation? = saved?.takeIf { it.id == id }
    }

    private class RecordingDispatcher(private val calls: MutableList<String>) : DomainEventDispatcher {
        var events: List<DomainEvent> = emptyList()
            private set
        var invocationCount: Int = 0
            private set

        override fun dispatch(events: List<DomainEvent>) {
            calls.add("dispatch")
            this.events = events.toList()
            invocationCount++
        }
    }

    private class FailingHandler : DomainEventHandler<CalculationPerformed> {
        var event: CalculationPerformed? = null
            private set

        override fun eventType(): Class<CalculationPerformed> = CalculationPerformed::class.java

        override fun handle(event: CalculationPerformed) {
            this.event = event
            throw IllegalStateException("handler failed")
        }
    }
}
