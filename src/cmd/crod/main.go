package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
	"time"

	"github.com/fatih/color"
)

var version = "2.0.0"

func main() {
	var (
		quick  = flag.Bool("quick", false, "Quick start (blockchain + GUI)")
		full   = flag.Bool("full", false, "Full blockchain stack")
		dev    = flag.Bool("dev", false, "Development mode")
		status = flag.Bool("status", false, "Show service status")
		stop   = flag.Bool("stop", false, "Stop all services")
		ver    = flag.Bool("version", false, "Show version")
		monitor = flag.Bool("monitor", false, "Start monitoring dashboard")
		visualize = flag.Bool("visualize", false, "Start visualization server")
	)
	
	flag.Parse()
	
	if *ver {
		printVersion()
		return
	}

	// Print banner
	printBanner()
	
	switch {
	case *quick:
		startQuick()
	case *full:
		startFull()
	case *dev:
		startDev()
	case *status:
		showStatus()
	case *stop:
		stopAll()
	case *monitor:
		startMonitor()
	case *visualize:
		startVisualizer()
	default:
		printHelp()
	}
}

func printBanner() {
	banner := color.New(color.FgCyan, color.Bold)
	banner.Println(`
   _____ _____   ____  _____  
  / ____|  __ \ / __ \|  __ \ 
 | |    | |__) | |  | | |  | |
 | |    |  _  /| |  | | |  | |
 | |____| | \ \| |__| | |__| |
  \_____|_|  \_\\____/|_____/ 
                              
  Consciousness Revolution On Demand`)
	fmt.Println()
}

func printVersion() {
	fmt.Printf("CROD Launcher v%s\n", version)
	fmt.Println("Built with Go - No more shell scripts!")
}

func printHelp() {
	help := `Usage: crod [options]

Options:
  --quick      Start blockchain + GUI only
  --full       Start full blockchain stack with all districts
  --dev        Development mode with hot reload
  --status     Show current service status
  --stop       Stop all CROD services
  --monitor    Start service monitoring dashboard
  --visualize  Start CROD visualization server
  --version    Show version information
  --help       Show this help message

Examples:
  crod --quick                 # Quick start
  crod --full                  # Full stack
  crod --monitor               # Monitor services
  crod --visualize             # Start visualizer
`
	fmt.Println(help)
}

func startQuick() {
	fmt.Println("Starting CROD (Quick Mode)...")
	
	// Start blockchain
	color.New(color.FgYellow).Println("→ Starting Blockchain Core...")
	cmd := exec.Command("node", "current/working/blockchain-server.js")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		color.Red("Failed to start blockchain: %v", err)
		return
	}
	
	// Start GUI
	time.Sleep(2 * time.Second)
	color.New(color.FgYellow).Println("→ Starting React GUI...")
	guiCmd := exec.Command("python3", "-m", "http.server", "8080")
	guiCmd.Dir = "current/working/crod-gui"
	if err := guiCmd.Start(); err != nil {
		color.Red("Failed to start GUI: %v", err)
		return
	}
	
	// Success message
	time.Sleep(1 * time.Second)
	color.Green("\n✓ CROD Quick Start Complete!")
	fmt.Println("\nServices:")
	fmt.Println("  • Blockchain API: http://localhost:8000")
	fmt.Println("  • React GUI: http://localhost:8080")
	fmt.Println("\nPress Ctrl+C to stop all services")
	
	// Wait for interrupt
	select {}
}

func startFull() {
	fmt.Println("Starting full blockchain stack...")
	
	// Check Docker
	if err := checkDocker(); err != nil {
		color.Red("Docker is required for full stack: %v", err)
		return
	}
	
	color.New(color.FgYellow).Println("→ Starting all services with Docker Compose...")
	cmd := exec.Command("docker-compose", "-f", "docker-compose.blockchain.yml", "up", "-d")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	
	if err := cmd.Run(); err != nil {
		color.Red("Failed to start services: %v", err)
		return
	}
	
	color.Green("\n✓ Full blockchain stack started!")
	fmt.Println("\nServices:")
	fmt.Println("  • NATS JetStream: nats://localhost:4222")
	fmt.Println("  • Pattern Genesis: http://localhost:7007")
	fmt.Println("  • Short-term Memory: http://localhost:7031")
	fmt.Println("  • Working Memory: http://localhost:7037")
	fmt.Println("  • Quantum Node: http://localhost:7101")
	fmt.Println("  • Neural Genesis: http://localhost:7113")
	fmt.Println("  • Master Orchestrator: http://localhost:7127")
	fmt.Println("  • Time Travel Node: http://localhost:7179")
}

