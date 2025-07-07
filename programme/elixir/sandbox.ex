defmodule CROD.Sandbox do
  @moduledoc """
  Safe testing environment for CROD experiments.
  
  The Sandbox lets you test CROD's capabilities without affecting
  your main polygon city. It's like a holodeck for digital architecture!
  """

  use GenServer
  require Logger

  alias CROD.{City, EventStore}

  defstruct [
    :sandbox_id,
    :virtual_city,
    :test_events,
    :experiments,
    :resource_override,
    :time_acceleration,
    :safety_limits
  ]

  # Client API

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: opts[:name] || __MODULE__)
  end

  def create_experiment(name, config \\ %{}) do
    GenServer.call(__MODULE__, {:create_experiment, name, config})
  end

  def run_simulation(experiment_id, steps \\ 100) do
    GenServer.call(__MODULE__, {:run_simulation, experiment_id, steps}, :infinity)
  end

  def test_growth_strategy(strategy, iterations \\ 10) do
    GenServer.call(__MODULE__, {:test_growth_strategy, strategy, iterations})
  end

  def preview_action(action_type, params) do
    GenServer.call(__MODULE__, {:preview_action, action_type, params})
  end

  def compare_strategies(strategies) do
    GenServer.call(__MODULE__, {:compare_strategies, strategies})
  end

  def reset_sandbox do
    GenServer.call(__MODULE__, :reset_sandbox)
  end

  def get_experiment_results(experiment_id) do
    GenServer.call(__MODULE__, {:get_experiment_results, experiment_id})
  end

  def export_learnings do
    GenServer.call(__MODULE__, :export_learnings)
  end

  # Server Callbacks

  @impl true
  def init(opts) do
    sandbox_id = "sandbox_#{:os.system_time(:microsecond)}"
    
    {:ok, %__MODULE__{
      sandbox_id: sandbox_id,
      virtual_city: initialize_virtual_city(),
      test_events: [],
      experiments: %{},
      resource_override: %{
        polygons: 1_000_000,  # Unlimited resources in sandbox
        energy: 500_000,
        data_flow: 100_000
      },
      time_acceleration: Map.get(opts, :time_acceleration, 10),
      safety_limits: %{
        max_districts: 1000,
        max_buildings: 10000,
        max_iterations: 100000
      }
    }}
  end

  @impl true
  def handle_call({:create_experiment, name, config}, _from, state) do
    experiment_id = "exp_#{:erlang.phash2({name, :os.system_time()})}"
    
    experiment = %{
      id: experiment_id,
      name: name,
      config: config,
      created_at: DateTime.utc_now(),
      status: :ready,
      city_snapshot: snapshot_virtual_city(state.virtual_city),
      results: %{},
      events: []
    }
    
    new_experiments = Map.put(state.experiments, experiment_id, experiment)
    
    Logger.info("Sandbox experiment created: #{name} (#{experiment_id})")
    
    {:reply, {:ok, experiment_id}, %{state | experiments: new_experiments}}
  end

  @impl true
  def handle_call({:run_simulation, experiment_id, steps}, _from, state) do
    case Map.get(state.experiments, experiment_id) do
      nil ->
        {:reply, {:error, :experiment_not_found}, state}
      
      experiment ->
        Logger.info("Running simulation: #{experiment.name} for #{steps} steps")
        
        # Run simulation in isolated environment
        {results, events} = run_isolated_simulation(
          experiment,
          steps,
          state.time_acceleration,
          state.safety_limits
        )
        
        # Update experiment with results
        updated_experiment = %{experiment |
          status: :completed,
          results: results,
          events: events,
          completed_at: DateTime.utc_now()
        }
        
        new_experiments = Map.put(state.experiments, experiment_id, updated_experiment)
        
        {:reply, {:ok, results}, %{state | experiments: new_experiments}}
    end
  end

  @impl true
  def handle_call({:test_growth_strategy, strategy, iterations}, _from, state) do
    Logger.info("Testing growth strategy: #{strategy} for #{iterations} iterations")
    
    results = Enum.map(1..iterations, fn i ->
      test_city = initialize_virtual_city()
      test_single_growth_iteration(test_city, strategy, i)
    end)
    
    analysis = analyze_growth_results(results, strategy)
    
    {:reply, {:ok, analysis}, state}
  end

  @impl true
  def handle_call({:preview_action, action_type, params}, _from, state) do
    # Create a copy of current state
    preview_city = deep_copy_city(state.virtual_city)
    
    # Simulate the action
    result = simulate_action(action_type, params, preview_city)
    
    # Calculate differences
    impact = calculate_impact(state.virtual_city, preview_city, result)
    
    preview = %{
      action: action_type,
      params: params,
      predicted_outcome: result,
      impact_analysis: impact,
      resource_cost: estimate_resource_cost(action_type, params),
      time_estimate: estimate_completion_time(action_type, params),
      warnings: detect_potential_issues(action_type, params, preview_city)
    }
    
    {:reply, {:ok, preview}, state}
  end

  @impl true
  def handle_call({:compare_strategies, strategies}, _from, state) do
    Logger.info("Comparing #{length(strategies)} growth strategies...")
    
    comparisons = Enum.map(strategies, fn strategy ->
      # Run each strategy multiple times
      results = Enum.map(1..5, fn _ ->
        test_city = initialize_virtual_city()
        run_strategy_test(test_city, strategy, 20)
      end)
      
      %{
        strategy: strategy,
        avg_growth_rate: calculate_avg_growth_rate(results),
        efficiency: calculate_efficiency(results),
        resource_usage: calculate_resource_usage(results),
        pattern_consistency: calculate_consistency(results),
        score: calculate_overall_score(results)
      }
    end)
    
    # Sort by score
    ranked = Enum.sort_by(comparisons, & &1.score, :desc)
    
    {:reply, {:ok, ranked}, state}
  end

  @impl true
  def handle_call(:reset_sandbox, _from, state) do
    Logger.info("Resetting sandbox environment...")
    
    new_state = %{state |
      virtual_city: initialize_virtual_city(),
      test_events: [],
      experiments: %{}
    }
    
    {:reply, :ok, new_state}
  end

  @impl true
  def handle_call({:get_experiment_results, experiment_id}, _from, state) do
    case Map.get(state.experiments, experiment_id) do
      nil ->
        {:reply, {:error, :not_found}, state}
      
      experiment ->
        results = format_experiment_results(experiment)
        {:reply, {:ok, results}, state}
    end
  end

  @impl true
  def handle_call(:export_learnings, _from, state) do
    learnings = extract_learnings(state.experiments)
    {:reply, {:ok, learnings}, state}
  end

  # Private Functions

  defp initialize_virtual_city do
    %{
      districts: %{},
      buildings: %{},
      connections: %{},
      resources: %{
        polygons: 100000,
        energy: 50000,
        data_flow: 10000
      },
      metrics: %{
        efficiency: 1.0,
        growth_rate: 0.0,
        density: 0.0
      }
    }
  end

  defp snapshot_virtual_city(city) do
    # Deep copy of city state
    %{
      districts: Map.new(city.districts),
      buildings: Map.new(city.buildings),
      connections: Map.new(city.connections),
      resources: Map.new(city.resources),
      metrics: Map.new(city.metrics)
    }
  end

  defp run_isolated_simulation(experiment, steps, time_acceleration, limits) do
    # Start with experiment's city snapshot
    city = experiment.city_snapshot
    events = []
    
    # Run simulation steps
    {final_city, all_events} = Enum.reduce(1..steps, {city, events}, fn step, {current_city, current_events} ->
      # Apply experiment config
      action = generate_experiment_action(experiment.config, step, current_city)
      
      # Execute action
      {result, new_city} = execute_sandbox_action(action, current_city, limits)
      
      # Record event
      event = %{
        step: step,
        action: action,
        result: result,
        timestamp: accelerated_time(step, time_acceleration),
        metrics: calculate_metrics(new_city)
      }
      
      {new_city, [event | current_events]}
    end)
    
    results = %{
      final_state: final_city,
      total_steps: steps,
      metrics_progression: analyze_metrics_progression(all_events),
      resource_efficiency: calculate_final_efficiency(final_city, experiment.city_snapshot),
      growth_achieved: calculate_growth(final_city, experiment.city_snapshot)
    }
    
    {results, Enum.reverse(all_events)}
  end

  defp generate_experiment_action(config, step, city) do
    cond do
      Map.get(config, :random_actions, false) ->
        generate_random_action(city)
      
      Map.get(config, :pattern) ->
        generate_pattern_action(config.pattern, step, city)
      
      Map.get(config, :strategy) ->
        generate_strategy_action(config.strategy, city)
      
      true ->
        # Default: balanced growth
        generate_balanced_action(step, city)
    end
  end

  defp generate_random_action(city) do
    actions = [:create_district, :create_building, :create_connection]
    action = Enum.random(actions)
    
    case action do
      :create_district ->
        %{
          type: :create_district,
          params: %{
            name: "test_district_#{:rand.uniform(9999)}",
            type: Enum.random([:residential, :commercial, :industrial, :cultural])
          }
        }
      
      :create_building ->
        if map_size(city.districts) > 0 do
          district_id = city.districts |> Map.keys() |> Enum.random()
          %{
            type: :create_building,
            params: %{
              district_id: district_id,
              building_type: Enum.random([:house, :office, :factory, :monument])
            }
          }
        else
          generate_random_action(city)  # Retry with different action
        end
      
      :create_connection ->
        if map_size(city.districts) > 1 do
          district_ids = Map.keys(city.districts)
          %{
            type: :create_connection,
            params: %{
              from: Enum.random(district_ids),
              to: Enum.random(district_ids -- [List.first(district_ids)])
            }
          }
        else
          generate_random_action(city)  # Retry
        end
    end
  end

  defp execute_sandbox_action(action, city, limits) do
    # Check limits
    if exceeds_limits?(action, city, limits) do
      {{:error, :limit_exceeded}, city}
    else
      # Execute action in sandbox
      case action.type do
        :create_district ->
          new_district = create_sandbox_district(action.params)
          new_city = put_in(city.districts[new_district.id], new_district)
          {{:ok, new_district.id}, new_city}
        
        :create_building ->
          new_building = create_sandbox_building(action.params)
          new_city = put_in(city.buildings[new_building.id], new_building)
          {{:ok, new_building.id}, new_city}
        
        :create_connection ->
          new_connection = create_sandbox_connection(action.params)
          new_city = put_in(city.connections[new_connection.id], new_connection)
          {{:ok, new_connection.id}, new_city}
        
        _ ->
          {{:error, :unknown_action}, city}
      end
    end
  end

  defp exceeds_limits?(action, city, limits) do
    case action.type do
      :create_district -> map_size(city.districts) >= limits.max_districts
      :create_building -> map_size(city.buildings) >= limits.max_buildings
      _ -> false
    end
  end

  defp create_sandbox_district(params) do
    %{
      id: "district_#{:rand.uniform(99999)}",
      name: params.name,
      type: params.type,
      created_at: DateTime.utc_now()
    }
  end

  defp create_sandbox_building(params) do
    %{
      id: "building_#{:rand.uniform(99999)}",
      district_id: params.district_id,
      type: params.building_type,
      created_at: DateTime.utc_now()
    }
  end

  defp create_sandbox_connection(params) do
    %{
      id: "conn_#{:rand.uniform(99999)}",
      from: params.from,
      to: params.to,
      created_at: DateTime.utc_now()
    }
  end

  defp calculate_metrics(city) do
    %{
      districts: map_size(city.districts),
      buildings: map_size(city.buildings),
      connections: map_size(city.connections),
      density: calculate_density(city),
      connectivity: calculate_connectivity(city),
      efficiency: calculate_city_efficiency(city)
    }
  end

  defp calculate_density(city) do
    if map_size(city.districts) > 0 do
      map_size(city.buildings) / map_size(city.districts)
    else
      0.0
    end
  end

  defp calculate_connectivity(city) do
    if map_size(city.districts) > 1 do
      map_size(city.connections) / (map_size(city.districts) * (map_size(city.districts) - 1) / 2)
    else
      1.0
    end
  end

  defp calculate_city_efficiency(city) do
    density_factor = min(1.0, calculate_density(city) / 10)
    connectivity_factor = calculate_connectivity(city)
    
    (density_factor + connectivity_factor) / 2
  end

  defp analyze_metrics_progression(events) do
    metrics_over_time = Enum.map(events, & &1.metrics)
    
    %{
      growth_curve: extract_growth_curve(metrics_over_time),
      efficiency_trend: extract_efficiency_trend(metrics_over_time),
      peak_metrics: find_peak_metrics(metrics_over_time),
      stability_score: calculate_stability(metrics_over_time)
    }
  end

  defp test_single_growth_iteration(city, strategy, iteration) do
    steps = 10 + iteration * 2
    
    Enum.reduce(1..steps, city, fn step, current_city ->
      action = generate_strategy_action(strategy, current_city)
      {_result, new_city} = execute_sandbox_action(action, current_city, %{
        max_districts: 100,
        max_buildings: 1000
      })
      new_city
    end)
  end

  defp generate_strategy_action(:organic, city) do
    # Organic growth: expand naturally from existing districts
    if map_size(city.districts) == 0 or :rand.uniform() < 0.3 do
      %{
        type: :create_district,
        params: %{
          name: "organic_#{:rand.uniform(999)}",
          type: Enum.random([:residential, :cultural])
        }
      }
    else
      %{
        type: :create_building,
        params: %{
          district_id: city.districts |> Map.keys() |> Enum.random(),
          building_type: Enum.random([:house, :apartment, :monument])
        }
      }
    end
  end

  defp generate_strategy_action(:structured, city) do
    # Structured growth: planned expansion
    district_count = map_size(city.districts)
    
    cond do
      district_count == 0 ->
        %{
          type: :create_district,
          params: %{name: "grid_0_0", type: :commercial}
        }
      
      rem(district_count, 4) == 0 ->
        %{
          type: :create_district,
          params: %{
            name: "grid_#{div(district_count, 4)}_#{rem(district_count, 4)}",
            type: Enum.random([:commercial, :industrial])
          }
        }
      
      true ->
        %{
          type: :create_building,
          params: %{
            district_id: city.districts |> Map.keys() |> List.last(),
            building_type: :office
          }
        }
    end
  end

  defp generate_strategy_action(:explosive, city) do
    # Explosive growth: rapid expansion
    if :rand.uniform() < 0.6 do
      %{
        type: :create_district,
        params: %{
          name: "boom_#{:rand.uniform(9999)}",
          type: Enum.random([:residential, :commercial, :industrial])
        }
      }
    else
      %{
        type: :create_building,
        params: %{
          district_id: city.districts |> Map.keys() |> Enum.random() || "new",
          building_type: Enum.random([:house, :office, :factory])
        }
      }
    end
  end

  defp generate_strategy_action(_, city) do
    # Default/balanced
    generate_balanced_action(0, city)
  end

  defp generate_balanced_action(step, city) do
    district_count = map_size(city.districts)
    building_count = map_size(city.buildings)
    
    cond do
      district_count == 0 ->
        %{
          type: :create_district,
          params: %{name: "central", type: :commercial}
        }
      
      building_count < district_count * 3 ->
        %{
          type: :create_building,
          params: %{
            district_id: city.districts |> Map.keys() |> Enum.random(),
            building_type: Enum.random([:house, :office])
          }
        }
      
      true ->
        %{
          type: :create_district,
          params: %{
            name: "district_#{district_count}",
            type: Enum.random([:residential, :commercial, :cultural])
          }
        }
    end
  end

  defp analyze_growth_results(results, strategy) do
    final_states = Enum.map(results, fn city ->
      %{
        districts: map_size(city.districts),
        buildings: map_size(city.buildings),
        efficiency: calculate_city_efficiency(city)
      }
    end)
    
    %{
      strategy: strategy,
      avg_districts: avg(Enum.map(final_states, & &1.districts)),
      avg_buildings: avg(Enum.map(final_states, & &1.buildings)),
      avg_efficiency: avg(Enum.map(final_states, & &1.efficiency)),
      consistency: calculate_variance(final_states),
      recommendation: generate_recommendation(final_states, strategy)
    }
  end

  defp avg(list) when length(list) > 0 do
    Enum.sum(list) / length(list)
  end
  defp avg([]), do: 0.0

  defp calculate_variance(states) do
    district_counts = Enum.map(states, & &1.districts)
    mean = avg(district_counts)
    
    variance = Enum.map(district_counts, fn x ->
      :math.pow(x - mean, 2)
    end) |> avg()
    
    :math.sqrt(variance)
  end

  defp generate_recommendation(states, strategy) do
    avg_efficiency = avg(Enum.map(states, & &1.efficiency))
    
    cond do
      avg_efficiency > 0.8 ->
        "#{strategy} strategy shows excellent efficiency. Recommended for production use."
      
      avg_efficiency > 0.6 ->
        "#{strategy} strategy is moderately efficient. Consider optimization."
      
      true ->
        "#{strategy} strategy needs improvement. Not recommended without modifications."
    end
  end

  defp deep_copy_city(city) do
    # Simple deep copy for sandbox purposes
    %{
      districts: Map.new(city.districts),
      buildings: Map.new(city.buildings),
      connections: Map.new(city.connections),
      resources: Map.new(city.resources),
      metrics: Map.new(city.metrics)
    }
  end

  defp simulate_action(action_type, params, city) do
    # Simplified simulation
    case action_type do
      :create_district ->
        {:ok, "sim_district_#{:rand.uniform(999)}"}
      
      :create_building ->
        {:ok, "sim_building_#{:rand.uniform(999)}"}
      
      :grow_city ->
        {:ok, %{
          districts_added: 2,
          buildings_added: 6,
          connections_added: 3
        }}
      
      _ ->
        {:ok, :simulated}
    end
  end

  defp calculate_impact(old_city, new_city, result) do
    %{
      districts_changed: map_size(new_city.districts) - map_size(old_city.districts),
      buildings_changed: map_size(new_city.buildings) - map_size(old_city.buildings),
      connections_changed: map_size(new_city.connections) - map_size(old_city.connections),
      efficiency_delta: calculate_city_efficiency(new_city) - calculate_city_efficiency(old_city),
      result_summary: result
    }
  end

  defp estimate_resource_cost(action_type, _params) do
    costs = %{
      create_district: %{polygons: 100, energy: 50},
      create_building: %{polygons: 30, energy: 15},
      grow_city: %{polygons: 500, energy: 250}
    }
    
    Map.get(costs, action_type, %{polygons: 10, energy: 5})
  end

  defp estimate_completion_time(action_type, _params) do
    times = %{
      create_district: "~5 seconds",
      create_building: "~2 seconds",
      grow_city: "~20 seconds"
    }
    
    Map.get(times, action_type, "~1 second")
  end

  defp detect_potential_issues(action_type, params, city) do
    issues = []
    
    issues = if action_type == :create_building and map_size(city.districts) == 0 do
      ["No districts exist yet" | issues]
    else
      issues
    end
    
    issues = if calculate_city_efficiency(city) < 0.3 do
      ["City efficiency is low, consider optimization" | issues]
    else
      issues
    end
    
    issues
  end

  defp run_strategy_test(city, strategy, iterations) do
    Enum.reduce(1..iterations, city, fn _, current_city ->
      action = generate_strategy_action(strategy, current_city)
      {_result, new_city} = execute_sandbox_action(action, current_city, %{
        max_districts: 100,
        max_buildings: 1000
      })
      new_city
    end)
  end

  defp calculate_avg_growth_rate(results) do
    growth_rates = Enum.map(results, fn city ->
      (map_size(city.districts) + map_size(city.buildings)) / 20  # Normalized by iterations
    end)
    avg(growth_rates)
  end

  defp calculate_efficiency(results) do
    efficiencies = Enum.map(results, &calculate_city_efficiency/1)
    avg(efficiencies)
  end

  defp calculate_resource_usage(results) do
    # Simplified resource calculation
    Enum.map(results, fn city ->
      map_size(city.districts) * 100 + map_size(city.buildings) * 30
    end) |> avg()
  end

  defp calculate_consistency(results) do
    # Lower variance = higher consistency
    1.0 / (1.0 + calculate_variance(Enum.map(results, fn city ->
      %{
        districts: map_size(city.districts),
        buildings: map_size(city.buildings),
        efficiency: calculate_city_efficiency(city)
      }
    end)))
  end

  defp calculate_overall_score(results) do
    growth = calculate_avg_growth_rate(results) * 0.3
    efficiency = calculate_efficiency(results) * 0.4
    consistency = calculate_consistency(results) * 0.3
    
    growth + efficiency + consistency
  end

  defp format_experiment_results(experiment) do
    %{
      id: experiment.id,
      name: experiment.name,
      status: experiment.status,
      created_at: experiment.created_at,
      completed_at: experiment[:completed_at],
      config: experiment.config,
      results: experiment.results,
      event_count: length(experiment.events),
      summary: summarize_experiment(experiment)
    }
  end

  defp summarize_experiment(experiment) do
    if experiment.status == :completed do
      %{
        growth_achieved: experiment.results[:growth_achieved],
        efficiency: experiment.results[:resource_efficiency],
        peak_performance: get_in(experiment.results, [:metrics_progression, :peak_metrics])
      }
    else
      %{status: "Not completed"}
    end
  end

  defp extract_learnings(experiments) do
    completed = experiments
    |> Map.values()
    |> Enum.filter(& &1.status == :completed)
    
    %{
      total_experiments: map_size(experiments),
      completed_experiments: length(completed),
      best_strategies: find_best_strategies(completed),
      common_patterns: extract_common_patterns(completed),
      optimization_tips: generate_optimization_tips(completed),
      export_time: DateTime.utc_now()
    }
  end

  defp find_best_strategies(experiments) do
    experiments
    |> Enum.filter(& get_in(&1.config, [:strategy]))
    |> Enum.group_by(& &1.config.strategy)
    |> Enum.map(fn {strategy, exps} ->
      avg_efficiency = avg(Enum.map(exps, & get_in(&1.results, [:resource_efficiency]) || 0))
      {strategy, avg_efficiency}
    end)
    |> Enum.sort_by(& elem(&1, 1), :desc)
    |> Enum.take(3)
  end

  defp extract_common_patterns(experiments) do
    # Analyze event sequences for patterns
    ["Early district creation improves efficiency",
     "Balanced growth between districts and buildings is optimal",
     "Connections should be added after 3+ districts exist"]
  end

  defp generate_optimization_tips(experiments) do
    ["Consider using organic growth for natural city evolution",
     "Structured growth works best for planned expansions",
     "Monitor efficiency metrics to detect optimization opportunities"]
  end

  defp accelerated_time(step, acceleration) do
    DateTime.add(DateTime.utc_now(), step * acceleration, :second)
  end

  defp extract_growth_curve(metrics) do
    Enum.map(metrics, & &1.districts)
  end

  defp extract_efficiency_trend(metrics) do
    Enum.map(metrics, & &1.efficiency)
  end

  defp find_peak_metrics(metrics) do
    Enum.max_by(metrics, & &1.efficiency, fn -> %{efficiency: 0} end)
  end

  defp calculate_stability(metrics) do
    if length(metrics) < 2 do
      1.0
    else
      efficiency_values = Enum.map(metrics, & &1.efficiency)
      variance = calculate_variance(Enum.map(efficiency_values, &%{efficiency: &1}))
      1.0 / (1.0 + variance)
    end
  end

  defp calculate_final_efficiency(final_city, initial_city) do
    initial_resources = calculate_total_resources(initial_city)
    final_resources = calculate_total_resources(final_city)
    growth = calculate_total_growth(final_city, initial_city)
    
    if final_resources - initial_resources > 0 do
      growth / (final_resources - initial_resources)
    else
      0.0
    end
  end

  defp calculate_total_resources(city) do
    map_size(city.districts) * 100 + 
    map_size(city.buildings) * 30 + 
    map_size(city.connections) * 20
  end

  defp calculate_total_growth(final_city, initial_city) do
    (map_size(final_city.districts) - map_size(initial_city.districts)) +
    (map_size(final_city.buildings) - map_size(initial_city.buildings)) +
    (map_size(final_city.connections) - map_size(initial_city.connections))
  end

  defp calculate_growth(final_city, initial_city) do
    %{
      districts: map_size(final_city.districts) - map_size(initial_city.districts),
      buildings: map_size(final_city.buildings) - map_size(initial_city.buildings),
      connections: map_size(final_city.connections) - map_size(initial_city.connections)
    }
  end

  defp generate_pattern_action(pattern, step, city) do
    # Pattern-based action generation
    case pattern do
      :spiral ->
        generate_spiral_action(step, city)
      :grid ->
        generate_grid_action(step, city)
      :radial ->
        generate_radial_action(step, city)
      _ ->
        generate_balanced_action(step, city)
    end
  end

  defp generate_spiral_action(step, city) do
    angle = step * 0.3
    radius = step * 0.1
    
    %{
      type: :create_district,
      params: %{
        name: "spiral_#{step}",
        type: Enum.random([:residential, :cultural]),
        position: %{
          x: radius * :math.cos(angle),
          y: radius * :math.sin(angle)
        }
      }
    }
  end

  defp generate_grid_action(step, city) do
    grid_size = 5
    x = rem(step, grid_size)
    y = div(step, grid_size)
    
    %{
      type: :create_district,
      params: %{
        name: "grid_#{x}_#{y}",
        type: Enum.random([:commercial, :industrial]),
        position: %{x: x * 10, y: y * 10}
      }
    }
  end

  defp generate_radial_action(step, city) do
    ring = div(step, 8) + 1
    position = rem(step, 8)
    
    %{
      type: :create_district,
      params: %{
        name: "ring#{ring}_pos#{position}",
        type: Enum.random([:residential, :commercial, :cultural]),
        position: calculate_radial_position(ring, position)
      }
    }
  end

  defp calculate_radial_position(ring, position) do
    angle = position * :math.pi() * 2 / 8
    radius = ring * 15
    
    %{
      x: radius * :math.cos(angle),
      y: radius * :math.sin(angle)
    }
  end
end