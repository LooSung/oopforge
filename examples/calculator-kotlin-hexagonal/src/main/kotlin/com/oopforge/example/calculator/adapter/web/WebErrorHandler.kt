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
    fun invalidRequest(): ApiError = ApiError("invalid_request", "The request is invalid.")

    @ExceptionHandler(IdempotencyConflictException::class)
    @ResponseStatus(HttpStatus.CONFLICT)
    fun idempotencyConflict(): ApiError =
        ApiError("idempotency_conflict", "The idempotency key was already used for a different request.")

    @ExceptionHandler(IllegalArgumentException::class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    fun domainError(): ApiError = ApiError("calculation_rejected", "The calculation could not be performed.")

    @ExceptionHandler(Exception::class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    fun unexpectedFailure(): ApiError {
        LOGGER.error("Unexpected calculation request failure")
        return ApiError("internal_error", "The request could not be completed.")
    }

    private companion object {
        val LOGGER: Logger = LoggerFactory.getLogger(WebErrorHandler::class.java)
    }
}
