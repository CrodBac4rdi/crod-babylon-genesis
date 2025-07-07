defmodule CROD.Repo do
  use Ecto.Repo,
    otp_app: :crod_orchestrator,
    adapter: Ecto.Adapters.Postgres
end