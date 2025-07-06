defmodule CROD.InnovationMining do
  @moduledoc """
  Innovation-based Mining System
  Neue Blöcke nur wenn wirklich Neues erschaffen wird!
  """
  
  use GenServer
  require Logger
  
  # Innovation Thresholds
  @min_innovation_score 0.7
  @creativity_multiplier 2.0
  @uniqueness_bonus 3.0
  
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    state = %{
      innovation_pool: [],
      existing_patterns: load_patterns(),
      mined_innovations: 0,
      rejected_duplicates: 0,
      efficiency_score: 1.0
    }
    
    {:ok, state}
  end
  
  # Check if creation deserves a new block
  def should_mine_block?(creation) do
    GenServer.call(__MODULE__, {:check_innovation, creation})
  end
  
  # Submit creation for innovation mining
  def submit_creation(creation) do
    GenServer.call(__MODULE__, {:submit_creation, creation})
  end
  
  # Get network efficiency score
  def get_efficiency_score do
    GenServer.call(__MODULE__, :get_efficiency)
  end
  
  def handle_call({:check_innovation, creation}, _from, state) do
    innovation_score = calculate_innovation_score(creation, state.existing_patterns)
    
    should_mine = innovation_score >= @min_innovation_score
    
    Logger.info("Innovation check: #{creation.type} - Score: #{innovation_score} - Mine: #{should_mine}")
    
    {:reply, {should_mine, innovation_score}, state}
  end
  
  def handle_call({:submit_creation, creation}, _from, state) do
    case analyze_creation(creation, state) do
      {:innovative, score, analysis} ->
        # This deserves a new block!
        new_block = create_innovation_block(creation, score, analysis)
        
        # Update patterns with new innovation
        new_patterns = update_patterns(state.existing_patterns, creation)
        
        # Increase network efficiency
        new_efficiency = state.efficiency_score * (1 + score / 10)
        
        new_state = %{state | 
          existing_patterns: new_patterns,
          mined_innovations: state.mined_innovations + 1,
          efficiency_score: new_efficiency
        }
        
        # Broadcast innovation event
        broadcast_innovation(new_block)
        
        {:reply, {:mined, new_block, new_efficiency}, new_state}
        
      {:duplicate, similarity} ->
        # No new block needed, we have this already
        new_state = %{state | 
          rejected_duplicates: state.rejected_duplicates + 1,
          efficiency_score: state.efficiency_score * 0.99  # Slight penalty
        }
        
        {:reply, {:rejected, "Similar creation exists (#{similarity}% match)"}, new_state}
    end
  end
  
  def handle_call(:get_efficiency, _from, state) do
    {:reply, state.efficiency_score, state}
  end
  
  # Calculate how innovative a creation is
  defp calculate_innovation_score(creation, existing_patterns) do
    base_score = 0.0
    
    # Check uniqueness
    uniqueness = calculate_uniqueness(creation, existing_patterns)
    base_score = base_score + uniqueness * @uniqueness_bonus
    
    # Check creativity metrics
    creativity = analyze_creativity(creation)
    base_score = base_score + creativity * @creativity_multiplier
    
    # Check technical innovation
    technical = analyze_technical_innovation(creation)
    base_score = base_score + technical
    
    # Check cross-domain fusion
    fusion = check_cross_domain_fusion(creation)
    base_score = base_score + fusion * 2
    
    # Normalize to 0-1
    min(base_score / 10, 1.0)
  end
  
  defp analyze_creation(creation, state) do
    # Deep analysis of the creation
    patterns = extract_patterns(creation)
    
    # Compare with existing
    similarities = Enum.map(state.existing_patterns, fn existing ->
      calculate_similarity(patterns, existing)
    end)
    
    max_similarity = Enum.max(similarities, fn -> 0 end)
    
    if max_similarity < 70 do  # Less than 70% similar to anything existing
      score = calculate_innovation_score(creation, state.existing_patterns)
      analysis = %{
        patterns: patterns,
        unique_elements: find_unique_elements(patterns, state.existing_patterns),
        innovation_type: classify_innovation(creation),
        potential_impact: estimate_impact(creation)
      }
      
      {:innovative, score, analysis}
    else
      {:duplicate, max_similarity}
    end
  end
  
  defp create_innovation_block(creation, score, analysis) do
    %{
      type: "innovation_block",
      timestamp: System.os_time(:millisecond),
      creation: creation,
      innovation_score: score,
      analysis: analysis,
      reward: calculate_reward(score),
      efficiency_gain: score * 0.1,
      tags: creation[:tags] || [],
      reviews_required: true
    }
  end
  
  defp calculate_uniqueness(creation, existing_patterns) do
    # Complex uniqueness calculation
    # Returns 0-1 score
    :rand.uniform()  # Placeholder
  end
  
  defp analyze_creativity(creation) do
    # Analyze creative aspects
    # Returns 0-1 score
    case creation.type do
      "game" -> check_game_creativity(creation)
      "3d_model" -> check_3d_creativity(creation)
      "story" -> check_story_creativity(creation)
      "music" -> check_music_creativity(creation)
      _ -> 0.5
    end
  end
  
  defp analyze_technical_innovation(creation) do
    # Check for technical innovations
    features = creation[:technical_features] || []
    
    innovation_points = Enum.reduce(features, 0, fn feature, acc ->
      case feature do
        "new_algorithm" -> acc + 2
        "performance_optimization" -> acc + 1
        "novel_ui_pattern" -> acc + 1.5
        "ai_integration" -> acc + 1
        _ -> acc
      end
    end)
    
    min(innovation_points / 5, 1.0)
  end
  
  defp check_cross_domain_fusion(creation) do
    # Reward creations that combine multiple domains
    domains = creation[:domains] || []
    
    case length(domains) do
      1 -> 0.0
      2 -> 0.3
      3 -> 0.6
      _ -> 0.9
    end
  end
  
  defp calculate_reward(innovation_score) do
    # Reward calculation based on innovation
    base_reward = 100
    innovation_bonus = innovation_score * 1000
    
    base_reward + innovation_bonus
  end
  
  defp broadcast_innovation(block) do
    Phoenix.PubSub.broadcast(CROD.PubSub, "innovations", {:new_innovation, block})
  end
  
  # Placeholder functions
  defp load_patterns, do: []
  defp extract_patterns(_), do: %{}
  defp calculate_similarity(_, _), do: :rand.uniform(100)
  defp update_patterns(patterns, _), do: patterns
  defp find_unique_elements(_, _), do: []
  defp classify_innovation(_), do: "general"
  defp estimate_impact(_), do: "medium"
  defp check_game_creativity(_), do: :rand.uniform()
  defp check_3d_creativity(_), do: :rand.uniform()
  defp check_story_creativity(_), do: :rand.uniform()
  defp check_music_creativity(_), do: :rand.uniform()
end