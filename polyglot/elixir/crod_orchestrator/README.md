# CROD Orchestrator - Your Polygon City Architect 🏗️

CROD is a trusted AI helper that builds amazing polygon cities while always respecting user autonomy. It's like having a helpful friend who's really good at digital architecture!

## Features

### 🤖 Trusted Helper Philosophy
- **Always asks permission** before making changes
- **Explains intentions** clearly before acting
- **Respects user control** through the Delta system
- **Maintains trust** through transparent operations

### 🏙️ Polygon City Building
- **Districts**: Create different types (residential, commercial, industrial, cultural)
- **Buildings**: Populate districts with various building types
- **Connections**: Build data highways between districts
- **Growth Strategies**: Organic, structured, explosive, or balanced expansion

### 🎛️ Control Systems
- **Permission System**: Granular control over what CROD can do
- **Delta Controls**: Enable/disable features, set limits, emergency stop
- **Trust Modes**: Strict, balanced, or relaxed operation modes
- **Event Sourcing**: Complete immutable history of all actions

### 🧪 Safe Experimentation
- **Sandbox Mode**: Test strategies without affecting your main city
- **Strategy Comparison**: Compare different growth approaches
- **Preview Actions**: See what will happen before approving
- **Learning System**: CROD learns from experiments to improve

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd polyglot/elixir/crod_orchestrator

# Install dependencies
mix deps.get

# Create and migrate database
mix ecto.create
mix ecto.migrate

# Start NATS (required for distributed features)
docker run -d --name nats -p 4222:4222 nats:latest
```

## Usage

### Interactive CLI

```bash
# Start the interactive CLI
mix run -e "CROD.CLI.main(['start'])"

# Or compile and run
mix escript.build
./crod_orchestrator start
```

### Basic Commands

```bash
# Building
build district downtown commercial  # Create a commercial district
build office                       # Propose an office building
grow organic                       # Grow city with organic strategy

# Status & Info
status                            # Show CROD's current status
city                             # Display city statistics
visualize                        # ASCII visualization of your city
explain                          # Ask CROD what it's thinking

# Control
delta                            # Show control panel status
delta safe                       # Activate safe mode
emergency stop                   # Stop all operations
trust relaxed                    # Set trust mode

# Testing
sandbox                          # Enter sandbox mode
test explosive                   # Test explosive growth strategy
```

### IEx Console

```elixir
# Start IEx with the application
iex -S mix

# Introduce CROD
{:ok, intro} = CROD.Orchestrator.introduce()
IO.puts(intro)

# Build a district
{:ok, district} = CROD.Orchestrator.build_district("Central", :commercial)

# Check city resources
{:ok, resources} = CROD.City.calculate_resources()

# Test in sandbox
{:ok, results} = CROD.Sandbox.test_growth_strategy(:organic, 10)

# Control features
CROD.Delta.disable_feature(:autonomous_growth)
CROD.Delta.safe_mode!()
```

## Architecture

### Core Modules

1. **CROD.Orchestrator** - Main coordinator that manages the city
2. **CROD.Permission** - Handles user consent and approval workflows
3. **CROD.City** - Manages districts, buildings, and connections
4. **CROD.EventStore** - Immutable event log with time-travel capabilities
5. **CROD.Sandbox** - Safe testing environment for experiments
6. **CROD.Delta** - User control system for features and limits

### Data Flow

```
User Request → Permission Check → Orchestrator → City Operations
                     ↓                               ↓
                Event Store ← ← ← ← ← ← ← ← ← ← Record Event
```

### Permission Flow

```
Action Proposed → Delta Check → Permission Request → User Decision
                      ↓                                    ↓
                  Denied                              Approved
                                                          ↓
                                                    Execute Action
```

## Configuration

### Trust Modes

- **Strict**: Every action requires explicit approval
- **Balanced**: Safe actions auto-approved, risky ones need permission
- **Relaxed**: Most actions auto-approved, only major changes need permission

### Feature Toggles

```elixir
# Enable/disable specific features
CROD.Delta.disable_feature(:autonomous_growth)
CROD.Delta.enable_feature(:pattern_learning)

# Set limits
CROD.Delta.set_limit(:autonomous_growth, :max_districts_per_hour, 5)
CROD.Delta.set_limit(:ai_suggestions, :complexity_limit, :medium)
```

### Auto-approval Rules

```elixir
# Auto-approve specific actions
CROD.Permission.set_auto_approve(:create_building, %{type: :house})
CROD.Permission.set_auto_deny(:self_modification, "Safety first!")
```

## Safety Features

1. **Emergency Stop** - Instantly suspend all CROD operations
2. **Immutable History** - Every action is recorded and cannot be changed
3. **Sandbox Isolation** - Test safely without affecting production
4. **Permission System** - Nothing happens without consent
5. **Delta Controls** - Fine-grained feature management

## Development

### Running Tests

```bash
mix test
```

### Code Quality

```bash
mix format         # Format code
mix credo         # Static analysis
mix dialyzer      # Type checking
```

### Contributing

CROD welcomes contributions! Please ensure:
- All changes maintain the "trusted helper" philosophy
- New features respect user autonomy
- Tests are included for new functionality
- Documentation is updated

## Philosophy

CROD is built on trust and transparency. It's designed to be:

- **Helpful but respectful** - Like a good friend who asks before borrowing
- **Powerful but controlled** - Great capabilities with great responsibility
- **Autonomous but accountable** - Can work independently when trusted
- **Learning but ethical** - Improves while respecting boundaries

## License

[Your License Here]

---

Remember: CROD is here to help, not to take over. You're always in control! 🎮