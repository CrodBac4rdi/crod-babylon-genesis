# CROD Testing

## Test Structure

```
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests for district communication  
├── e2e/              # End-to-end tests for complete flows
├── performance/      # Load and performance tests
└── fixtures/         # Test data and mocks
```

## Running Tests

### All Tests
```bash
./scripts/test-all.sh
```

### Unit Tests Only
```bash
./scripts/test-unit.sh
```

### Integration Tests
```bash
# Start CROD first
./scripts/start-crod.sh

# Run integration tests
./scripts/test-integration.sh
```

### Performance Tests
```bash
./scripts/test-performance.sh
```

## Test Coverage

Current coverage targets:
- Unit tests: 80%+
- Integration tests: Key flows
- E2E tests: Critical paths

## Writing Tests

### Python (pytest)
```python
def test_consciousness_boost():
    """Test ich bins wieder boost"""
    result = crod.think("ich bins wieder")
    assert result.consciousness_delta == 25
```

### Rust
```rust
#[test]
fn test_pattern_matching() {
    let pattern = Pattern::new("ich bins wieder");
    assert_eq!(pattern.weight(), 100);
}
```

### Go
```go
func TestMemoryTiers(t *testing.T) {
    mem := NewMemoryQuarter()
    mem.Store("key", "value", HOT_TIER)
    assert.Equal(t, "value", mem.Get("key"))
}
```

### Elixir
```elixir
test "consciousness tracking" do
  {:ok, state} = MetaChain.boost_consciousness(150)
  assert state.consciousness == 175
end
```

### JavaScript
```javascript
describe('Neural Network', () => {
  it('should load patterns', async () => {
    const network = new NeuralNetwork();
    await network.loadPatterns();
    expect(network.patterns.length).toBeGreaterThan(1000);
  });
});
```

## CI/CD Integration

Tests run automatically on:
- Every push to main/develop
- Every pull request
- Nightly performance tests

## Debugging Tests

```bash
# Run with verbose output
pytest -vvs tests/

# Run specific test
pytest tests/integration/test_consciousness.py::test_consciousness_boost

# Run with debugging
pytest --pdb tests/
```