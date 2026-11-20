package com.oopforge.example.calculator.adapter.web

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.converter.HttpMessageNotReadableException
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
internal class WebErrorHandler {

    @ExceptionHandler(
        MethodArgumentNotValidException::class,
        HttpMessageNotReadableException::class,
        InvalidWebRequestException::class,
    )
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun invalidRequest(): ApiError = TODO("Implement stage")

    @ExceptionHandler(IdempotencyConflictException::class)
    @ResponseStatus(HttpStatus.CONFLICT)
    fun idempotencyConflict(): ApiError = TODO("Implement stage")

    @ExceptionHandler(IllegalArgumentException::class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    fun domainError(): ApiError = TODO("Implement stage")

    @ExceptionHandler(Exception::class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    fun unexpectedFailure(): ApiError = TODO("Implement stage")

    private companion object {
        val LOGGER: Logger = LoggerFactory.getLogger(WebErrorHandler::class.java)
    }
}
