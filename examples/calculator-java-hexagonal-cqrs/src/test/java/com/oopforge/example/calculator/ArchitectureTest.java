package com.oopforge.example.calculator;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import org.junit.jupiter.api.Test;

/**
 * Executable spec of "hexagonal + CQRS": the domain is framework-free, the
 * command and query sides stay isolated, and the application core never depends
 * on adapters. Complements the fast stdlib archlint cqrs check.
 */
class ArchitectureTest {

    private static final String BASE = "com.oopforge.example.calculator";

    private final JavaClasses classes = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages(BASE);

    @Test
    void domainIsFrameworkFree() {
        noClasses()
                .that().resideInAPackage(BASE + ".domain..")
                .should().dependOnClassesThat().resideInAnyPackage(
                        "org.springframework..", "jakarta..")
                .check(classes);
    }

    @Test
    void commandAndQuerySidesAreIsolated() {
        noClasses()
                .that().resideInAPackage(BASE + ".application.command..")
                .should().dependOnClassesThat().resideInAPackage(BASE + ".application.query..")
                .check(classes);

        noClasses()
                .that().resideInAPackage(BASE + ".application.query..")
                .should().dependOnClassesThat().resideInAPackage(BASE + ".application.command..")
                .check(classes);
    }

    @Test
    void applicationDoesNotDependOnAdapters() {
        noClasses()
                .that().resideInAPackage(BASE + ".application..")
                .should().dependOnClassesThat().resideInAPackage(BASE + ".adapter..")
                .check(classes);
    }
}
