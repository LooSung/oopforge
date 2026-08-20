package com.oopforge.example.calculator.application.required;

import com.oopforge.example.calculator.domain.DomainEvent;

import java.util.List;

public interface DomainEventDispatcher {

    void dispatch(List<DomainEvent> events);
}
