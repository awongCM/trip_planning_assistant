from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from trip_planning_assistant.tools import (
    FlightSearchTool,
    HotelSearchTool,
    WeatherTool,
    CurrencyConversionTool
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TripPlanningAssistant():
    """TripPlanningAssistant crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def destination_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['destination_researcher'],
            tools=[WeatherTool()],
            verbose=True
        )

    @agent
    def flight_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['flight_searcher'],
            tools=[FlightSearchTool()],
            verbose=True
        )

    @agent
    def hotel_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['hotel_finder'],
            tools=[HotelSearchTool()],
            verbose=True
        )

    @agent
    def currency_converter(self) -> Agent:
        return Agent(
            config=self.agents_config['currency_converter'],
            tools=[CurrencyConversionTool()],
            verbose=True
        )

    @agent
    def itinerary_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_builder'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_destination_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_destination_task'],
        )

    @task
    def search_flights_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_flights_task'],
        )

    @task
    def find_hotels_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_hotels_task'],
        )

    @task
    def convert_budget_task(self) -> Task:
        return Task(
            config=self.tasks_config['convert_budget_task'],
        )

    @task
    def build_itinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config['build_itinerary_task'],
            output_file='trip_itinerary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TripPlanningAssistant crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
