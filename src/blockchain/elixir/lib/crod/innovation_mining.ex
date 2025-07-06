defmodule CROD.InnovationMining do
  @moduledoc """
  Innovation-based Mining for CROD Blockchain
  Only truly innovative creations deserve new blocks!
  """
  
  use GenServer
  require Logger
  
  @min_innovation_score 0.7
  
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    {:ok, %{
      patterns: [],
      efficiency: 1.0,
      mined_count: 0
    }}
  end
  
  def should_mine_block?(creation) do
    GenServer.call(__MODULE__, {:check_innovation, creation})
  end
  
  def get_efficiency_score do
    GenServer.call(__MODULE__, :get_efficiency)
  end
  
  def handle_call({:check_innovation, creation}, _from, state) do
    # Simple innovation check for now
    score = calculate_innovation(creation, state.patterns)
    should_mine = score >= @min_innovation_score
    
    new_state = if should_mine do
      %{state | 
        patterns: [creation | state.patterns],
        efficiency: state.efficiency * 1.01,
        mined_count: state.mined_count + 1
      }
    else
      %{state | efficiency: state.efficiency * 0.99}
    end
    
    {:reply, {should_mine, score}, new_state}
  end
  
  def handle_call(:get_efficiency, _from, state) do
    {:reply, state.efficiency, state}
  end
  
  defp calculate_innovation(creation, existing_patterns) do
    # Basic innovation scoring
    base_score = 0.5
    
    # Check if type is new
    type_bonus = if Enum.any?(existing_patterns, &(&1["type"] == creation["type"])) do
      0.0
    else
      0.3
    end
    
    # Random factor for demo
    random_bonus = :rand.uniform() * 0.3
    
    base_score + type_bonus + random_bonus
  end
end