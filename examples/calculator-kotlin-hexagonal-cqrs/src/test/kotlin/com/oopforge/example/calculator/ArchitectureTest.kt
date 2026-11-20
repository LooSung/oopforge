package com.oopforge.example.calculator

import com.tngtech.archunit.core.domain.JavaClasses
import com.tngtech.archunit.core.importer.ClassFileImporter
import com.tngtech.archunit.core.importer.ImportOption
import com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses
import org.junit.jupiter.api.Test

/**
 * Executable spec of "hexagonal + CQRS": the domain is framework-free, the
 * command and query sides stay isolated, and the application core never depends
 * on adapters. Complements the fast stdlib archlint cqrs check.
 */
class ArchitectureTest {

    private val classes: JavaClasses = ClassFileImporter()
        .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
        .importPackages(BASE)

    @Test
    fun domainIsFrameworkFree() {
        noClasses()
            .that().resideInAPackage("$BASE.domain..")
            .should().dependOnClassesThat().resideInAnyPackage(
                "org.springframework..", "jakarta..",
            )
            .check(classes)
    }

    @Test
    fun commandAndQuerySidesAreIsolated() {
        noClasses()
            .that().resideInAPackage("$BASE.application.command..")
            .should().dependOnClassesThat().resideInAPackage("$BASE.application.query..")
            .check(classes)

        noClasses()
            .that().resideInAPackage("$BASE.application.query..")
            .should().dependOnClassesThat().resideInAPackage("$BASE.application.command..")
            .check(classes)
    }

    @Test
    fun applicationDoesNotDependOnAdapters() {
        noClasses()
            .that().resideInAPackage("$BASE.application..")
            .should().dependOnClassesThat().resideInAPackage("$BASE.adapter..")
            .check(classes)
    }

    private companion object {
        const val BASE = "com.oopforge.example.calculator"
    }
}
