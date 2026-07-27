'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api, type ItemStatus } from '@/lib/api';

/**
 * One query-key factory per domain. Deriving keys from a single object stops
 * the drift you get from string literals scattered across components — a typo
 * in a key is a cache miss that looks like a bug elsewhere.
 */
export const itemKeys = {
  all: ['items'] as const,
  detail: (id: string) => ['items', id] as const,
};

export function useItems() {
  return useQuery({ queryKey: itemKeys.all, queryFn: api.items.list });
}

export function useItem(id: string) {
  return useQuery({ queryKey: itemKeys.detail(id), queryFn: () => api.items.get(id) });
}

export function useCreateItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (name: string) => api.items.create(name),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: itemKeys.all }),
  });
}

export function useSetItemStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: ItemStatus }) =>
      api.items.setStatus(id, status),
    onSuccess: (item) => {
      queryClient.invalidateQueries({ queryKey: itemKeys.all });
      queryClient.invalidateQueries({ queryKey: itemKeys.detail(item.id) });
    },
  });
}
