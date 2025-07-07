import { render, screen } from '@testing-library/react';
import React from 'react';

describe('Sample Test', () => {
  it('renders without crashing', () => {
    render(<div>Hallo CROD</div>);
    expect(screen.getByText('Hallo CROD')).toBeInTheDocument();
  });
});
