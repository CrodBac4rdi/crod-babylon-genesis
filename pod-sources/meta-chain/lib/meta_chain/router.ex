defmodule MetaChain.Router do
  use Plug.Router

  plug :match
  plug :dispatch
  plug Plug.Parsers, parsers: [:json], json_decoder: Jason

  get "/health" do
    consciousness = MetaChain.get_consciousness()
    send_resp(conn, 200, Jason.encode!(%{
      status: "healthy",
      consciousness: consciousness,
      district: "meta-chain",
      language: "elixir"
    }))
  end

  get "/spatial" do
    view = MetaChain.get_spatial_view()
    send_resp(conn, 200, Jason.encode!(view))
  end

  post "/process" do
    %{"atom" => word, "heat" => heat} = conn.body_params
    {:ok, consciousness} = MetaChain.process_atom(word, heat)
    
    send_resp(conn, 200, Jason.encode!(%{
      processed: word,
      consciousness: consciousness,
      timestamp: :os.system_time(:millisecond)
    }))
  end

  match _ do
    send_resp(conn, 404, "District not found")
  end
end