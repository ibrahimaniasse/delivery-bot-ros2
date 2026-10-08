import math
import os
import tempfile
import numpy as np
import pytest

from delivery_bot_ai.obstacle_avoidance_agent import QLearningAgent


class TestQLearningAgent:
    """Unit tests for the tabular Q-Learning autonomous navigation agent."""

    @pytest.fixture
    def agent(self) -> QLearningAgent:
        return QLearningAgent(
            learning_rate=0.1,
            discount_factor=0.95,
            epsilon=0.3,
            epsilon_decay=0.995,
            epsilon_min=0.05,
        )

    def test_initialization(self, agent: QLearningAgent) -> None:
        """Verify initialization parameters and action dimensions."""
        assert agent.alpha == 0.1
        assert agent.gamma == 0.95
        assert agent.epsilon == 0.3
        assert len(agent.actions) == 6
        assert len(agent.q_table) == 0

    def test_discretize_lidar_all_clear(self, agent: QLearningAgent) -> None:
        """All readings above WARN_DIST (1.0m) should produce CLEAR (0) across all sectors."""
        ranges = [2.5] * 360
        sectors = agent.discretize_lidar(ranges, num_sectors=5)
        assert len(sectors) == 5
        assert all(s == 0 for s in sectors)

    def test_discretize_lidar_warn_zone(self, agent: QLearningAgent) -> None:
        """Readings between DANGER (0.4m) and WARN (1.0m) should yield WARN (1)."""
        ranges = [0.6] * 360
        sectors = agent.discretize_lidar(ranges, num_sectors=5)
        assert all(s == 1 for s in sectors)

    def test_discretize_lidar_danger_zone(self, agent: QLearningAgent) -> None:
        """Readings below DANGER_DIST (0.4m) should yield DANGER (2)."""
        ranges = [0.2] * 360
        sectors = agent.discretize_lidar(ranges, num_sectors=5)
        assert all(s == 2 for s in sectors)

    def test_discretize_lidar_handles_inf_and_nan(self, agent: QLearningAgent) -> None:
        """Readings with inf and nan should be filtered safely."""
        ranges = [float("inf"), float("nan"), 3.0] * 120
        sectors = agent.discretize_lidar(ranges, num_sectors=5)
        assert all(s == 0 for s in sectors)

    def test_discretize_lidar_empty_fallback(self, agent: QLearningAgent) -> None:
        """Empty ranges should trigger fail-safe danger state."""
        sectors = agent.discretize_lidar([], num_sectors=5)
        assert all(s == 2 for s in sectors)

    def test_get_goal_direction_discrete_bins(self, agent: QLearningAgent) -> None:
        """Goal direction index must be in range [0, 7]."""
        direction = agent.get_goal_direction(
            current_pos=(0.0, 0.0), current_yaw=0.0, goal=(5.0, 5.0)
        )
        assert 0 <= direction <= 7

    def test_get_state_combines_lidar_and_goal(self, agent: QLearningAgent) -> None:
        """Full state should tuple 5 lidar sectors + 1 goal direction = 6 elements."""
        ranges = [2.0] * 360
        state = agent.get_state(
            lidar_ranges=ranges, position=(0.0, 0.0), yaw=0.0
        )
        assert len(state) == 6
        assert state[:5] == (0, 0, 0, 0, 0)
        assert 0 <= state[5] <= 7

    def test_bellman_q_table_update(self, agent: QLearningAgent) -> None:
        """Verify mathematical correctness of Bellman equation update."""
        state = (0, 0, 0, 0, 0, 1)
        next_state = (0, 0, 0, 0, 0, 2)
        action = 0
        reward = 10.0

        # Prepopulate next state with a known max Q-value
        agent.q_table[next_state][0] = 20.0
        agent.q_table[next_state][1] = 5.0

        # Initial Q(s, a) is 0.0
        # Expected new Q: 0.0 + 0.1 * (10.0 + 0.95 * 20.0 - 0.0)
        # = 0.1 * (10.0 + 19.0) = 2.9
        agent.update(state, action, reward, next_state)
        assert agent.q_table[state][action] == pytest.approx(2.9)

    def test_epsilon_decay_behavior(self, agent: QLearningAgent) -> None:
        """Epsilon should decay progressively and not fall below epsilon_min."""
        initial_eps = agent.epsilon
        agent.decay_epsilon()
        assert agent.epsilon == pytest.approx(initial_eps * 0.995)

        # Force decay multiple times to verify threshold clamp
        for _ in range(1000):
            agent.decay_epsilon()
        assert agent.epsilon == pytest.approx(agent.epsilon_min)

    def test_q_table_persistence(self, agent: QLearningAgent) -> None:
        """Saved Q-table must reload identically from disk."""
        state = (1, 0, 2, 0, 1, 3)
        agent.q_table[state][0] = 42.5
        agent.q_table[state][4] = -12.3

        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            agent.save(tmp_path)
            new_agent = QLearningAgent()
            new_agent.load(tmp_path)

            assert state in new_agent.q_table
            assert new_agent.q_table[state][0] == pytest.approx(42.5)
            assert new_agent.q_table[state][4] == pytest.approx(-12.3)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_action_velocities_bounds(self, agent: QLearningAgent) -> None:
        """All velocities must be within safe robot limits."""
        for action_idx in range(len(agent.actions)):
            linear, angular = agent.get_velocity(action_idx)
            assert 0.0 <= linear <= 0.5
            assert -1.0 <= angular <= 1.0
