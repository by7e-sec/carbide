from typing import Dict

from libs.agent import Agent

from .agent import Agent


class AgentsRegistry:
    """Global registry for all agents."""

    _instance = None
    _agents: Dict[str, Agent] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register_provider(self, agent_class: Agent) -> None:
        """Register a provider class with the registry."""
        agent_name = agent_class.get_name().upper()
        if agent_name in self._agents:
            raise ValueError(f"Provider '{agent_name}' is already registered")
        self._agents[agent_name] = agent_class

    def instance_agent(self, agent_name: str) -> Agent | None:
        """Get a registered provider by name."""
        _agent_class: Agent = self._agents.get(agent_name)
        if _agent_class:
            return _agent_class()

    def get_agents(self) -> Dict[str, Agent]:
        """Get all providers of a specific type."""
        return {name: cls for name, cls in self._agents.items()}

    def discover_agents(self, package_name: str) -> None:
        """Discover and register providers in a package."""
        import importlib
        import pkgutil

        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package_name}.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Agent) and attr != Agent:
                    self.register_provider(attr)
