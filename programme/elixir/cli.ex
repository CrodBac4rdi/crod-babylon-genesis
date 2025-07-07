defmodule CROD.CLI do
  @moduledoc """
  Command Line Interface for CROD - Your trusted polygon city architect!
  
  This provides an interactive CLI where users can communicate with CROD
  and control the polygon city building process.
  """

  alias CROD.{Orchestrator, City, Permission, Delta, Sandbox, EventStore}

  def main(args \\ []) do
    case args do
      ["start"] -> start_interactive()
      ["help"] -> show_help()
      ["version"] -> show_version()
      _ -> start_interactive()
    end
  end

  def start_interactive do
    IO.puts("\n" <> String.duplicate("=", 60))
    IO.puts("🏗️  CROD POLYGON CITY ARCHITECT v1.0")
    IO.puts(String.duplicate("=", 60))
    
    {:ok, intro} = Orchestrator.introduce()
    IO.puts(intro)
    
    IO.puts("\nType 'help' for available commands or 'quit' to exit.\n")
    
    loop()
  end

  defp loop do
    command = IO.gets("CROD> ") |> String.trim()
    
    case parse_command(command) do
      {:quit} ->
        IO.puts("\n👋 Thanks for building with CROD! See you next time, bro!")
        :ok
        
      {:error, reason} ->
        IO.puts("❌ Error: #{reason}")
        loop()
        
      result ->
        handle_result(result)
        loop()
    end
  end

  defp parse_command("quit"), do: {:quit}
  defp parse_command("exit"), do: {:quit}
  defp parse_command("q"), do: {:quit}
  
  defp parse_command("help"), do: show_commands()
  defp parse_command("h"), do: show_commands()
  
  defp parse_command("status"), do: show_status()
  defp parse_command("s"), do: show_status()
  
  defp parse_command("explain"), do: explain_intentions()
  defp parse_command("think"), do: explain_intentions()
  
  defp parse_command("city"), do: show_city()
  defp parse_command("visualize"), do: visualize_city()
  
  defp parse_command("build district " <> rest) do
    [name | type_parts] = String.split(rest, " ")
    type = type_parts |> Enum.join("_") |> String.to_atom()
    build_district(name, type)
  end
  
  defp parse_command("build " <> type) do
    propose_building(String.to_atom(type))
  end
  
  defp parse_command("grow"), do: grow_city(:balanced)
  defp parse_command("grow " <> strategy) do
    grow_city(String.to_atom(strategy))
  end
  
  defp parse_command("sandbox"), do: enter_sandbox()
  defp parse_command("test " <> strategy) do
    test_strategy(String.to_atom(strategy))
  end
  
  defp parse_command("delta"), do: show_delta_status()
  defp parse_command("delta enable " <> feature) do
    enable_feature(String.to_atom(feature))
  end
  defp parse_command("delta disable " <> feature) do
    disable_feature(String.to_atom(feature))
  end
  defp parse_command("delta safe"), do: activate_safe_mode()
  defp parse_command("emergency stop"), do: emergency_stop()
  defp parse_command("resume"), do: resume_operations()
  
  defp parse_command("history"), do: show_history()
  defp parse_command("events " <> type) do
    show_events(String.to_atom(type))
  end
  
  defp parse_command("trust " <> mode) do
    set_trust_mode(String.to_atom(mode))
  end
  
  defp parse_command("approve " <> id), do: approve_permission(id)
  defp parse_command("deny " <> id), do: deny_permission(id)
  
  defp parse_command(unknown) do
    {:error, "Unknown command: '#{unknown}'. Type 'help' for available commands."}
  end

  defp show_commands do
    commands = """
    
    📚 CROD COMMANDS:
    
    🏗️  Building Commands:
      build district <name> <type>  - Create a new district (types: residential, commercial, industrial, cultural)
      build <type>                  - Propose a new building
      grow [strategy]              - Grow the city (strategies: organic, structured, explosive, balanced)
      city                         - Show city statistics
      visualize                    - Display ASCII visualization of your city
    
    🤖 CROD Control:
      status                       - Show CROD's current status
      explain                      - Ask CROD to explain its intentions
      trust <mode>                 - Set trust mode (strict, balanced, relaxed)
    
    🧪 Testing & Experimentation:
      sandbox                      - Enter sandbox mode for experiments
      test <strategy>              - Test a growth strategy
    
    🎛️  Delta Control System:
      delta                        - Show Delta control status
      delta enable <feature>       - Enable a CROD feature
      delta disable <feature>      - Disable a CROD feature
      delta safe                   - Activate safe mode
      emergency stop               - Emergency stop all CROD operations
      resume                       - Resume after emergency stop
    
    📊 History & Events:
      history                      - Show recent permission history
      events <type>                - Show events of specific type
    
    ✅ Permissions:
      approve <id>                 - Approve a pending permission request
      deny <id>                    - Deny a pending permission request
    
    🚪 Exit:
      quit, exit, q                - Exit CROD CLI
    
    💡 Tip: CROD will always ask permission before making changes!
    """
    
    IO.puts(commands)
    {:ok}
  end

  defp show_status do
    case Orchestrator.status() do
      {:ok, status} ->
        IO.puts("\n📊 CROD STATUS REPORT:")
        IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        IO.puts("Status: #{format_status(status.orchestrator_status)}")
        IO.puts("Trust Level: #{format_trust_level(status.trust_level)}")
        IO.puts("\nCity Statistics:")
        IO.puts("  Districts: #{status.city_stats.districts}")
        IO.puts("  Buildings: #{status.city_stats.buildings}")
        IO.puts("  Connections: #{status.city_stats.connections}")
        IO.puts("\nCurrent Activity: #{status.current_activity || "None"}")
        IO.puts("Pending Actions: #{status.pending_actions}")
        IO.puts("\nDelta Status: #{status.delta_restrictions.emergency_stop && "🛑 EMERGENCY STOP" || "✅ Normal"}")
        {:ok}
        
      error ->
        {:error, "Failed to get status: #{inspect(error)}"}
    end
  end

  defp explain_intentions do
    case Orchestrator.explain_intentions() do
      {:ok, explanation} ->
        IO.puts(explanation)
        {:ok}
      error ->
        {:error, "Failed to get explanation: #{inspect(error)}"}
    end
  end

  defp show_city do
    case City.calculate_resources() do
      {:ok, resources} ->
        IO.puts("\n🏙️  CITY RESOURCES:")
        IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        IO.puts("Polygons: #{resources.available_polygons}/#{resources.total_polygons} available")
        IO.puts("Energy: #{resources.energy}")
        IO.puts("Data Flow: #{resources.data_flow}")
        IO.puts("\nStructures:")
        IO.puts("  Districts: #{resources.districts}")
        IO.puts("  Buildings: #{resources.buildings}")
        IO.puts("  Connections: #{resources.connections}")
        {:ok}
      error ->
        {:error, "Failed to get city data: #{inspect(error)}"}
    end
  end

  defp visualize_city do
    case City.visualize_city(:ascii) do
      {:ok, visualization} ->
        IO.puts(visualization)
        {:ok}
      error ->
        {:error, "Failed to visualize: #{inspect(error)}"}
    end
  end

  defp build_district(name, type) do
    IO.puts("\n🏗️  Proposing new district: #{name} (#{type})")
    
    case Orchestrator.build_district(name, type) do
      {:ok, district} ->
        IO.puts("✅ District '#{district.name}' created successfully!")
        IO.puts("   Shape: #{inspect(district.polygon_shape)}")
        IO.puts("   Capacity: #{district.resources.capacity} polygons")
        {:ok}
        
      {:denied, reason} ->
        IO.puts("❌ Permission denied: #{reason}")
        {:ok}
        
      {:pending, id} ->
        IO.puts("⏳ Permission pending (ID: #{id})")
        {:ok}
        
      error ->
        {:error, "Failed to build district: #{inspect(error)}"}
    end
  end

  defp propose_building(type) do
    IO.puts("\n🏗️  Proposing new building of type: #{type}")
    
    # For demo, pick a random district
    case City.list_districts() do
      {:ok, []} ->
        IO.puts("❌ No districts available! Build a district first.")
        {:ok}
        
      {:ok, districts} ->
        district = Enum.random(districts)
        
        case Orchestrator.propose_action(:create_building, %{
          district_id: district.id,
          type: type,
          config: %{}
        }) do
          {:ok, result} ->
            IO.puts("✅ Building created in #{district.name}!")
            {:ok}
            
          {:denied, reason} ->
            IO.puts("❌ Permission denied: #{reason}")
            {:ok}
            
          {:pending, id} ->
            IO.puts("⏳ Permission pending (ID: #{id})")
            {:ok}
        end
        
      error ->
        {:error, "Failed to list districts: #{inspect(error)}"}
    end
  end

  defp grow_city(strategy) do
    IO.puts("\n🌱 Proposing city growth with #{strategy} strategy...")
    
    case Orchestrator.grow_city(strategy) do
      {:ok, result} ->
        IO.puts("✅ City growth completed!")
        IO.puts("   Districts added: #{result.districts_added}")
        IO.puts("   Buildings added: #{result.buildings_added}")
        IO.puts("   Connections added: #{result.connections_added}")
        IO.puts("   Time taken: #{result.duration_ms}ms")
        {:ok}
        
      {:denied, reason} ->
        IO.puts("❌ Permission denied: #{reason}")
        {:ok}
        
      error ->
        {:error, "Growth failed: #{inspect(error)}"}
    end
  end

  defp enter_sandbox do
    IO.puts("\n🧪 SANDBOX MODE")
    IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    IO.puts("Test CROD features without affecting your main city!")
    IO.puts("\nAvailable experiments:")
    IO.puts("1. Test growth strategies")
    IO.puts("2. Compare different approaches")
    IO.puts("3. Preview actions")
    IO.puts("\nUse 'test <strategy>' to run experiments")
    {:ok}
  end

  defp test_strategy(strategy) do
    IO.puts("\n🧪 Testing #{strategy} growth strategy...")
    
    case Sandbox.test_growth_strategy(strategy, 5) do
      {:ok, analysis} ->
        IO.puts("\n📊 STRATEGY ANALYSIS: #{strategy}")
        IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        IO.puts("Average Districts: #{Float.round(analysis.avg_districts, 2)}")
        IO.puts("Average Buildings: #{Float.round(analysis.avg_buildings, 2)}")
        IO.puts("Average Efficiency: #{Float.round(analysis.avg_efficiency * 100, 2)}%")
        IO.puts("Consistency Score: #{Float.round(analysis.consistency, 2)}")
        IO.puts("\n💡 #{analysis.recommendation}")
        {:ok}
        
      error ->
        {:error, "Test failed: #{inspect(error)}"}
    end
  end

  defp show_delta_status do
    case Delta.get_status() do
      {:ok, status} ->
        IO.puts("\n🎛️  DELTA CONTROL STATUS:")
        IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        IO.puts(status.control_summary)
        IO.puts("\nEnabled Features (#{length(status.enabled_features)}):")
        Enum.each(status.enabled_features, fn feature ->
          IO.puts("  ✅ #{feature}")
        end)
        
        if length(status.disabled_features) > 0 do
          IO.puts("\nDisabled Features (#{length(status.disabled_features)}):")
          Enum.each(status.disabled_features, fn feature ->
            IO.puts("  ❌ #{feature}")
          end)
        end
        
        IO.puts("\nActive Limits: #{map_size(status.active_limits)}")
        IO.puts("Override Rules: #{status.override_count}")
        {:ok}
        
      error ->
        {:error, "Failed to get Delta status: #{inspect(error)}"}
    end
  end

  defp enable_feature(feature) do
    case Delta.enable_feature(feature) do
      :ok ->
        IO.puts("✅ Feature '#{feature}' enabled!")
        {:ok}
      {:error, reason} ->
        {:error, "Failed to enable feature: #{reason}"}
    end
  end

  defp disable_feature(feature) do
    case Delta.disable_feature(feature) do
      :ok ->
        IO.puts("✅ Feature '#{feature}' disabled!")
        {:ok}
      {:error, reason} ->
        {:error, "Failed to disable feature: #{reason}"}
    end
  end

  defp activate_safe_mode do
    Delta.safe_mode!()
    IO.puts("✅ Safe mode activated! CROD is now in restricted operation.")
    {:ok}
  end

  defp emergency_stop do
    case Delta.emergency_stop!() do
      :ok ->
        IO.puts("🛑 EMERGENCY STOP ACTIVATED!")
        IO.puts("All CROD operations have been suspended.")
        IO.puts("Use 'resume' to restore normal operations.")
        {:ok}
      error ->
        {:error, "Failed to activate emergency stop: #{inspect(error)}"}
    end
  end

  defp resume_operations do
    case Delta.resume() do
      :ok ->
        IO.puts("✅ Normal operations resumed!")
        {:ok}
      {:error, reason} ->
        {:error, "Failed to resume: #{reason}"}
    end
  end

  defp show_history do
    case Permission.review_history(10) do
      {:ok, history} ->
        IO.puts("\n📜 RECENT PERMISSION HISTORY:")
        IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        if Enum.empty?(history) do
          IO.puts("No permission requests yet.")
        else
          Enum.each(history, fn entry ->
            time = Calendar.strftime(entry.timestamp, "%H:%M:%S")
            icon = if entry.decision == :approved, do: "✅", else: "❌"
            IO.puts("#{time} #{icon} #{entry.action} - #{entry.reason}")
          end)
        end
        {:ok}
        
      error ->
        {:error, "Failed to get history: #{inspect(error)}"}
    end
  end

  defp show_events(type) do
    case EventStore.get_events_by_type(type, 10) do
      {:ok, events} ->
        IO.puts("\n📊 RECENT #{type} EVENTS:")
        IO.puts("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        if Enum.empty?(events) do
          IO.puts("No events of type '#{type}' found.")
        else
          Enum.each(events, fn event ->
            time = Calendar.strftime(event.timestamp, "%H:%M:%S")
            IO.puts("#{time} [##{event.id}] #{inspect(event.payload, pretty: true, limit: 2)}")
          end)
        end
        {:ok}
        
      error ->
        {:error, "Failed to get events: #{inspect(error)}"}
    end
  end

  defp set_trust_mode(mode) do
    case Permission.set_trust_mode(mode) do
      :ok ->
        IO.puts("✅ Trust mode set to: #{mode}")
        {:ok}
      error ->
        {:error, "Failed to set trust mode: #{inspect(error)}"}
    end
  end

  defp approve_permission(id) do
    case Permission.approve(id) do
      :ok ->
        IO.puts("✅ Permission #{id} approved!")
        {:ok}
      error ->
        {:error, "Failed to approve: #{inspect(error)}"}
    end
  end

  defp deny_permission(id) do
    case Permission.deny(id) do
      :ok ->
        IO.puts("❌ Permission #{id} denied!")
        {:ok}
      error ->
        {:error, "Failed to deny: #{inspect(error)}"}
    end
  end

  defp handle_result({:ok}), do: :ok
  defp handle_result({:ok, _}), do: :ok
  defp handle_result({:error, reason}), do: IO.puts("❌ Error: #{reason}")
  defp handle_result(_), do: :ok

  defp format_status(:idle), do: "💤 Idle"
  defp format_status(:active), do: "🚀 Active"
  defp format_status(:thinking), do: "🤔 Thinking"
  defp format_status(status), do: to_string(status)

  defp format_trust_level(:cautious), do: "🟡 Cautious"
  defp format_trust_level(:friendly), do: "🟢 Friendly"
  defp format_trust_level(:trusted), do: "💚 Trusted"
  defp format_trust_level(level), do: to_string(level)

  defp show_version do
    IO.puts("CROD Orchestrator v1.0.0")
    IO.puts("Your trusted polygon city architect 🏗️")
  end
end