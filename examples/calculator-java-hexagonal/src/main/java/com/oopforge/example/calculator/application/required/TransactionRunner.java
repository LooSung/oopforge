package com.oopforge.example.calculator.application.required;

import java.util.function.Supplier;

public interface TransactionRunner {

    <T> T run(Supplier<T> work);
}
