defmodule CROD.Permission do
  @moduledoc """
  Handles permission requests and user consent for CROD actions.
  
  This module ensures CROD always asks before acting and respects
  user decisions. It's the trust foundation of the CROD system.
  """

  use GenServer
  require Logger

  @permission_timeout 60_000 # 1 minute timeout for permissions

  defstruct [
    :pending_requests,
    :permission_history,
    :auto_approve_rules,
    :auto_deny_rules,
    :trust_mode
  ]

  # Client API

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %__MODULE__{}, name: __MODULE__)
  end

  def request_permission(proposal) do
    GenServer.call(__MODULE__, {:request_permission, proposal}, @permission_timeout)
  end

  def set_auto_approve(action_pattern, conditions \\ %{}) do
    GenServer.call(__MODULE__, {:set_auto_approve, action_pattern, conditions})
  end

  def set_auto_deny(action_pattern, reason) do
    GenServer.call(__MODULE__, {:set_auto_deny, action_pattern, reason})
  end

  def review_history(limit \\ 10) do
    GenServer.call(__MODULE__, {:review_history, limit})
  end

  def set_trust_mode(mode) when mode in [:strict, :balanced, :relaxed] do
    GenServer.call(__MODULE__, {:set_trust_mode, mode})
  end

  # Server Callbacks

  @impl true
  def init(state) do
    {:ok, %{state | 
      pending_requests: %{},
      permission_history: [],
      auto_approve_rules: %{},
      auto_deny_rules: %{},
      trust_mode: :balanced
    }}
  end

  @impl true
  def handle_call({:request_permission, proposal}, from, state) do
    request_id = generate_request_id()
    
    # Check auto-deny rules first
    case check_auto_deny(proposal, state.auto_deny_rules) do
      {:deny, reason} ->
        log_permission_decision(proposal, :denied, reason, state)
        {:reply, {:denied, reason}, state}
      
      :continue ->
        # Check auto-approve rules
        case check_auto_approve(proposal, state.auto_approve_rules, state.trust_mode) do
          {:approve, reason} ->
            log_permission_decision(proposal, :approved, reason, state)
            {:reply, {:approved, reason}, state}
          
          :ask_user ->
            # Present to user and wait for response
            display_permission_request(proposal, request_id)
            
            # Store pending request
            pending = %{
              id: request_id,
              proposal: proposal,
              from: from,
              created_at: DateTime.utc_now()
            }
            
            new_state = %{state | 
              pending_requests: Map.put(state.pending_requests, request_id, pending)
            }
            
            # In a real implementation, this would wait for user input
            # For now, we'll simulate immediate approval in balanced mode
            if state.trust_mode == :balanced and is_safe_action?(proposal.action) do
              {:reply, {:approved, "Auto-approved safe action"}, new_state}
            else
              {:reply, {:deferred, request_id}, new_state}
            end
        end
    end
  end

  @impl true
  def handle_call({:set_auto_approve, pattern, conditions}, _from, state) do
    new_rules = Map.put(state.auto_approve_rules, pattern, conditions)
    {:reply, :ok, %{state | auto_approve_rules: new_rules}}
  end

  @impl true
  def handle_call({:set_auto_deny, pattern, reason}, _from, state) do
    new_rules = Map.put(state.auto_deny_rules, pattern, reason)
    {:reply, :ok, %{state | auto_deny_rules: new_rules}}
  end

  @impl true
  def handle_call({:review_history, limit}, _from, state) do
    recent_history = Enum.take(state.permission_history, limit)
    {:reply, {:ok, recent_history}, state}
  end

  @impl true
  def handle_call({:set_trust_mode, mode}, _from, state) do
    Logger.info("CROD Permission: Trust mode changed to #{mode}")
    {:reply, :ok, %{state | trust_mode: mode}}
  end

  @impl true
  def handle_call({:user_response, request_id, decision, reason}, _from, state) do
    case Map.get(state.pending_requests, request_id) do
      nil ->
        {:reply, {:error, :no_such_request}, state}
      
      pending ->
        # Remove from pending
        new_pending = Map.delete(state.pending_requests, request_id)
        
        # Log the decision
        new_state = %{state | pending_requests: new_pending}
        logged_state = log_permission_decision(
          pending.proposal, 
          decision, 
          reason, 
          new_state
        )
        
        # Reply to original caller
        response = case decision do
          :approved -> {:approved, reason}
          :denied -> {:denied, reason}
        end
        
        GenServer.reply(pending.from, response)
        {:reply, :ok, logged_state}
    end
  end

  # Private Functions

  defp generate_request_id do
    "perm_#{:crypto.strong_rand_bytes(8) |> Base.encode16(case: :lower)}"
  end

  defp check_auto_deny(proposal, rules) do
    Enum.find_value(rules, :continue, fn {pattern, reason} ->
      if matches_pattern?(proposal.action, pattern) do
        {:deny, reason}
      else
        false
      end
    end)
  end

  defp check_auto_approve(proposal, rules, trust_mode) do
    base_approved = Enum.any?(rules, fn {pattern, conditions} ->
      matches_pattern?(proposal.action, pattern) and 
      meets_conditions?(proposal, conditions)
    end)
    
    cond do
      base_approved ->
        {:approve, "Matches auto-approve rule"}
      
      trust_mode == :relaxed and is_safe_action?(proposal.action) ->
        {:approve, "Safe action in relaxed mode"}
      
      trust_mode == :strict ->
        :ask_user
      
      true ->
        :ask_user
    end
  end

  defp matches_pattern?(action, pattern) when is_atom(pattern) do
    action == pattern
  end

  defp matches_pattern?(action, pattern) when is_binary(pattern) do
    action_str = to_string(action)
    String.contains?(action_str, pattern)
  end

  defp meets_conditions?(_proposal, conditions) when map_size(conditions) == 0 do
    true
  end

  defp meets_conditions?(proposal, conditions) do
    Enum.all?(conditions, fn {key, expected} ->
      get_in(proposal, [key]) == expected
    end)
  end

  defp is_safe_action?(action) do
    safe_actions = [
      :status, :explain_intentions, :preview, :estimate,
      :sandbox_test, :simulate, :dry_run
    ]
    action in safe_actions
  end

  defp display_permission_request(proposal, request_id) do
    IO.puts("\n" <> String.duplicate("=", 60))
    IO.puts("🤖 CROD PERMISSION REQUEST ##{request_id}")
    IO.puts(String.duplicate("=", 60))
    IO.puts("\nAction: #{format_action(proposal.action)}")
    IO.puts("Description: #{proposal[:description] || "No description provided"}")
    
    if proposal[:impact] do
      IO.puts("\nPotential Impact:")
      IO.puts(proposal.impact)
    end
    
    if proposal[:resources_needed] do
      IO.puts("\nResources Required:")
      IO.inspect(proposal.resources_needed, pretty: true)
    end
    
    IO.puts("\nReversible: #{if proposal[:reversible], do: "Yes ✓", else: "No ✗"}")
    
    if proposal[:preview] do
      IO.puts("\nPreview:")
      IO.inspect(proposal.preview, pretty: true, limit: 5)
    end
    
    IO.puts("\n" <> String.duplicate("-", 60))
    IO.puts("To approve: CROD.Permission.approve(\"#{request_id}\", \"reason\")")
    IO.puts("To deny: CROD.Permission.deny(\"#{request_id}\", \"reason\")")
    IO.puts(String.duplicate("=", 60) <> "\n")
  end

  defp format_action(action) when is_atom(action) do
    action
    |> to_string()
    |> String.replace("_", " ")
    |> String.split()
    |> Enum.map(&String.capitalize/1)
    |> Enum.join(" ")
  end

  defp format_action(action), do: to_string(action)

  defp log_permission_decision(proposal, decision, reason, state) do
    entry = %{
      timestamp: DateTime.utc_now(),
      action: proposal.action,
      decision: decision,
      reason: reason,
      proposal_summary: summarize_proposal(proposal)
    }
    
    history = [entry | state.permission_history] |> Enum.take(1000) # Keep last 1000
    
    Logger.info("Permission #{decision} for #{proposal.action}: #{reason}")
    
    %{state | permission_history: history}
  end

  defp summarize_proposal(proposal) do
    %{
      action: proposal.action,
      params: proposal[:params],
      impact: proposal[:impact],
      reversible: proposal[:reversible]
    }
  end

  # Public helper functions for CLI

  def approve(request_id, reason \\ "User approved") do
    GenServer.call(__MODULE__, {:user_response, request_id, :approved, reason})
  end

  def deny(request_id, reason \\ "User denied") do
    GenServer.call(__MODULE__, {:user_response, request_id, :denied, reason})
  end
end