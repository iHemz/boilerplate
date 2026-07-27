import { render, screen } from '@testing-library/react';
import { ItemCard } from './ItemCard';
import type { Item } from '@/lib/api';

const item: Item = {
  id: '1',
  name: 'Acme',
  status: 'ready',
  created_at: '2026-01-01T00:00:00Z',
};

it('renders the item name', () => {
  render(<ItemCard item={item} />);
  expect(screen.getByText('Acme')).toBeInTheDocument();
});

it('renders the status badge', () => {
  render(<ItemCard item={item} />);
  expect(screen.getByText('ready')).toBeInTheDocument();
});
