/**
 * The only bridge to the backend.
 *
 * Everything that talks to the API goes through `request`, so timeouts, auth
 * headers, and error shaping live in exactly one place. Components never call
 * `fetch` directly — they call a query hook, which calls one of these.
 */

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

const DEFAULT_TIMEOUT_MS = 30_000;

/** An error carrying the HTTP status, so callers can branch on 404 vs 500. */
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

interface RequestOptions extends RequestInit {
  /** Abort after this many milliseconds. A hung request is worse than a failed one. */
  timeoutMs?: number;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, headers, body, ...init } = options;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  // FormData sets its own multipart boundary — forcing a JSON content-type
  // header onto it produces a request the server cannot parse.
  const isFormData = body instanceof FormData;

  try {
    const response = await fetch(`${BASE}${path}`, {
      ...init,
      body,
      signal: controller.signal,
      headers: {
        ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
        ...headers,
      },
    });

    if (!response.ok) {
      throw new ApiError(await readErrorMessage(response), response.status);
    }

    // 204 and other empty responses have no body to parse.
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return undefined as T;
    }
    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new ApiError(`Request to ${path} timed out after ${timeoutMs}ms.`, 408);
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

/** Prefer the API's `detail` field; fall back to raw text, then the status line. */
async function readErrorMessage(response: Response): Promise<string> {
  const text = await response.text().catch(() => '');
  if (!text) return response.statusText || `Request failed with ${response.status}`;
  try {
    const parsed: unknown = JSON.parse(text);
    if (parsed && typeof parsed === 'object' && 'detail' in parsed) {
      return String((parsed as { detail: unknown }).detail);
    }
  } catch {
    // Not JSON — the raw text is the best message available.
  }
  return text;
}

export type ItemStatus = 'draft' | 'ready' | 'archived';

export interface Item {
  id: string;
  name: string;
  status: ItemStatus;
  created_at: string;
}

export const api = {
  health: () => request<{ status: string; environment: string }>('/health'),

  items: {
    list: () => request<Item[]>('/items/'),
    get: (id: string) => request<Item>(`/items/${id}`),
    create: (name: string) =>
      request<Item>('/items/', { method: 'POST', body: JSON.stringify({ name }) }),
    setStatus: (id: string, status: ItemStatus) =>
      request<Item>(`/items/${id}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      }),
    remove: (id: string) => request<void>(`/items/${id}`, { method: 'DELETE' }),
  },
};
