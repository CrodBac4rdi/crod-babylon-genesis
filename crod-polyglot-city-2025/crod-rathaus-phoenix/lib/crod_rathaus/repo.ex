defmodule CrodRathaus.Repo do
  use Ecto.Repo,
    otp_app: :crod_rathaus,
    adapter: Ecto.Adapters.Postgres
end