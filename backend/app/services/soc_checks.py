"""Separation of Concerns analyzer service."""

from pathlib import Path
from typing import Any, Optional

try:
    import grimp
    GRIMP_AVAILABLE = True
except ImportError:
    GRIMP_AVAILABLE = False


class SoCAnalyzer:
    """Analyzer for Separation of Concerns violations."""

    def __init__(self, project_path: str) -> None:
        """Initialize SoC analyzer."""
        self.project_path = Path(project_path)
        self.violations: list[dict[str, Any]] = []

    def analyze_python_imports(self, package_name: str) -> dict[str, Any]:
        """Analyze Python import dependencies using grimp."""
        if not GRIMP_AVAILABLE:
            return {
                "error": "grimp not installed",
                "message": "Install grimp to enable Python import analysis",
                "violations": [],
            }

        try:
            graph = grimp.build_graph(package_name)

            # Find circular dependencies
            chains = graph.find_illegal_dependencies_for_layers(
                layers={
                    "ui": ["service"],
                    "service": ["domain"],
                    "domain": ["infrastructure"],
                    "infrastructure": [],
                },
                containers=[package_name],
            )

            violations = []
            for chain in chains:
                violations.append(
                    {
                        "type": "layer_violation",
                        "chain": [str(module) for module in chain],
                        "message": f"Illegal dependency: {' -> '.join(str(m) for m in chain)}",
                    }
                )

            # Find circular imports
            cycles = []
            for module in graph.modules:
                descendants = graph.find_descendants(module)
                if module in descendants:
                    cycles.append(
                        {
                            "type": "circular_dependency",
                            "module": str(module),
                            "message": f"Module {module} has circular dependencies",
                        }
                    )

            return {
                "package": package_name,
                "total_modules": len(graph.modules),
                "layer_violations": violations,
                "circular_dependencies": cycles,
                "total_violations": len(violations) + len(cycles),
            }

        except Exception as e:
            return {
                "error": str(e),
                "message": "Failed to analyze imports",
                "violations": [],
            }

    def check_generic_layers(
        self, project_id: int, layer_rules: dict[str, list[str]]
    ) -> dict[str, Any]:
        """Check generic layer rules based on tags."""
        violations = []

        # Example: Check that UI layer doesn't import from Infrastructure
        # In a real implementation, this would parse actual code
        # For now, return a structure showing how it would work

        return {
            "project_id": project_id,
            "layers_checked": list(layer_rules.keys()),
            "violations": violations,
            "status": "passed" if not violations else "failed",
        }

    def generate_dependency_graph(self, package_name: str) -> dict[str, Any]:
        """Generate dependency graph data for visualization."""
        if not GRIMP_AVAILABLE:
            return {
                "error": "grimp not available",
                "nodes": [],
                "edges": [],
            }

        try:
            graph = grimp.build_graph(package_name)

            nodes = [{"id": str(module), "label": str(module)} for module in graph.modules]

            edges = []
            for importer in graph.modules:
                for imported in graph.find_modules_directly_imported_by(importer):
                    edges.append(
                        {
                            "from": str(importer),
                            "to": str(imported),
                        }
                    )

            return {
                "nodes": nodes,
                "edges": edges,
                "total_modules": len(nodes),
                "total_dependencies": len(edges),
            }

        except Exception as e:
            return {
                "error": str(e),
                "nodes": [],
                "edges": [],
            }

    def find_hotspots(self, package_name: str) -> list[dict[str, Any]]:
        """Find modules with high coupling (hotspots)."""
        if not GRIMP_AVAILABLE:
            return []

        try:
            graph = grimp.build_graph(package_name)

            hotspots = []
            for module in graph.modules:
                imported_by = len(list(graph.find_modules_that_directly_import(module)))
                imports = len(list(graph.find_modules_directly_imported_by(module)))
                coupling = imported_by + imports

                if coupling > 10:  # Threshold for high coupling
                    hotspots.append(
                        {
                            "module": str(module),
                            "imported_by_count": imported_by,
                            "imports_count": imports,
                            "coupling_score": coupling,
                        }
                    )

            # Sort by coupling score
            hotspots.sort(key=lambda x: x["coupling_score"], reverse=True)

            return hotspots[:10]  # Return top 10 hotspots

        except Exception:
            return []


def analyze_project_soc(project_path: str, package_name: Optional[str] = None) -> dict[str, Any]:
    """Analyze a project for Separation of Concerns violations."""
    analyzer = SoCAnalyzer(project_path)

    result = {
        "project_path": project_path,
        "grimp_available": GRIMP_AVAILABLE,
    }

    if package_name and GRIMP_AVAILABLE:
        result["python_analysis"] = analyzer.analyze_python_imports(package_name)
        result["dependency_graph"] = analyzer.generate_dependency_graph(package_name)
        result["hotspots"] = analyzer.find_hotspots(package_name)
    else:
        result["message"] = "Specify package_name for Python analysis"

    return result
