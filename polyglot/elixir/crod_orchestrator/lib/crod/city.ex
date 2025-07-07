defmodule CROD.City do
  @moduledoc """
  Manages the polygon city structure and districts.
  
  The City is CROD's canvas - a living, growing digital metropolis
  built from polygons and connected by data highways.
  """

  use GenServer
  require Logger

  alias CROD.{EventStore, City.District, City.Building, City.Connection}

  defstruct [
    :districts,
    :buildings,
    :connections,
    :metadata,
    :growth_patterns,
    :resource_pools
  ]

  # Client API

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %__MODULE__{}, name: __MODULE__)
  end

  def create_district(name, type) do
    GenServer.call(__MODULE__, {:create_district, name, type})
  end

  def create_building(district_id, type, config \\ %{}) do
    GenServer.call(__MODULE__, {:create_building, district_id, type, config})
  end

  def connect_districts(from_id, to_id, connection_type \\ :standard) do
    GenServer.call(__MODULE__, {:connect_districts, from_id, to_id, connection_type})
  end

  def get_district(district_id) do
    GenServer.call(__MODULE__, {:get_district, district_id})
  end

  def list_districts do
    GenServer.call(__MODULE__, :list_districts)
  end

  def generate_growth_plan(strategy, current_stats) do
    GenServer.call(__MODULE__, {:generate_growth_plan, strategy, current_stats})
  end

  def visualize_city(format \\ :ascii) do
    GenServer.call(__MODULE__, {:visualize_city, format})
  end

  def calculate_resources do
    GenServer.call(__MODULE__, :calculate_resources)
  end

  # Server Callbacks

  @impl true
  def init(state) do
    {:ok, %{state |
      districts: %{},
      buildings: %{},
      connections: %{},
      metadata: %{
        founded_at: DateTime.utc_now(),
        founder: "CROD",
        theme: "polygon_metropolis"
      },
      growth_patterns: load_growth_patterns(),
      resource_pools: %{
        polygons: 10000,
        energy: 5000,
        data_flow: 1000
      }
    }}
  end

  @impl true
  def handle_call({:create_district, name, type}, _from, state) do
    district_id = generate_district_id(name)
    
    district = %District{
      id: district_id,
      name: name,
      type: type,
      polygon_shape: generate_polygon_shape(type),
      created_at: DateTime.utc_now(),
      buildings: [],
      resources: %{
        capacity: calculate_district_capacity(type),
        used: 0
      },
      attributes: generate_district_attributes(type)
    }
    
    new_districts = Map.put(state.districts, district_id, district)
    new_state = %{state | districts: new_districts}
    
    EventStore.record_event(:district_created, %{
      district_id: district_id,
      name: name,
      type: type
    })
    
    {:reply, {:ok, district}, new_state}
  end

  @impl true
  def handle_call({:create_building, district_id, type, config}, _from, state) do
    case Map.get(state.districts, district_id) do
      nil ->
        {:reply, {:error, :district_not_found}, state}
      
      district ->
        building_id = generate_building_id()
        
        building = %Building{
          id: building_id,
          district_id: district_id,
          type: type,
          polygon_count: calculate_building_polygons(type),
          height: config[:height] || generate_building_height(type),
          config: config,
          created_at: DateTime.utc_now(),
          attributes: generate_building_attributes(type, config)
        }
        
        # Update district with new building
        updated_district = %{district | 
          buildings: [building_id | district.buildings],
          resources: %{district.resources | 
            used: district.resources.used + building.polygon_count
          }
        }
        
        new_buildings = Map.put(state.buildings, building_id, building)
        new_districts = Map.put(state.districts, district_id, updated_district)
        
        new_state = %{state | 
          buildings: new_buildings,
          districts: new_districts
        }
        
        EventStore.record_event(:building_created, %{
          building_id: building_id,
          district_id: district_id,
          type: type
        })
        
        {:reply, {:ok, building}, new_state}
    end
  end

  @impl true
  def handle_call({:connect_districts, from_id, to_id, connection_type}, _from, state) do
    cond do
      not Map.has_key?(state.districts, from_id) ->
        {:reply, {:error, :from_district_not_found}, state}
      
      not Map.has_key?(state.districts, to_id) ->
        {:reply, {:error, :to_district_not_found}, state}
      
      true ->
        connection_id = generate_connection_id(from_id, to_id)
        
        connection = %Connection{
          id: connection_id,
          from_district: from_id,
          to_district: to_id,
          type: connection_type,
          bandwidth: calculate_bandwidth(connection_type),
          polygon_path: generate_connection_path(from_id, to_id, state.districts),
          created_at: DateTime.utc_now(),
          attributes: %{
            bidirectional: true,
            latency_ms: calculate_latency(from_id, to_id, state.districts)
          }
        }
        
        new_connections = Map.put(state.connections, connection_id, connection)
        new_state = %{state | connections: new_connections}
        
        EventStore.record_event(:districts_connected, %{
          connection_id: connection_id,
          from: from_id,
          to: to_id,
          type: connection_type
        })
        
        {:reply, {:ok, connection}, new_state}
    end
  end

  @impl true
  def handle_call({:get_district, district_id}, _from, state) do
    case Map.get(state.districts, district_id) do
      nil -> {:reply, {:error, :not_found}, state}
      district -> {:reply, {:ok, district}, state}
    end
  end

  @impl true
  def handle_call(:list_districts, _from, state) do
    districts = Map.values(state.districts)
    {:reply, {:ok, districts}, state}
  end

  @impl true
  def handle_call({:generate_growth_plan, strategy, current_stats}, _from, state) do
    plan = case strategy do
      :organic ->
        generate_organic_growth(state, current_stats)
      
      :structured ->
        generate_structured_growth(state, current_stats)
      
      :explosive ->
        generate_explosive_growth(state, current_stats)
      
      :balanced ->
        generate_balanced_growth(state, current_stats)
      
      _ ->
        generate_balanced_growth(state, current_stats)
    end
    
    {:reply, plan, state}
  end

  @impl true
  def handle_call({:visualize_city, :ascii}, _from, state) do
    visualization = generate_ascii_visualization(state)
    {:reply, {:ok, visualization}, state}
  end

  @impl true
  def handle_call(:calculate_resources, _from, state) do
    resources = %{
      total_polygons: state.resource_pools.polygons,
      used_polygons: calculate_used_polygons(state),
      available_polygons: state.resource_pools.polygons - calculate_used_polygons(state),
      energy: state.resource_pools.energy,
      data_flow: state.resource_pools.data_flow,
      districts: map_size(state.districts),
      buildings: map_size(state.buildings),
      connections: map_size(state.connections)
    }
    {:reply, {:ok, resources}, state}
  end

  # Private Functions

  defp generate_district_id(name) do
    clean_name = name 
    |> String.downcase() 
    |> String.replace(~r/[^a-z0-9]/, "_")
    "district_#{clean_name}_#{:erlang.phash2(name, 9999)}"
  end

  defp generate_building_id do
    "building_#{:os.system_time(:microsecond)}"
  end

  defp generate_connection_id(from, to) do
    "conn_#{from}_#{to}_#{:os.system_time(:microsecond)}"
  end

  defp generate_polygon_shape(type) do
    base_shapes = %{
      residential: {:hexagon, 6},
      commercial: {:octagon, 8},
      industrial: {:square, 4},
      cultural: {:pentagon, 5},
      tech: {:dodecagon, 12}
    }
    
    Map.get(base_shapes, type, {:hexagon, 6})
  end

  defp calculate_district_capacity(type) do
    capacities = %{
      residential: 500,
      commercial: 800,
      industrial: 1200,
      cultural: 600,
      tech: 1000
    }
    
    Map.get(capacities, type, 600)
  end

  defp generate_district_attributes(type) do
    %{
      population_density: calculate_density(type),
      tech_level: calculate_tech_level(type),
      culture_score: calculate_culture_score(type),
      efficiency: calculate_efficiency(type),
      special_features: generate_special_features(type)
    }
  end

  defp calculate_building_polygons(type) do
    polygon_counts = %{
      house: 10,
      apartment: 25,
      office: 40,
      factory: 60,
      monument: 80,
      datacenter: 100,
      hub: 150
    }
    
    Map.get(polygon_counts, type, 20)
  end

  defp generate_building_height(type) do
    height_ranges = %{
      house: {1, 3},
      apartment: {5, 20},
      office: {10, 50},
      factory: {2, 10},
      monument: {1, 100},
      datacenter: {5, 15},
      hub: {20, 80}
    }
    
    {min, max} = Map.get(height_ranges, type, {1, 10})
    min + :rand.uniform(max - min)
  end

  defp generate_building_attributes(type, config) do
    %{
      function: type,
      efficiency_rating: 0.7 + :rand.uniform() * 0.3,
      polygon_optimization: calculate_optimization(type),
      special_properties: Map.get(config, :special, []),
      connections: []
    }
  end

  defp calculate_bandwidth(type) do
    bandwidths = %{
      standard: 100,
      express: 500,
      quantum: 1000,
      neural: 2000
    }
    
    Map.get(bandwidths, type, 100)
  end

  defp generate_connection_path(from_id, to_id, districts) do
    # Simplified path generation - in reality would use pathfinding
    from = Map.get(districts, from_id)
    to = Map.get(districts, to_id)
    
    [
      %{x: 0, y: 0, district: from_id},
      %{x: 50, y: 50, district: "transit"},
      %{x: 100, y: 100, district: to_id}
    ]
  end

  defp calculate_latency(from_id, to_id, districts) do
    # Simplified latency calculation
    base_latency = 10
    distance_factor = :rand.uniform(5)
    base_latency + distance_factor
  end

  defp load_growth_patterns do
    %{
      organic: %{
        spread_rate: 0.3,
        density_preference: :medium,
        connection_style: :mesh
      },
      structured: %{
        spread_rate: 0.5,
        density_preference: :high,
        connection_style: :grid
      },
      explosive: %{
        spread_rate: 0.8,
        density_preference: :varied,
        connection_style: :hub_spoke
      },
      balanced: %{
        spread_rate: 0.5,
        density_preference: :adaptive,
        connection_style: :hybrid
      }
    }
  end

  defp generate_organic_growth(state, current_stats) do
    %{
      strategy: :organic,
      new_districts: calculate_new_districts(0.3, current_stats),
      new_buildings: calculate_new_buildings(:organic, state),
      new_connections: calculate_new_connections(:mesh, state),
      total_resources: estimate_resources(:organic, state),
      description: "Natural, flowing growth following data currents"
    }
  end

  defp generate_structured_growth(state, current_stats) do
    %{
      strategy: :structured,
      new_districts: calculate_new_districts(0.5, current_stats),
      new_buildings: calculate_new_buildings(:structured, state),
      new_connections: calculate_new_connections(:grid, state),
      total_resources: estimate_resources(:structured, state),
      description: "Organized expansion with clear district boundaries"
    }
  end

  defp generate_explosive_growth(state, current_stats) do
    %{
      strategy: :explosive,
      new_districts: calculate_new_districts(0.8, current_stats),
      new_buildings: calculate_new_buildings(:explosive, state),
      new_connections: calculate_new_connections(:hub_spoke, state),
      total_resources: estimate_resources(:explosive, state),
      description: "Rapid expansion in all directions"
    }
  end

  defp generate_balanced_growth(state, current_stats) do
    %{
      strategy: :balanced,
      new_districts: calculate_new_districts(0.5, current_stats),
      new_buildings: calculate_new_buildings(:balanced, state),
      new_connections: calculate_new_connections(:hybrid, state),
      total_resources: estimate_resources(:balanced, state),
      description: "Thoughtful growth balancing all factors"
    }
  end

  defp calculate_new_districts(rate, current_stats) do
    base = max(1, round(current_stats.districts * rate))
    base + :rand.uniform(2)
  end

  defp calculate_new_buildings(strategy, state) do
    district_count = map_size(state.districts)
    case strategy do
      :organic -> district_count * 3 + :rand.uniform(5)
      :structured -> district_count * 5
      :explosive -> district_count * 8 + :rand.uniform(10)
      :balanced -> district_count * 4 + :rand.uniform(3)
    end
  end

  defp calculate_new_connections(style, state) do
    district_count = map_size(state.districts)
    case style do
      :mesh -> district_count * 2
      :grid -> district_count + 2
      :hub_spoke -> district_count
      :hybrid -> round(district_count * 1.5)
    end
  end

  defp estimate_resources(strategy, _state) do
    base_costs = %{
      organic: 800,
      structured: 1200,
      explosive: 2000,
      balanced: 1000
    }
    
    Map.get(base_costs, strategy, 1000)
  end

  defp calculate_used_polygons(state) do
    building_polygons = state.buildings
    |> Map.values()
    |> Enum.map(& &1.polygon_count)
    |> Enum.sum()
    
    district_polygons = map_size(state.districts) * 100
    connection_polygons = map_size(state.connections) * 20
    
    building_polygons + district_polygons + connection_polygons
  end

  defp generate_ascii_visualization(state) do
    """
    
    🏙️  CROD POLYGON CITY VISUALIZATION
    ═══════════════════════════════════
    
    Districts: #{map_size(state.districts)}
    Buildings: #{map_size(state.buildings)}
    Connections: #{map_size(state.connections)}
    
    #{generate_district_map(state)}
    
    Resource Usage:
    #{generate_resource_bar(state)}
    
    Growth Potential: #{calculate_growth_potential(state)}%
    """
  end

  defp generate_district_map(state) do
    if map_size(state.districts) == 0 do
      "    [No districts yet - build your first!]"
    else
      state.districts
      |> Map.values()
      |> Enum.take(5)
      |> Enum.map(&format_district_ascii/1)
      |> Enum.join("\n")
    end
  end

  defp format_district_ascii(district) do
    shape = case district.polygon_shape do
      {:hexagon, _} -> "⬡"
      {:octagon, _} -> "⬢"
      {:square, _} -> "◼"
      {:pentagon, _} -> "⬟"
      _ -> "●"
    end
    
    building_count = length(district.buildings)
    used_percent = round(district.resources.used / district.resources.capacity * 100)
    
    "    #{shape} #{district.name} (#{district.type}): #{building_count} buildings [#{used_percent}% full]"
  end

  defp generate_resource_bar(state) do
    used = calculate_used_polygons(state)
    total = state.resource_pools.polygons
    percent = round(used / total * 100)
    
    bar_length = 30
    filled = round(bar_length * percent / 100)
    empty = bar_length - filled
    
    bar = String.duplicate("█", filled) <> String.duplicate("░", empty)
    "    Polygons: [#{bar}] #{percent}% (#{used}/#{total})"
  end

  defp calculate_growth_potential(state) do
    used_percent = calculate_used_polygons(state) / state.resource_pools.polygons
    connection_ratio = if map_size(state.districts) > 0,
      do: map_size(state.connections) / map_size(state.districts),
      else: 0
    
    base_potential = (1 - used_percent) * 100
    connection_bonus = min(20, connection_ratio * 10)
    
    round(base_potential + connection_bonus)
  end

  defp calculate_density(:residential), do: :high
  defp calculate_density(:commercial), do: :medium
  defp calculate_density(:industrial), do: :low
  defp calculate_density(_), do: :medium

  defp calculate_tech_level(:tech), do: 10
  defp calculate_tech_level(:commercial), do: 7
  defp calculate_tech_level(:industrial), do: 5
  defp calculate_tech_level(_), do: 3

  defp calculate_culture_score(:cultural), do: 10
  defp calculate_culture_score(:residential), do: 6
  defp calculate_culture_score(:commercial), do: 4
  defp calculate_culture_score(_), do: 2

  defp calculate_efficiency(type) do
    base_efficiency = 0.7
    type_bonus = case type do
      :tech -> 0.2
      :industrial -> 0.15
      :commercial -> 0.1
      _ -> 0.05
    end
    base_efficiency + type_bonus
  end

  defp generate_special_features(:cultural), do: ["art_gallery", "amphitheater"]
  defp generate_special_features(:tech), do: ["quantum_lab", "ai_center"]
  defp generate_special_features(:commercial), do: ["marketplace", "trade_hub"]
  defp generate_special_features(_), do: []

  defp calculate_optimization(:datacenter), do: 0.95
  defp calculate_optimization(:hub), do: 0.9
  defp calculate_optimization(:office), do: 0.85
  defp calculate_optimization(_), do: 0.75
end

# Sub-modules for data structures

defmodule CROD.City.District do
  @moduledoc false
  defstruct [:id, :name, :type, :polygon_shape, :created_at, :buildings, :resources, :attributes]
end

defmodule CROD.City.Building do
  @moduledoc false
  defstruct [:id, :district_id, :type, :polygon_count, :height, :config, :created_at, :attributes]
end

defmodule CROD.City.Connection do
  @moduledoc false
  defstruct [:id, :from_district, :to_district, :type, :bandwidth, :polygon_path, :created_at, :attributes]
end