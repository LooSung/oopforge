package com.oopforge.example.layered

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class LayeredCalculatorApplication

fun main(args: Array<String>) {
    runApplication<LayeredCalculatorApplication>(*args)
}
