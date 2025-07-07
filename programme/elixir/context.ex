defmodule Crod.Parasite.Context do
  @moduledoc """
  Manages conversation context for the CROD Parasite interpreter.
  """

  defstruct [
    :session_id,
    :created_at,
    :updated_at,
    :messages,
    :metadata,
    :intent_stack,
    :memory_references
  ]

  @doc """
  Creates a new context for a session.
  """
  def new(session_id) do
    %__MODULE__{
      session_id: session_id,
      created_at: DateTime.utc_now(),
      updated_at: DateTime.utc_now(),
      messages: [],
      metadata: %{},
      intent_stack: [],
      memory_references: []
    }
  end

  @doc """
  Adds a human message to the context.
  """
  def add_human_message(context, message) do
    message_entry = %{
      type: :human,
      content: message,
      timestamp: DateTime.utc_now(),
      intents: extract_intents(message)
    }
    
    %{context | 
      messages: context.messages ++ [message_entry],
      updated_at: DateTime.utc_now()
    }
  end

  @doc """
  Adds an LLM response to the context.
  """
  def add_llm_response(context, llm_response, human_response) do
    response_entry = %{
      type: :llm,
      llm_content: llm_response,
      human_content: human_response,
      timestamp: DateTime.utc_now()
    }
    
    %{context | 
      messages: context.messages ++ [response_entry],
      updated_at: DateTime.utc_now()
    }
  end

  @doc """
  Gets the conversation history in a format suitable for LLMs.
  """
  def get_conversation_history(context, limit \\ 10) do
    context.messages
    |> Enum.take(-limit)
    |> Enum.map(&format_message_for_llm/1)
  end

  @doc """
  Extracts key information from the context for decision making.
  """
  def extract_context_summary(context) do
    %{
      session_duration: DateTime.diff(DateTime.utc_now(), context.created_at),
      message_count: length(context.messages),
      recent_intents: get_recent_intents(context, 5),
      dominant_topics: analyze_topics(context)
    }
  end

  # Private functions

  defp extract_intents(message) do
    # Simple intent extraction - can be enhanced with NLP
    cond do
      String.contains?(message, ["help", "assist", "support"]) -> [:help_request]
      String.contains?(message, ["create", "make", "build"]) -> [:creation_request]
      String.contains?(message, ["analyze", "explain", "understand"]) -> [:analysis_request]
      String.contains?(message, ["fix", "debug", "solve"]) -> [:problem_solving]
      true -> [:general_conversation]
    end
  end

  defp format_message_for_llm(%{type: :human, content: content}) do
    %{role: "user", content: content}
  end

  defp format_message_for_llm(%{type: :llm, llm_content: content}) do
    %{role: "assistant", content: content}
  end

  defp get_recent_intents(context, limit) do
    context.messages
    |> Enum.filter(&(&1.type == :human))
    |> Enum.take(-limit)
    |> Enum.flat_map(&(&1[:intents] || []))
    |> Enum.uniq()
  end

  defp analyze_topics(context) do
    # Placeholder for topic analysis
    # Could integrate with NLP services
    [:general]
  end
end