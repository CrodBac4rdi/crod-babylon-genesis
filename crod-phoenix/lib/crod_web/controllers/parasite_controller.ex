defmodule CrodWeb.ParasiteController do
  use CrodWeb, :controller

  alias Crod.Parasite.Interpreter

  action_fallback CrodWeb.FallbackController

  def interpret(conn, %{"message" => message} = params) do
    session_id = params["session_id"] || generate_session_id()
    
    with {:ok, llm_request} <- Interpreter.interpret(message, session_id) do
      conn
      |> put_status(:ok)
      |> json(%{
        session_id: session_id,
        llm_request: llm_request,
        status: "interpreted"
      })
    end
  end

  def humanize(conn, %{"llm_response" => llm_response, "session_id" => session_id}) do
    with {:ok, human_response} <- Interpreter.humanize(llm_response, session_id) do
      conn
      |> put_status(:ok)
      |> json(%{
        session_id: session_id,
        human_response: human_response,
        status: "humanized"
      })
    end
  end

  def get_context(conn, %{"session_id" => session_id}) do
    with {:ok, context} <- Interpreter.get_context(session_id) do
      conn
      |> put_status(:ok)
      |> json(%{
        session_id: session_id,
        context: serialize_context(context),
        status: "success"
      })
    end
  end

  defp generate_session_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end

  defp serialize_context(context) do
    %{
      session_id: context.session_id,
      created_at: context.created_at,
      updated_at: context.updated_at,
      message_count: length(context.messages),
      recent_messages: Enum.take(context.messages, -5),
      metadata: context.metadata
    }
  end
end