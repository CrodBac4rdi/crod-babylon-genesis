defmodule Crod.Parasite.Interpreter do
  @moduledoc """
  CROD Parasite: The human-LLM interpreter.
  Translates human intentions into LLM-understandable formats and manages context.
  """

  use GenServer
  require Logger

  alias Crod.Services.NatsClient
  alias Crod.Parasite.{Context, Memory, Translator}

  @interpreter_topic "crod.parasite.interpreter"

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    # Subscribe to NATS topics
    NatsClient.subscribe(@interpreter_topic, self())
    
    state = %{
      contexts: %{},
      active_sessions: %{},
      memory_store: Memory.new()
    }
    
    {:ok, state}
  end

  # Public API

  @doc """
  Interprets a human message and returns an LLM-ready format.
  """
  def interpret(message, session_id \\ generate_session_id()) do
    GenServer.call(__MODULE__, {:interpret, message, session_id})
  end

  @doc """
  Processes an LLM response and translates it back to human-readable format.
  """
  def humanize(llm_response, session_id) do
    GenServer.call(__MODULE__, {:humanize, llm_response, session_id})
  end

  @doc """
  Gets the current context for a session.
  """
  def get_context(session_id) do
    GenServer.call(__MODULE__, {:get_context, session_id})
  end

  # GenServer callbacks

  @impl true
  def handle_call({:interpret, message, session_id}, _from, state) do
    # Get or create context
    context = Map.get(state.contexts, session_id, Context.new(session_id))
    
    # Update context with new message
    context = Context.add_human_message(context, message)
    
    # Translate to LLM format
    llm_request = Translator.human_to_llm(message, context)
    
    # Store in memory
    memory_store = Memory.store(state.memory_store, session_id, :human, message)
    
    # Update state
    new_state = %{state | 
      contexts: Map.put(state.contexts, session_id, context),
      memory_store: memory_store
    }
    
    # Publish to NATS for other services
    NatsClient.publish("crod.parasite.interpreted", %{
      session_id: session_id,
      original: message,
      llm_request: llm_request
    })
    
    {:reply, {:ok, llm_request}, new_state}
  end

  @impl true
  def handle_call({:humanize, llm_response, session_id}, _from, state) do
    context = Map.get(state.contexts, session_id, Context.new(session_id))
    
    # Translate LLM response to human format
    human_response = Translator.llm_to_human(llm_response, context)
    
    # Update context
    context = Context.add_llm_response(context, llm_response, human_response)
    
    # Store in memory
    memory_store = Memory.store(state.memory_store, session_id, :llm, llm_response)
    
    # Update state
    new_state = %{state | 
      contexts: Map.put(state.contexts, session_id, context),
      memory_store: memory_store
    }
    
    {:reply, {:ok, human_response}, new_state}
  end

  @impl true
  def handle_call({:get_context, session_id}, _from, state) do
    context = Map.get(state.contexts, session_id, Context.new(session_id))
    {:reply, {:ok, context}, state}
  end

  @impl true
  def handle_info({:nats_message, topic, message}, state) do
    Logger.info("Received message on topic #{topic}: #{inspect(message)}")
    # Handle NATS messages here
    {:noreply, state}
  end

  # Private functions

  defp generate_session_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end
end