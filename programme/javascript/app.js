// If you want to use Phoenix channels, run `mix help phx.gen.channel`
// to get started and then uncomment the line below.
// import "./user_socket.js"

// You can include dependencies in two ways.
//
// The simplest option is to put them in assets/vendor and
// import them using relative paths:
//
//     import "../vendor/some-package.js"
//
// Alternatively, you can `npm install some-package --prefix assets` and import
// them using a path starting with the package name:
//
//     import "some-package"
//

// Include phoenix_html to handle method=PUT/DELETE in forms and buttons.
import "phoenix_html"
// Establish Phoenix Socket and LiveView configuration.
import {Socket} from "phoenix"
import {LiveSocket} from "phoenix_live_view"
import topbar from "../vendor/topbar"

let csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content")

// CROD Desktop Hooks
let Hooks = {}

Hooks.ConsciousnessChart = {
  mounted() {
    this.handleEvent("update-chart", ({data}) => {
      // Update consciousness chart visualization
      console.log("Consciousness update:", data)
    })
  }
}

Hooks.QuantumState = {
  mounted() {
    this.el.addEventListener("click", e => {
      // Trigger quantum measurement
      this.pushEvent("measure-quantum", {qubit: e.target.dataset.qubit})
    })
  }
}

Hooks.PatternStream = {
  mounted() {
    this.handleEvent("new-pattern", ({pattern}) => {
      // Add pattern to stream visualization
      const patternEl = document.createElement("div")
      patternEl.className = "pattern-item"
      patternEl.textContent = pattern
      this.el.prepend(patternEl)
      
      // Keep only last 20 patterns
      while (this.el.children.length > 20) {
        this.el.removeChild(this.el.lastChild)
      }
    })
  }
}

let liveSocket = new LiveSocket("/live", Socket, {
  params: {_csrf_token: csrfToken},
  hooks: Hooks
})

// Show progress bar on live navigation and form submits
topbar.config({barColors: {0: "#29d"}, shadowColor: "rgba(0, 0, 0, .3)"})
window.addEventListener("phx:page-loading-start", _info => topbar.show(300))
window.addEventListener("phx:page-loading-stop", _info => topbar.hide())

// connect if there are any LiveViews on the page
liveSocket.connect()

// expose liveSocket on window for web console debug logs and latency simulation:
// >> liveSocket.enableDebug()
// >> liveSocket.enableLatencySim(1000)  // enabled for duration of browser session
// >> liveSocket.disableLatencySim()
window.liveSocket = liveSocket

// CROD specific functionality
window.CROD = {
  activate() {
    console.log("🧠 CROD Activated!")
    document.body.classList.add("crod-active")
  },
  
  deactivate() {
    console.log("🔴 CROD Deactivated")
    document.body.classList.remove("crod-active")
  },
  
  showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.className = `notification notification-${type}`
    notification.textContent = message
    document.body.appendChild(notification)
    
    setTimeout(() => {
      notification.remove()
    }, 5000)
  }
}