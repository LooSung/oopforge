package com.oopforge.example.layered.calculator

import com.tngtech.archunit.core.domain.JavaClasses
import com.tngtech.archunit.core.importer.ClassFileImporter
import com.tngtech.archunit.core.importer.ImportOption
import com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses
import com.tngtech.archunit.library.Architectures.layeredArchitecture
import org.junit.jupiter.api.Test

/**
 * Enforces the layer-layout Hard Rule with the industry-standard ArchUnit,
 * on top of the fast stdlib archlint check. A reviewer can read these rules as
 * the executable spec of "what layered means here".
 */
class ArchitectureTest {

    private val classes: JavaClasses = ClassFileImporter()
        .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
        .importPackages(BASE)

    @Test
    fun layers_only_depend_downward() {
        layeredArchitecture().consideringOnlyDependenciesInLayers()
            .layer("Controller").definedBy("$BASE.controller..")
            .layer("Service").definedBy("$BASE.service..")
            .layer("Repository").definedBy("$BASE.repository..")
            .layer("Domain").definedBy("$BASE.domain..")
            .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
            .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service")
            .whereLayer("Domain").mayOnlyBeAccessedByLayers("Controller", "Service", "Repository")
            .check(classes)
    }

    @Test
    fun domain_is_framework_free() {
        noClasses()
            .that().resideInAPackage("$BASE.domain..")
            .should().dependOnClassesThat().resideInAnyPackage(
                "org.springframework..", "jakarta..", "org.springdoc..",
            )
            .check(classes)
    }

    private companion object {
        const val BASE = "com.oopforge.example.layered.calculator"
    }
}
