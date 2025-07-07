defmodule CrodRathaus.Event do
  use Ecto.Schema
  import Ecto.Changeset
  
  @primary_key {:id, :binary_id, autogenerate: true}
  
  schema "events" do
    field :aggregate_id, :string
    field :event_type, :string
    field :event_data, :map
    field :metadata, :map
    field :version, :integer
    field :created_at, :utc_datetime_usec
  end
  
  def changeset(event, attrs) do
    event
    |> cast(attrs, [:aggregate_id, :event_type, :event_data, :metadata, :version, :created_at])
    |> validate_required([:aggregate_id, :event_type, :event_data, :version, :created_at])
    |> unique_constraint([:aggregate_id, :version])
  end
end