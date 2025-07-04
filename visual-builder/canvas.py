"""
NETWORK CANVAS - Drag & Drop Canvas für Atoms
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import Optional, Tuple
import math

# Import at bottom to avoid circular import
# from network import CRODNetwork
# from atom_types import create_atom

class AtomVisual(QGraphicsItem):
    """Visual representation of an atom"""
    
    # Atom colors
    COLORS = {
        "thinker": "#FF6B6B",
        "doubter": "#4ECDC4",
        "learner": "#45B7D1",
        "connector": "#96CEB4",
        "evaluator": "#FFEAA7",
        "memory": "#DDA0DD",
        "synthesizer": "#98D8C8",
        "router": "#F7DC6F"
    }
    
    def __init__(self, atom_id: str, atom_type: str, x: float = 0, y: float = 0):
        super().__init__()
        self.atom_id = atom_id
        self.atom_type = atom_type
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        
        self.ports_in = []
        self.ports_out = []
        self.is_processing = False
        
    def boundingRect(self):
        return QRectF(-40, -30, 80, 60)
        
    def paint(self, painter, option, widget):
        # Get color
        color = QColor(self.COLORS.get(self.atom_type, "#888888"))
        
        # Draw shadow
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
        painter.drawRoundedRect(-38, -28, 80, 60, 10, 10)
        
        # Draw main rectangle
        if self.isSelected():
            painter.setPen(QPen(Qt.white, 3))
        else:
            painter.setPen(QPen(color.darker(150), 2))
            
        if self.is_processing:
            # Pulsing effect
            color = color.lighter(120)
            
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(-40, -30, 80, 60, 10, 10)
        
        # Draw type text
        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.atom_type)
        
        # Draw ports
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QBrush(Qt.darkGray))
        
        # Input ports (left side)
        for i, port in enumerate(self.ports_in):
            y = -20 + (i + 1) * 40 / (len(self.ports_in) + 1)
            painter.drawEllipse(QPointF(-40, y), 5, 5)
            
        # Output ports (right side)
        for i, port in enumerate(self.ports_out):
            y = -20 + (i + 1) * 40 / (len(self.ports_out) + 1)
            painter.drawEllipse(QPointF(40, y), 5, 5)
            
    def get_port_pos(self, port_name: str, is_output: bool) -> QPointF:
        """Get position of a port"""
        ports = self.ports_out if is_output else self.ports_in
        if port_name in ports:
            index = ports.index(port_name)
            x = 40 if is_output else -40
            y = -20 + (index + 1) * 40 / (len(ports) + 1)
            return self.mapToScene(QPointF(x, y))
        return self.scenePos()
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            # Update connections when moved
            if self.scene():
                canvas = self.scene().parent()
                if hasattr(canvas, 'update_connections'):
                    canvas.update_connections()
        return super().itemChange(change, value)

class ConnectionVisual(QGraphicsItem):
    """Visual representation of a connection"""
    
    def __init__(self, connection_id: str):
        super().__init__()
        self.connection_id = connection_id
        self.from_pos = QPointF()
        self.to_pos = QPointF()
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(-1)  # Behind atoms
        self.is_active = False
        
    def boundingRect(self):
        return QRectF(self.from_pos, self.to_pos).normalized().adjusted(-5, -5, 5, 5)
        
    def paint(self, painter, option, widget):
        if self.from_pos == self.to_pos:
            return
            
        # Draw connection line
        if self.isSelected():
            painter.setPen(QPen(Qt.white, 3))
        elif self.is_active:
            painter.setPen(QPen(Qt.green, 2))
        else:
            painter.setPen(QPen(Qt.gray, 2))
            
        # Calculate control points for bezier curve
        dx = self.to_pos.x() - self.from_pos.x()
        dy = self.to_pos.y() - self.from_pos.y()
        
        ctrl1 = QPointF(self.from_pos.x() + dx * 0.5, self.from_pos.y())
        ctrl2 = QPointF(self.to_pos.x() - dx * 0.5, self.to_pos.y())
        
        # Draw bezier curve
        path = QPainterPath()
        path.moveTo(self.from_pos)
        path.cubicTo(ctrl1, ctrl2, self.to_pos)
        painter.drawPath(path)
        
        # Draw arrow
        angle = math.atan2(dy, dx)
        arrow_length = 10
        arrow_angle = math.pi / 6
        
        p1 = self.to_pos - QPointF(
            arrow_length * math.cos(angle - arrow_angle),
            arrow_length * math.sin(angle - arrow_angle)
        )
        p2 = self.to_pos - QPointF(
            arrow_length * math.cos(angle + arrow_angle),
            arrow_length * math.sin(angle + arrow_angle)
        )
        
        painter.drawLine(self.to_pos, p1)
        painter.drawLine(self.to_pos, p2)
        
    def update_positions(self, from_pos: QPointF, to_pos: QPointF):
        """Update connection positions"""
        self.prepareGeometryChange()
        self.from_pos = from_pos
        self.to_pos = to_pos

class NetworkCanvas(QGraphicsView):
    """Main canvas for network visualization"""
    
    atom_selected = pyqtSignal(object)  # Emit atom when selected
    connection_selected = pyqtSignal(object)  # Emit connection when selected
    
    def __init__(self, network=None):
        super().__init__()
        self.network = network
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Visual items
        self.atom_visuals = {}
        self.connection_visuals = {}
        
        # Connection drawing
        self.drawing_connection = False
        self.temp_connection = None
        self.connection_start = None
        
        # Setup view
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
        # Dark background
        self.setStyleSheet("background-color: #1e1e1e;")
        self.scene.setBackgroundBrush(QBrush(QColor("#1e1e1e")))
        
        # Grid
        self.grid_size = 20
        
    def set_network(self, network):
        """Set new network"""
        self.network = network
        self.scene.clear()
        self.atom_visuals.clear()
        self.connection_visuals.clear()
        self.update()
        
    def drawBackground(self, painter, rect):
        """Draw grid background"""
        super().drawBackground(painter, rect)
        
        # Grid
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        lines = []
        for x in range(left, int(rect.right()), self.grid_size):
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))
        for y in range(top, int(rect.bottom()), self.grid_size):
            lines.append(QLineF(rect.left(), y, rect.right(), y))
            
        painter.setPen(QPen(QColor(50, 50, 50), 0.5))
        painter.drawLines(lines)
        
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        """Handle drag move"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        """Handle drop - create new atom"""
        if event.mimeData().hasText():
            atom_type = event.mimeData().text()
            pos = self.mapToScene(event.pos())
            
            # Snap to grid
            x = round(pos.x() / self.grid_size) * self.grid_size
            y = round(pos.y() / self.grid_size) * self.grid_size
            
            # Create atom in network
            from atom_types import create_atom
            atom = self.network.add_atom(atom_type, (x, y))
            
            # Create visual
            self.create_atom_visual(atom)
            
            event.acceptProposedAction()
            
    def create_atom_visual(self, atom):
        """Create visual for atom"""
        visual = AtomVisual(atom.id, atom.type, atom.position["x"], atom.position["y"])
        
        # Set ports
        visual.ports_in = atom.get_input_ports()
        visual.ports_out = atom.get_output_ports()
        
        self.scene.addItem(visual)
        self.atom_visuals[atom.id] = visual
        
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            
            if item and isinstance(item, AtomVisual):
                # Check if clicking on port
                scene_pos = self.mapToScene(event.pos())
                atom_pos = item.scenePos()
                relative_pos = scene_pos - atom_pos
                
                # Check output ports
                if relative_pos.x() > 20:  # Right side
                    self.start_connection(item, scene_pos)
                    return
                    
        super().mousePressEvent(event)
        
    def start_connection(self, atom_visual: AtomVisual, pos: QPointF):
        """Start drawing connection"""
        self.drawing_connection = True
        self.connection_start = (atom_visual, self.get_nearest_port(atom_visual, pos, True))
        
        # Create temporary connection line
        self.temp_connection = QGraphicsLineItem()
        self.temp_connection.setPen(QPen(Qt.white, 2, Qt.DashLine))
        self.scene.addItem(self.temp_connection)
        
    def get_nearest_port(self, atom_visual: AtomVisual, pos: QPointF, is_output: bool) -> str:
        """Get nearest port to position"""
        ports = atom_visual.ports_out if is_output else atom_visual.ports_in
        if not ports:
            return None
            
        min_dist = float('inf')
        nearest_port = ports[0]
        
        for port in ports:
            port_pos = atom_visual.get_port_pos(port, is_output)
            dist = (port_pos - pos).manhattanLength()
            if dist < min_dist:
                min_dist = dist
                nearest_port = port
                
        return nearest_port
        
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if self.drawing_connection and self.temp_connection:
            pos = self.mapToScene(event.pos())
            start_atom, start_port = self.connection_start
            start_pos = start_atom.get_port_pos(start_port, True)
            self.temp_connection.setLine(start_pos.x(), start_pos.y(), pos.x(), pos.y())
            
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton and self.drawing_connection:
            # End connection
            item = self.itemAt(event.pos())
            
            if item and isinstance(item, AtomVisual) and item != self.connection_start[0]:
                # Complete connection
                scene_pos = self.mapToScene(event.pos())
                end_port = self.get_nearest_port(item, scene_pos, False)
                
                if end_port:
                    start_atom, start_port = self.connection_start
                    
                    # Create connection in network
                    conn = self.network.connect_atoms(
                        start_atom.atom_id, start_port,
                        item.atom_id, end_port
                    )
                    
                    if conn:
                        self.create_connection_visual(conn)
                        
            # Clean up
            if self.temp_connection:
                self.scene.removeItem(self.temp_connection)
                self.temp_connection = None
                
            self.drawing_connection = False
            self.connection_start = None
            
        super().mouseReleaseEvent(event)
        
    def create_connection_visual(self, connection):
        """Create visual for connection"""
        visual = ConnectionVisual(connection.id)
        self.scene.addItem(visual)
        self.connection_visuals[connection.id] = visual
        self.update_connections()
        
    def update_connections(self):
        """Update all connection positions"""
        for conn_id, conn_visual in self.connection_visuals.items():
            if conn_id in self.network.connections:
                conn = self.network.connections[conn_id]
                
                # Get atom visuals
                from_visual = self.atom_visuals.get(conn.from_atom)
                to_visual = self.atom_visuals.get(conn.to_atom)
                
                if from_visual and to_visual:
                    from_pos = from_visual.get_port_pos(conn.from_port, True)
                    to_pos = to_visual.get_port_pos(conn.to_port, False)
                    conn_visual.update_positions(from_pos, to_pos)
                    
    def delete_selected(self):
        """Delete selected items"""
        for item in self.scene.selectedItems():
            if isinstance(item, AtomVisual):
                # Remove atom
                self.network.remove_atom(item.atom_id)
                del self.atom_visuals[item.atom_id]
                self.scene.removeItem(item)
                
            elif isinstance(item, ConnectionVisual):
                # Remove connection
                self.network.remove_connection(item.connection_id)
                del self.connection_visuals[item.connection_id]
                self.scene.removeItem(item)
                
        self.update_connections()
        
    def selectionChanged(self):
        """Handle selection change"""
        items = self.scene.selectedItems()
        if items:
            item = items[0]
            if isinstance(item, AtomVisual):
                atom = self.network.atoms.get(item.atom_id)
                if atom:
                    self.atom_selected.emit(atom)
            elif isinstance(item, ConnectionVisual):
                conn = self.network.connections.get(item.connection_id)
                if conn:
                    self.connection_selected.emit(conn)
                    
    def update(self):
        """Update canvas"""
        super().update()
        
        # Update atom states
        for atom_id, visual in self.atom_visuals.items():
            if atom_id in self.network.atoms:
                atom = self.network.atoms[atom_id]
                visual.is_processing = atom.state.get("processing", False)
                visual.update()
                
        # Update connection states
        # TODO: Show data flow