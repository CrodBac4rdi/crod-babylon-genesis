defmodule Crod.Parasite.Translator do
  @moduledoc """
  Translates between human and LLM formats.
  Core component of the CROD Parasite interpreter.
  """

  alias Crod.Parasite.Context

  @doc """
  Translates a human message into an LLM-ready format.
  """
  def human_to_llm(message, context) do
    %{
      messages: build_llm_messages(message, context),
      system_prompt: build_system_prompt(context),
      parameters: %{
        temperature: determine_temperature(message, context),
        max_tokens: determine_max_tokens(message),
        model: select_model(message, context)
      },
      metadata: %{
        session_id: context.session_id,
        timestamp: DateTime.utc_now(),
        intent: analyze_intent(message)
      }
    }
  end

  @doc """
  Translates an LLM response into human-readable format.
  """
  def llm_to_human(llm_response, context) do
    llm_response
    |> extract_content()
    |> apply_formatting()
    |> add_context_cues(context)
    |> ensure_coherence(context)
  end

  @doc """
  Enhances a prompt with CROD-specific capabilities.
  """
  def enhance_prompt(base_prompt, capabilities \\ []) do
    enhancements = [
      neural_enhancement(capabilities),
      memory_enhancement(capabilities),
      pattern_enhancement(capabilities)
    ]
    
    Enum.reduce(enhancements, base_prompt, fn enhancement, prompt ->
      prompt <> "\n\n" <> enhancement
    end)
  end

  # Private functions

  defp build_llm_messages(message, context) do
    history = Context.get_conversation_history(context, 10)
    history ++ [%{role: "user", content: message}]
  end

  defp build_system_prompt(context) do
    summary = Context.extract_context_summary(context)
    
    """
    You are CROD's AI assistant, integrated through the Parasite interpreter.
    
    Context Summary:
    - Session duration: #{summary.session_duration} seconds
    - Message count: #{summary.message_count}
    - Recent intents: #{inspect(summary.recent_intents)}
    
    Guidelines:
    1. Maintain consistency with previous responses
    2. Be helpful and precise
    3. Adapt your communication style based on the user's patterns
    4. Reference previous context when relevant
    """
  end

  defp determine_temperature(message, context) do
    cond do
      creative_request?(message) -> 0.8
      technical_request?(message) -> 0.3
      length(context.messages) < 3 -> 0.5
      true -> 0.6
    end
  end

  defp determine_max_tokens(message) do
    cond do
      String.contains?(message, ["explain", "describe", "elaborate"]) -> 2000
      String.contains?(message, ["summary", "brief", "quick"]) -> 500
      true -> 1000
    end
  end

  defp select_model(message, context) do
    cond do
      complex_request?(message) -> "claude-3-opus"
      code_related?(message) -> "claude-3-sonnet"
      true -> "claude-3-haiku"
    end
  end

  defp analyze_intent(message) do
    # Enhanced intent analysis
    intents = []
    
    intents = if String.contains?(message, ~w(create build make generate)), 
      do: [:creation | intents], else: intents
    
    intents = if String.contains?(message, ~w(help assist support guide)), 
      do: [:assistance | intents], else: intents
    
    intents = if String.contains?(message, ~w(analyze explain understand interpret)), 
      do: [:analysis | intents], else: intents
    
    intents = if String.contains?(message, ~w(fix debug solve troubleshoot)), 
      do: [:debugging | intents], else: intents
    
    if intents == [], do: [:general], else: intents
  end

  defp extract_content(llm_response) do
    case llm_response do
      %{"content" => content} -> content
      %{"choices" => [%{"message" => %{"content" => content}} | _]} -> content
      content when is_binary(content) -> content
      _ -> "I encountered an error processing the response."
    end
  end

  defp apply_formatting(content) do
    content
    |> String.replace(~r/```(\w+)/, "\n**Code (\1):**\n```")
    |> String.replace(~r/\*\*(.*?)\*\*/, "**\1**")
    |> ensure_proper_line_breaks()
  end

  defp add_context_cues(content, context) do
    if should_add_continuation_cue?(context) do
      content <> "\n\n*Is there anything specific about this you'd like me to elaborate on?*"
    else
      content
    end
  end

  defp ensure_coherence(content, context) do
    # Check for consistency with previous responses
    if contradicts_previous?(content, context) do
      content <> "\n\n*Note: This information updates my previous response based on new context.*"
    else
      content
    end
  end

  defp neural_enhancement(_capabilities) do
    "Enhanced with CROD neural network capabilities for pattern recognition and learning."
  end

  defp memory_enhancement(_capabilities) do
    "Integrated with CROD memory systems for context persistence and recall."
  end

  defp pattern_enhancement(_capabilities) do
    "Utilizing CROD pattern detection for improved understanding and response generation."
  end

  defp creative_request?(message) do
    String.contains?(String.downcase(message), ~w(create imagine design brainstorm))
  end

  defp technical_request?(message) do
    String.contains?(String.downcase(message), ~w(code debug api function algorithm))
  end

  defp complex_request?(message) do
    String.length(message) > 200 or String.contains?(message, ~w(complex elaborate detailed))
  end

  defp code_related?(message) do
    String.contains?(String.downcase(message), ~w(code function class method programming))
  end

  defp ensure_proper_line_breaks(content) do
    content
    |> String.replace(~r/\n{3,}/, "\n\n")
    |> String.replace(~r/([.!?])\s+/, "\\1\n\n")
  end

  defp should_add_continuation_cue?(context) do
    length(context.messages) < 3
  end

  defp contradicts_previous?(_content, _context) do
    # Placeholder for contradiction detection
    false
  end
end