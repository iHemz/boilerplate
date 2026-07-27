import { ItemsView } from '@/components/items/ItemsView';

/**
 * Server component: no `"use client"`, no hooks, no state. It composes the
 * page and hands interactivity to the view component below it.
 */
export default function HomePage() {
  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-12 sm:px-6">
      <h1 className="text-2xl font-semibold tracking-tight">Boilerplate</h1>
      <p className="text-foreground-muted mt-2 text-sm">
        A reference vertical slice: page → view → query hook → api → backend.
      </p>
      <div className="mt-8">
        <ItemsView />
      </div>
    </main>
  );
}
