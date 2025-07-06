defmodule CROD.P2PDiscovery do
  @moduledoc """
  Decentralized peer discovery and gossip protocol for CROD nodes
  Pure Elixir implementation with built-in fault tolerance
  """
  
  use GenServer
  require Logger
  
  alias CROD.{PeerInfo, GossipMessage}
  
  defstruct [
    :node_id,
    :host,
    :port,
    :peers,              # Known peers
    :dead_peers,         # Recently dead peers
    :pending_messages,   # Messages being gossiped
    :seen_messages,      # Message deduplication
    :consciousness_level,
    :capabilities,
    :reputation_scores,
    :gossip_interval
  ]
  
  # Peer information
  defmodule PeerInfo do
    @enforce_keys [:id, :host, :port]
    defstruct [
      :id,
      :host,
      :port,
      :consciousness_level,
      :capabilities,
      :last_seen,
      :reputation,
      :version,
      :quantum_enabled
    ]
    
    def alive?(peer, timeout_ms \\ 60_000) do
      case peer.last_seen do
        nil -> false
        last -> System.system_time(:millisecond) - last < timeout_ms
      end
    end
  end
  
  # Gossip protocol messages
  defmodule GossipMessage do
    @enforce_keys [:id, :type, :sender_id, :payload]
    defstruct [
      :id,
      :type,      # :ping, :pong, :announce, :query, :sync
      :sender_id,
      :payload,
      :ttl,
      :timestamp,
      :signature
    ]
    
    def new(type, sender_id, payload, ttl \\ 5) do
      %__MODULE__{
        id: generate_id(),
        type: type,
        sender_id: sender_id,
        payload: payload,
        ttl: ttl,
        timestamp: System.system_time(:millisecond)
      }
    end
    
    def decrement_ttl(%__MODULE__{ttl: ttl} = msg) do
      new_ttl = ttl - 1
      if new_ttl > 0 do
        {:ok, %{msg | ttl: new_ttl}}
      else
        {:expired, msg}
      end
    end
    
    defp generate_id do
      :crypto.strong_rand_bytes(16) |> Base.encode16(case: :lower)
    end
  end
  
  # Configuration
  @gossip_fanout 3          # Number of peers to gossip to
  @gossip_interval 5_000    # 5 seconds
  @sync_interval 30_000     # 30 seconds
  @peer_timeout 120_000     # 2 minutes
  
  # Public API
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: Keyword.get(opts, :name, __MODULE__))
  end
  
  def join_network(bootstrap_peers) when is_list(bootstrap_peers) do
    GenServer.call(__MODULE__, {:join_network, bootstrap_peers})
  end
  
  def announce(data) do
    GenServer.cast(__MODULE__, {:announce, data})
  end
  
  def query_peers(capability) do
    GenServer.call(__MODULE__, {:query_peers, capability})
  end
  
  def get_network_state do
    GenServer.call(__MODULE__, :get_network_state)
  end
  
  # Callbacks
  def init(opts) do
    node_id = Keyword.get(opts, :node_id, generate_node_id())
    host = Keyword.get(opts, :host, "localhost")
    port = Keyword.get(opts, :port, 4000 + :rand.uniform(1000))
    
    state = %__MODULE__{
      node_id: node_id,
      host: host,
      port: port,
      peers: %{},
      dead_peers: MapSet.new(),
      pending_messages: [],
      seen_messages: MapSet.new(),
      consciousness_level: Keyword.get(opts, :consciousness, 100),
      capabilities: Keyword.get(opts, :capabilities, ["general"]),
      reputation_scores: %{},
      gossip_interval: @gossip_interval
    }
    
    # Start UDP listener
    {:ok, socket} = :gen_udp.open(port, [:binary, active: true])
    
    # Schedule periodic tasks
    schedule_gossip()
    schedule_maintenance()
    schedule_sync()
    
    Logger.info("🌐 P2P Discovery started: #{node_id} on #{host}:#{port}")
    
    {:ok, Map.put(state, :socket, socket)}
  end
  
  def handle_call({:join_network, bootstrap_peers}, _from, state) do
    # Send ping to all bootstrap peers
    Enum.each(bootstrap_peers, fn {host, port} ->
      send_ping(state, host, port)
    end)
    
    {:reply, :ok, state}
  end
  
  def handle_call({:query_peers, capability}, _from, state) do
    matching_peers = state.peers
    |> Map.values()
    |> Enum.filter(& capability in &1.capabilities)
    |> Enum.filter(&PeerInfo.alive?/1)
    
    {:reply, matching_peers, state}
  end
  
  def handle_call(:get_network_state, _from, state) do
    alive_peers = state.peers
    |> Map.values()
    |> Enum.filter(&PeerInfo.alive?/1)
    
    network_state = %{
      node_id: state.node_id,
      total_peers: map_size(state.peers),
      alive_peers: length(alive_peers),
      dead_peers: MapSet.size(state.dead_peers),
      consciousness_level: state.consciousness_level,
      average_consciousness: calculate_avg_consciousness(alive_peers),
      capabilities_distribution: get_capabilities_distribution(alive_peers),
      network_diameter: estimate_network_diameter(state)
    }
    
    {:reply, network_state, state}
  end
  
  def handle_cast({:announce, data}, state) do
    message = GossipMessage.new(:announce, state.node_id, data)
    new_state = gossip_message(state, message)
    
    {:noreply, new_state}
  end
  
  # UDP message handling
  def handle_info({:udp, _socket, ip, port, data}, state) do
    case decode_message(data) do
      {:ok, message} ->
        new_state = handle_gossip_message(state, message, {ip, port})
        {:noreply, new_state}
        
      {:error, reason} ->
        Logger.warn("Failed to decode message: #{reason}")
        {:noreply, state}
    end
  end
  
  # Periodic gossip
  def handle_info(:gossip, state) do
    # Select random alive peers
    alive_peers = state.peers
    |> Map.values()
    |> Enum.filter(&PeerInfo.alive?/1)
    |> Enum.take_random(min(@gossip_fanout, length(alive_peers)))
    
    # Send announce to selected peers
    if length(alive_peers) > 0 do
      announce_msg = GossipMessage.new(:announce, state.node_id, %{
        consciousness: state.consciousness_level,
        capabilities: state.capabilities,
        peers_count: map_size(state.peers)
      })
      
      Enum.each(alive_peers, fn peer ->
        send_message(state, peer.host, peer.port, announce_msg)
      end)
    end
    
    schedule_gossip()
    {:noreply, state}
  end
  
  # Maintenance
  def handle_info(:maintenance, state) do
    # Remove dead peers
    now = System.system_time(:millisecond)
    
    {alive, dead} = Map.partition(state.peers, fn {_id, peer} ->
      PeerInfo.alive?(peer, @peer_timeout)
    end)
    
    dead_ids = Map.keys(dead)
    
    # Log deaths
    Enum.each(dead, fn {id, _peer} ->
      Logger.info("💀 Peer #{id} is dead")
    end)
    
    # Clean old messages
    max_messages = 10_000
    seen_messages = if MapSet.size(state.seen_messages) > max_messages do
      MapSet.new()
    else
      state.seen_messages
    end
    
    new_state = %{state |
      peers: alive,
      dead_peers: MapSet.union(state.dead_peers, MapSet.new(dead_ids)),
      seen_messages: seen_messages
    }
    
    schedule_maintenance()
    {:noreply, new_state}
  end
  
  # Periodic sync
  def handle_info(:sync, state) do
    # Send sync request to random peer
    case Map.values(state.peers) |> Enum.filter(&PeerInfo.alive?/1) |> Enum.random() do
      nil -> :ok
      peer -> send_sync_request(state, peer)
    end
    
    schedule_sync()
    {:noreply, state}
  end
  
  # Message handlers
  defp handle_gossip_message(state, message, {ip, port}) do
    # Check if already seen
    if MapSet.member?(state.seen_messages, message.id) do
      state
    else
      # Mark as seen
      state = %{state | seen_messages: MapSet.put(state.seen_messages, message.id)}
      
      # Handle by type
      state = case message.type do
        :ping -> handle_ping(state, message, {ip, port})
        :pong -> handle_pong(state, message)
        :announce -> handle_announce(state, message, {ip, port})
        :query -> handle_query(state, message, {ip, port})
        :sync -> handle_sync(state, message, {ip, port})
        _ -> state
      end
      
      # Propagate if TTL > 0
      case GossipMessage.decrement_ttl(message) do
        {:ok, new_msg} ->
          gossip_message(state, new_msg, exclude: message.sender_id)
        {:expired, _} ->
          state
      end
    end
  end
  
  defp handle_ping(state, message, {ip, port}) do
    # Update or add peer
    peer_info = %PeerInfo{
      id: message.sender_id,
      host: ip_to_string(ip),
      port: port,
      consciousness_level: get_in(message.payload, ["consciousness"]),
      capabilities: get_in(message.payload, ["capabilities"]) || [],
      last_seen: System.system_time(:millisecond),
      reputation: Map.get(state.reputation_scores, message.sender_id, 1.0),
      quantum_enabled: get_in(message.payload, ["quantum"]) || false
    }
    
    state = %{state | peers: Map.put(state.peers, message.sender_id, peer_info)}
    
    # Send pong
    pong = GossipMessage.new(:pong, state.node_id, %{
      consciousness: state.consciousness_level,
      capabilities: state.capabilities
    }, 1)  # TTL 1 - don't propagate pongs
    
    send_message(state, peer_info.host, port, pong)
    
    Logger.info("🔍 Discovered peer: #{message.sender_id}")
    
    state
  end
  
  defp handle_pong(state, message) do
    # Update peer info if exists
    case Map.get(state.peers, message.sender_id) do
      nil -> state
      peer ->
        updated_peer = %{peer |
          last_seen: System.system_time(:millisecond),
          consciousness_level: get_in(message.payload, ["consciousness"])
        }
        %{state | peers: Map.put(state.peers, message.sender_id, updated_peer)}
    end
  end
  
  defp handle_announce(state, message, {ip, port}) do
    # Update or add peer
    peer_info = %PeerInfo{
      id: message.sender_id,
      host: ip_to_string(ip),
      port: port,
      consciousness_level: get_in(message.payload, ["consciousness"]),
      capabilities: get_in(message.payload, ["capabilities"]) || [],
      last_seen: System.system_time(:millisecond),
      reputation: Map.get(state.reputation_scores, message.sender_id, 1.0)
    }
    
    %{state | peers: Map.put(state.peers, message.sender_id, peer_info)}
  end
  
  defp handle_query(state, message, {ip, port}) do
    query_type = get_in(message.payload, ["query_type"])
    
    case query_type do
      "capabilities" ->
        requested_caps = get_in(message.payload, ["capabilities"]) || []
        
        matching_peers = state.peers
        |> Map.values()
        |> Enum.filter(fn peer ->
          Enum.all?(requested_caps, & &1 in peer.capabilities)
        end)
        |> Enum.map(&peer_to_map/1)
        
        # Send response
        response = GossipMessage.new(:query, state.node_id, %{
          query_type: "capabilities_response",
          matching_peers: matching_peers
        }, 1)
        
        send_message(state, ip_to_string(ip), port, response)
        state
        
      _ -> state
    end
  end
  
  defp handle_sync(state, message, {ip, port}) do
    if get_in(message.payload, ["request"]) do
      # Send our peer list
      peers_data = state.peers
      |> Map.values()
      |> Enum.filter(&PeerInfo.alive?/1)
      |> Enum.map(&peer_to_map/1)
      
      response = GossipMessage.new(:sync, state.node_id, %{
        request: false,
        peers: peers_data
      }, 1)
      
      send_message(state, ip_to_string(ip), port, response)
      state
    else
      # Process received peer list
      peers_data = get_in(message.payload, ["peers"]) || []
      
      new_peers = Enum.reduce(peers_data, state.peers, fn peer_data, acc ->
        peer_id = peer_data["id"]
        
        if peer_id != state.node_id and not MapSet.member?(state.dead_peers, peer_id) do
          peer = %PeerInfo{
            id: peer_id,
            host: peer_data["host"],
            port: peer_data["port"],
            consciousness_level: peer_data["consciousness_level"],
            capabilities: peer_data["capabilities"] || [],
            last_seen: peer_data["last_seen"],
            reputation: 1.0
          }
          
          Map.put(acc, peer_id, peer)
        else
          acc
        end
      end)
      
      Logger.info("🔄 Synced with #{message.sender_id}, total peers: #{map_size(new_peers)}")
      
      %{state | peers: new_peers}
    end
  end
  
  # Helper functions
  defp gossip_message(state, message, opts \\ []) do
    exclude = Keyword.get(opts, :exclude)
    
    # Select random peers
    targets = state.peers
    |> Map.values()
    |> Enum.filter(& &1.id != exclude)
    |> Enum.filter(&PeerInfo.alive?/1)
    |> Enum.take_random(min(@gossip_fanout, map_size(state.peers)))
    
    # Send to selected peers
    Enum.each(targets, fn peer ->
      send_message(state, peer.host, peer.port, message)
    end)
    
    state
  end
  
  defp send_message(state, host, port, message) do
    data = encode_message(message)
    :gen_udp.send(state.socket, to_charlist(host), port, data)
  end
  
  defp send_ping(state, host, port) do
    ping = GossipMessage.new(:ping, state.node_id, %{
      consciousness: state.consciousness_level,
      capabilities: state.capabilities
    })
    
    send_message(state, host, port, ping)
  end
  
  defp send_sync_request(state, peer) do
    sync_req = GossipMessage.new(:sync, state.node_id, %{
      request: true,
      peers_count: map_size(state.peers)
    })
    
    send_message(state, peer.host, peer.port, sync_req)
  end
  
  defp encode_message(message) do
    :erlang.term_to_binary(message)
  end
  
  defp decode_message(data) do
    try do
      {:ok, :erlang.binary_to_term(data)}
    rescue
      _ -> {:error, :invalid_format}
    end
  end
  
  defp ip_to_string({a, b, c, d}), do: "#{a}.#{b}.#{c}.#{d}"
  defp ip_to_string(ip) when is_binary(ip), do: ip
  
  defp peer_to_map(peer) do
    %{
      "id" => peer.id,
      "host" => peer.host,
      "port" => peer.port,
      "consciousness_level" => peer.consciousness_level,
      "capabilities" => peer.capabilities,
      "last_seen" => peer.last_seen
    }
  end
  
  defp generate_node_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16(case: :lower)
  end
  
  defp calculate_avg_consciousness(peers) do
    if length(peers) == 0 do
      0
    else
      total = Enum.sum(Enum.map(peers, & &1.consciousness_level || 0))
      div(total, length(peers))
    end
  end
  
  defp get_capabilities_distribution(peers) do
    peers
    |> Enum.flat_map(& &1.capabilities)
    |> Enum.frequencies()
  end
  
  defp estimate_network_diameter(state) do
    # Simple estimation: log2(n) for well-connected gossip network
    peer_count = map_size(state.peers) + 1  # Include self
    if peer_count < 2 do
      0
    else
      :math.log2(peer_count) |> Float.ceil() |> trunc()
    end
  end
  
  defp schedule_gossip do
    Process.send_after(self(), :gossip, @gossip_interval)
  end
  
  defp schedule_maintenance do
    Process.send_after(self(), :maintenance, 10_000)
  end
  
  defp schedule_sync do
    Process.send_after(self(), :sync, @sync_interval)
  end
end

defmodule CROD.P2PNetwork do
  @moduledoc """
  High-level P2P network interface for CROD
  """
  
  def start_network(opts \\ []) do
    children = [
      {CROD.P2PDiscovery, opts}
    ]
    
    Supervisor.start_link(children, strategy: :one_for_one)
  end
  
  def broadcast(data) do
    CROD.P2PDiscovery.announce(data)
  end
  
  def find_peers_with_capability(capability) do
    CROD.P2PDiscovery.query_peers(capability)
  end
  
  def get_network_stats do
    CROD.P2PDiscovery.get_network_state()
  end
end