from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


def _family_knowledge_source() -> TextFileKnowledgeSource:
    # Path is relative to the project knowledge/ directory (repo root when running locally).
    return TextFileKnowledgeSource(file_paths=["user_preference.txt"])


@CrewBase
class TripPlanningAssistant:
    """TripPlanningAssistant crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trip_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["trip_strategist"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def destination_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["destination_researcher"],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def itinerary_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["itinerary_architect"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def budget_and_links_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["budget_and_links_analyst"],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def family_trip_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["family_trip_editor"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def planning_brief_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_brief_task"],  # type: ignore[index]
        )

    @task
    def destination_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["destination_research_task"],  # type: ignore[index]
        )

    @task
    def itinerary_draft_task(self) -> Task:
        return Task(
            config=self.tasks_config["itinerary_draft_task"],  # type: ignore[index]
        )

    @task
    def budget_and_links_task(self) -> Task:
        return Task(
            config=self.tasks_config["budget_and_links_task"],  # type: ignore[index]
        )

    @task
    def finalize_trip_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["finalize_trip_plan_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TripPlanningAssistant crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[_family_knowledge_source()],
        )
