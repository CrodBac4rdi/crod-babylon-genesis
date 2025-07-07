defmodule Crod.Repo do
  use Ecto.Repo,
    otp_app: :crod,
    adapter: Ecto.Adapters.Postgres
end