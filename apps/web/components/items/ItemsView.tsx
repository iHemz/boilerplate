'use client';

import { useState } from 'react';
import { useCreateItem, useItems, useSetItemStatus } from '@/lib/queries/items';
import { ItemCard } from './ItemCard';

/**
 * The `*View` component is the assembly point: it owns client state and wires
 * query hooks to presentational children. Every UX state the feature can be in
 * — loading, error, empty, populated — is handled explicitly here.
 */
export function ItemsView() {
  const [name, setName] = useState('');
  const { data: items, isPending, isError, error } = useItems();
  const createItem = useCreateItem();
  const setStatus = useSetItemStatus();

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) return;
    createItem.mutate(trimmed, { onSuccess: () => setName('') });
  }

  return (
    <section>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <label htmlFor="item-name" className="sr-only">
          Item name
        </label>
        <input
          id="item-name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="New item name"
          className="border-border bg-surface focus-visible:border-accent w-full rounded-lg border px-3 py-2 text-sm transition-colors outline-none"
        />
        <button
          type="submit"
          disabled={createItem.isPending || !name.trim()}
          className="bg-accent hover:bg-accent-hover focus-visible:outline-accent shrink-0 rounded-lg px-4 py-2 text-sm font-medium text-white transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50"
        >
          {createItem.isPending ? 'Adding…' : 'Add'}
        </button>
      </form>

      {isPending && (
        <div className="mt-6 space-y-2" aria-busy="true" aria-label="Loading items">
          {[0, 1, 2].map((row) => (
            <div key={row} className="bg-surface-muted h-[70px] animate-pulse rounded-xl" />
          ))}
        </div>
      )}

      {isError && (
        <p role="alert" className="text-danger mt-6 text-sm">
          Could not load items: {error.message}
        </p>
      )}

      {items && items.length === 0 && (
        <p className="text-foreground-muted mt-6 text-sm">No items yet. Add one above.</p>
      )}

      {items && items.length > 0 && (
        <ul className="mt-6 space-y-2">
          {items.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              action={
                item.status === 'draft' ? (
                  <button
                    onClick={() => setStatus.mutate({ id: item.id, status: 'ready' })}
                    disabled={setStatus.isPending}
                    className="border-border hover:bg-surface-muted focus-visible:outline-accent shrink-0 rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50"
                  >
                    Mark ready
                  </button>
                ) : null
              }
            />
          ))}
        </ul>
      )}
    </section>
  );
}
