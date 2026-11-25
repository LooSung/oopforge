import { Controller, Get, NotFoundException, Param, Query } from '@nestjs/common';
import { ApiBadRequestResponse, ApiNotFoundResponse, ApiOkResponse, ApiQuery, ApiTags } from '@nestjs/swagger';

import { CalculationHistory } from '../../application/query/calculation-history.js';
import { CalculationId } from '../../domain/calculation-id.js';
import { type HistoryEntryResponse, type HistoryListResponse, toHistoryEntryResponse } from './history-entry.response.js';
import { calculationIdParam, historyLimitQuery } from './query.params.js';

@ApiTags('Calculator Queries')
@Controller('api/v1/calculations')
export class CalculatorQueryController {
  constructor(private readonly calculationHistory: CalculationHistory) {}

  // Declared before ':calculationId' so Nest registers the literal path first.
  @Get('history')
  @ApiOkResponse({ description: 'Recent calculations, most recent first' })
  @ApiBadRequestResponse({ description: 'limit is not a positive integer' })
  // The schema's default makes limit optional; the generated parameter says required.
  @ApiQuery({ name: 'limit', required: false })
  async listHistory(@Query('limit', { schema: historyLimitQuery }) limit: number): Promise<HistoryListResponse> {
    const summaries = await this.calculationHistory.listRecent(limit);
    return { items: summaries.map(toHistoryEntryResponse) };
  }

  @Get(':calculationId')
  @ApiOkResponse({ description: 'One calculation from the history' })
  @ApiBadRequestResponse({ description: 'calculationId is not a UUID' })
  @ApiNotFoundResponse({ description: 'No calculation with this id' })
  async getCalculation(
    @Param('calculationId', { schema: calculationIdParam }) calculationId: string,
  ): Promise<HistoryEntryResponse> {
    const summary = await this.calculationHistory.findById(CalculationId.of(calculationId));
    if (summary === undefined) {
      throw new NotFoundException();
    }
    return toHistoryEntryResponse(summary);
  }
}
