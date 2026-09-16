// engines.ts – จัดการ video engines

/** Engine identifiers supported by the pipeline. */
export type Engine = 'FAL' | 'MAGIC_HOUR';

/** Free-form payload forwarded to the provider adapter. */
export type EnginePayload = Record<string, unknown>;

/** Shape returned by every provider adapter. */
export interface EngineResult {
  id: string;
  status: 'queued' | 'ready' | 'failed';
  url?: string;
}

export async function runEngine(
  engine: Engine,
  payload: EnginePayload,
): Promise<EngineResult> {
  try {
    switch (engine) {
      case 'FAL':
        return await callFalEngine(payload);
      case 'MAGIC_HOUR':
        return await callMagicHour(payload);
      default: {
        // exhaustiveness guard — unreachable while Engine stays in sync
        const never: never = engine;
        throw new Error(`Engine ${String(never)} not supported`);
      }
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(`[Engine Error] ${message}`);
    throw err;
  }
}

async function callFalEngine(_payload: EnginePayload): Promise<EngineResult> {
  // TODO: implement API call
  throw new Error('FAL engine not implemented');
}

async function callMagicHour(_payload: EnginePayload): Promise<EngineResult> {
  // TODO: implement API call
  throw new Error('MagicHour engine not implemented');
}
