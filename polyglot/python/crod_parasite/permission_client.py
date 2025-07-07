"""
Permission Client - Integrates with Elixir orchestrator for permission management
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

import structlog
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout, ErrNoServers

logger = structlog.get_logger()


class PermissionLevel(Enum):
    """Permission levels"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    SYSTEM = "system"


class PermissionScope(Enum):
    """Permission scopes"""
    USER = "user"
    PROJECT = "project"
    SYSTEM = "system"
    GLOBAL = "global"


class PermissionClient:
    """
    Client for checking permissions with the Elixir orchestrator
    
    I make sure users can only do what they're allowed to do,
    keeping everyone safe and happy.
    """
    
    def __init__(
        self,
        nats_url: str = "nats://localhost:4222",
        cache_ttl: int = 300  # 5 minutes
    ):
        self.nats_url = nats_url
        self.nc: Optional[NATS] = None
        self.cache_ttl = cache_ttl
        
        # Permission cache
        self._permission_cache: Dict[str, Dict[str, Any]] = {}
        
        # Default permissions for fallback
        self._default_permissions = {
            "query": [PermissionLevel.READ],
            "command": [PermissionLevel.EXECUTE],
            "system_control": [PermissionLevel.ADMIN, PermissionLevel.SYSTEM],
            "clarification": [PermissionLevel.READ],
            "conversation": [PermissionLevel.READ]
        }
        
    async def connect(self):
        """Connect to NATS for communication with orchestrator"""
        try:
            self.nc = NATS()
            await self.nc.connect(self.nats_url)
            logger.info("Connected to NATS for permission checks")
        except Exception as e:
            logger.warning(
                "NATS connection failed, using local permission rules",
                error=str(e)
            )
            self.nc = None
    
    async def disconnect(self):
        """Disconnect from NATS"""
        if self.nc and not self.nc.is_closed:
            await self.nc.close()
    
    async def check_permission(
        self,
        user_id: str,
        action: str,
        resource: Optional[Dict[str, Any]] = None,
        scope: PermissionScope = PermissionScope.USER
    ) -> bool:
        """
        Check if a user has permission for an action
        
        Returns True if allowed, False if denied
        """
        # Check cache first
        cache_key = f"{user_id}:{action}:{scope.value}"
        if cache_key in self._permission_cache:
            cached = self._permission_cache[cache_key]
            if datetime.utcnow() < cached["expires"]:
                logger.debug("Using cached permission", result=cached["allowed"])
                return cached["allowed"]
        
        # Check with orchestrator
        if self.nc and not self.nc.is_closed:
            try:
                allowed = await self._check_with_orchestrator(
                    user_id, action, resource, scope
                )
            except Exception as e:
                logger.error("Permission check failed", error=str(e))
                # Fall back to local rules
                allowed = await self._check_local_permission(user_id, action, scope)
        else:
            # Use local rules
            allowed = await self._check_local_permission(user_id, action, scope)
        
        # Cache the result
        self._permission_cache[cache_key] = {
            "allowed": allowed,
            "expires": datetime.utcnow() + timedelta(seconds=self.cache_ttl)
        }
        
        return allowed
    
    async def _check_with_orchestrator(
        self,
        user_id: str,
        action: str,
        resource: Optional[Dict[str, Any]],
        scope: PermissionScope
    ) -> bool:
        """Check permission with the Elixir orchestrator via NATS"""
        request = {
            "user_id": user_id,
            "action": action,
            "resource": resource or {},
            "scope": scope.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Send request and wait for response
            response = await self.nc.request(
                "permissions.check",
                json.dumps(request).encode(),
                timeout=2.0  # 2 second timeout
            )
            
            result = json.loads(response.data.decode())
            return result.get("allowed", False)
            
        except ErrTimeout:
            logger.warning("Permission check timed out")
            raise
        except Exception as e:
            logger.error("Permission check error", error=str(e))
            raise
    
    async def _check_local_permission(
        self,
        user_id: str,
        action: str,
        scope: PermissionScope
    ) -> bool:
        """
        Local permission checking when orchestrator is unavailable
        
        This is a simple fallback - in production, you'd have more
        sophisticated rules here.
        """
        # For demo purposes, we'll use simple rules
        
        # System actions require admin scope
        if action == "system_control" and scope != PermissionScope.SYSTEM:
            return False
        
        # Default permissions based on action
        required_levels = self._default_permissions.get(action, [PermissionLevel.READ])
        
        # For now, assume all users have READ and EXECUTE permissions
        # In production, you'd check against a user database
        user_levels = [PermissionLevel.READ, PermissionLevel.EXECUTE]
        
        # Check if user has any required level
        return any(level in user_levels for level in required_levels)
    
    async def get_user_permissions(self, user_id: str) -> Dict[str, Any]:
        """Get all permissions for a user"""
        if self.nc and not self.nc.is_closed:
            try:
                response = await self.nc.request(
                    "permissions.list",
                    json.dumps({"user_id": user_id}).encode(),
                    timeout=2.0
                )
                
                return json.loads(response.data.decode())
                
            except Exception as e:
                logger.error("Failed to get user permissions", error=str(e))
        
        # Return default permissions
        return {
            "user_id": user_id,
            "permissions": [
                {
                    "action": "query",
                    "scope": PermissionScope.USER.value,
                    "levels": ["read"]
                },
                {
                    "action": "command",
                    "scope": PermissionScope.USER.value,
                    "levels": ["execute"]
                }
            ]
        }
    
    async def request_permission(
        self,
        user_id: str,
        action: str,
        reason: str,
        scope: PermissionScope = PermissionScope.USER
    ) -> Dict[str, Any]:
        """Request additional permissions for a user"""
        request = {
            "user_id": user_id,
            "action": action,
            "reason": reason,
            "scope": scope.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.nc and not self.nc.is_closed:
            try:
                response = await self.nc.request(
                    "permissions.request",
                    json.dumps(request).encode(),
                    timeout=2.0
                )
                
                return json.loads(response.data.decode())
                
            except Exception as e:
                logger.error("Failed to request permission", error=str(e))
        
        # Return pending status
        return {
            "status": "pending",
            "request_id": f"local-{user_id}-{action}-{datetime.utcnow().timestamp()}",
            "message": "Permission request recorded. An admin will review it."
        }
    
    async def check_rate_limit(
        self,
        user_id: str,
        action: str,
        limit: int = 100,
        window: int = 3600  # 1 hour
    ) -> bool:
        """Check if user is within rate limits"""
        if self.nc and not self.nc.is_closed:
            try:
                response = await self.nc.request(
                    "ratelimit.check",
                    json.dumps({
                        "user_id": user_id,
                        "action": action,
                        "limit": limit,
                        "window": window
                    }).encode(),
                    timeout=1.0
                )
                
                result = json.loads(response.data.decode())
                return result.get("allowed", True)
                
            except Exception as e:
                logger.error("Rate limit check failed", error=str(e))
        
        # Default to allowing if can't check
        return True
    
    async def log_permission_event(
        self,
        user_id: str,
        action: str,
        allowed: bool,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log permission events for auditing"""
        event = {
            "user_id": user_id,
            "action": action,
            "allowed": allowed,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        if self.nc and not self.nc.is_closed:
            try:
                await self.nc.publish(
                    "permissions.events",
                    json.dumps(event).encode()
                )
            except Exception as e:
                logger.error("Failed to log permission event", error=str(e))
        
        # Always log locally as well
        logger.info(
            "Permission event",
            user_id=user_id,
            action=action,
            allowed=allowed
        )
    
    def clear_cache(self, user_id: Optional[str] = None):
        """Clear permission cache"""
        if user_id:
            # Clear specific user's cache
            keys_to_remove = [
                key for key in self._permission_cache
                if key.startswith(f"{user_id}:")
            ]
            for key in keys_to_remove:
                del self._permission_cache[key]
        else:
            # Clear all cache
            self._permission_cache.clear()
        
        logger.info("Permission cache cleared", user_id=user_id)