import { cn } from '@/lib/utils';
import type { Item, ItemStatus } from '@/lib/api';

const STATUS_STYLES: Record<ItemStatus, string> = {
  draft: 'bg-surface-muted text-foreground-muted',
  ready: 'bg-accent/10 text-accent',
  archived: 'bg-surface-muted text-foreground-muted line-through',
};

/**
 * A leaf presentational component: props in, markup out. No data fetching and
 * no state, which is what makes it trivial to test and reuse.
 */
export function ItemCard({ item, action }: { item: Item; action?: React.ReactNode }) {
  return (
    <li className="border-border flex items-center justify-between gap-4 rounded-xl border p-4">
      <div className="min-w-0">
        <p className="truncate font-medium">{item.name}</p>
        <span
          className={cn(
            'mt-1 inline-block rounded-md px-2 py-0.5 text-xs font-medium',
            STATUS_STYLES[item.status],
          )}
        >
          {item.status}
        </span>
      </div>
      {action}
    </li>
  );
}