func startDev() {
	fmt.Println("Starting development mode...")
	color.Yellow("→ Starting services with hot reload...")
	
	// Start blockchain with nodemon
	blockchainCmd := exec.Command("npm", "run", "dev")
	blockchainCmd.Dir = "current/working"
	blockchainCmd.Stdout = os.Stdout
	blockchainCmd.Stderr = os.Stderr
	
	if err := blockchainCmd.Start(); err != nil {
		// Fallback to regular node
		color.Yellow("nodemon not found, using regular node")
		blockchainCmd = exec.Command("node", "blockchain-server.js")
		blockchainCmd.Dir = "current/working"
		blockchainCmd.Start()
	}
	
	// Start GUI dev server
	time.Sleep(2 * time.Second)
	guiCmd := exec.Command("npm", "run", "dev")
	guiCmd.Dir = "current/working/crod-gui"
	guiCmd.Stdout = os.Stdout
	guiCmd.Stderr = os.Stderr
	
	if err := guiCmd.Start(); err != nil {
		color.Red("Failed to start GUI dev server: %v", err)
	}
	
	color.Green("\n✓ Development mode started with hot reload!")
	select {}
}

func showStatus() {
	fmt.Println("CROD Service Status")
	fmt.Println("==================")
	
	services := []struct {
		name string
		port int
	}{
		{"Blockchain Core", 8000},
		{"React GUI", 8080},
		{"Polyglot Gateway", 4000},
		{"NATS JetStream", 4222},
		{"LLaMA Service", 5001},
		{"Pattern Genesis", 7007},
		{"Short Memory", 7031},
		{"Working Memory", 7037},
		{"Quantum Node", 7101},
		{"Orchestrator", 7127},
	}
	
	for _, svc := range services {
		checkService(svc.name, svc.port)
	}
}

func checkService(name string, port int) {
	cmd := exec.Command("lsof", "-i", fmt.Sprintf(":%d", port))
	if err := cmd.Run(); err != nil {
		color.Red("✗ %s (port %d) - Not running", name, port)
	} else {
		color.Green("✓ %s (port %d) - Running", name, port)
	}
}

func stopAll() {
	color.Yellow("Stopping all CROD services...")
	
	// Stop processes
	processes := []string{
		"blockchain-server.js",
		"http.server",
		"crod-llama-service.py",
		"crod-polyglot",
	}
	
	for _, proc := range processes {
		exec.Command("pkill", "-f", proc).Run()
	}
	
	// Stop Docker containers
	exec.Command("docker-compose", "-f", "docker-compose.blockchain.yml", "down").Run()
	
	color.Green("✓ All services stopped")
}

func startMonitor() {
	color.Cyan("Starting CROD Monitor...")
	cmd := exec.Command("./bin/crod-monitor")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Stdin = os.Stdin
	
	if err := cmd.Run(); err != nil {
		// Try to build and run
		color.Yellow("Monitor not found, building...")
		buildCmd := exec.Command("go", "build", "-o", "bin/crod-monitor", "./cmd/crod-monitor/main.go")
		if err := buildCmd.Run(); err != nil {
			color.Red("Failed to build monitor: %v", err)
			return
		}
		cmd.Run()
	}
}

func startVisualizer() {
	color.Cyan("Starting CROD Visualizer...")
	fmt.Println("Visualizer will be available at http://localhost:8888")
	
	cmd := exec.Command("./bin/crod-visualizer")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	
	if err := cmd.Run(); err != nil {
		// Try to build and run
		color.Yellow("Visualizer not found, building...")
		buildCmd := exec.Command("go", "build", "-o", "bin/crod-visualizer", "./cmd/crod-visualizer/main.go")
		if err := buildCmd.Run(); err != nil {
			color.Red("Failed to build visualizer: %v", err)
			return
		}
		cmd.Run()
	}
}

func checkDocker() error {
	cmd := exec.Command("docker", "--version")
	return cmd.Run()
}