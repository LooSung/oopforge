package com.oopforge.example.calculator.application.required

interface TransactionRunner {

    fun <T> run(work: () -> T): T
}
